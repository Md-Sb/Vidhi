"""
BIS RAG Retrieval Module
=========================
A minimal, beginner-friendly retrieval component for a RAG (Retrieval
Augmented Generation) pipeline over text extracted from BIS
(Bureau of Indian Standards) PDFs.

Each retrievable unit ("chunk") is one piece of extracted text plus
its metadata:
    - standard_number : e.g. "IS 456"
    - edition          : e.g. "2000, Reaffirmed 2016"
    - clause           : e.g. "5.3.2"
    - page             : the PDF page number the text came from
    - product          : product/category the standard covers, e.g. "Cement"
    - status           : "current", "superseded", or "withdrawn" -- lets
                          retrieve() prioritize/filter by relevance status

Install dependencies first (in your terminal, not in this file):
    pip install sentence-transformers faiss-cpu numpy
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


# ---------------------------------------------------------------------------
# 1. The data structure for a single chunk
# ---------------------------------------------------------------------------

@dataclass
class Chunk:
    """
    One retrievable unit: the text itself, plus everything needed to
    trace it back to its exact place in a BIS standard document.
    """
    text: str
    standard_number: str
    edition: str
    clause: str
    page: int
    product: str
    # Defaults to "current" so existing data (and the JSON schema you were
    # already using) keeps working without any change. Set this to
    # "superseded" or "withdrawn" for standards that have been replaced.
    status: str = "current"

    def to_metadata(self) -> Dict[str, Any]:
        """Return every field except the raw text, as a plain dict.
        Used to attach metadata onto search results."""
        return {
            "standard_number": self.standard_number,
            "edition": self.edition,
            "clause": self.clause,
            "page": self.page,
            "product": self.product,
            "status": self.status,
        }


def load_chunks_from_json(path: str) -> List[Chunk]:
    """
    Load chunks from a JSON file shaped like:
    [
      {
        "text": "...",
        "standard_number": "IS 456",
        "edition": "2000",
        "clause": "5.3.2",
        "page": 12,
        "product": "Cement Concrete",
        "status": "current"
      },
      ...
    ]
    "status" is optional in your JSON -- it defaults to "current" if omitted.
    This is where your actual PDF-extraction pipeline output plugs in.
    """
    with open(path, "r", encoding="utf-8") as f:
        raw_items = json.load(f)
    return [Chunk(**item) for item in raw_items]


# ---------------------------------------------------------------------------
# 2. The retriever: embeddings + FAISS index + search
# ---------------------------------------------------------------------------

class BISRetriever:
    """
    Wraps an embedding model and a FAISS vector index together, and
    keeps a parallel list of Chunk objects so every vector in the
    index can be mapped back to its metadata.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # SentenceTransformer downloads and loads a pretrained model that
        # turns text into a fixed-length numeric vector ("embedding").
        # "all-MiniLM-L6-v2" is small, fast, free, and runs locally
        # (no API key needed) -- good default for a first RAG project.
        self.model = SentenceTransformer(model_name)

        # FAISS index object; created later once we know the vector size.
        self.index: Optional[faiss.Index] = None

        # Parallel list: self.chunks[i] is the metadata for the vector
        # stored at row i of the FAISS index. This is how we go from
        # "FAISS says row 7 matched" back to "that's clause 5.3.2, page 12".
        self.chunks: List[Chunk] = []

    def _embed(self, texts: List[str]) -> np.ndarray:
        """Convert a list of strings into a 2D array of embeddings."""
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,       # return a numpy array, which FAISS needs
            show_progress_bar=False,
            normalize_embeddings=True,   # scale each vector to length 1
        )
        # FAISS expects 32-bit floats, not numpy's default 64-bit floats.
        return embeddings.astype("float32")

    def build_index(self, chunks: List[Chunk]) -> None:
        """
        Embed every chunk's text and load the vectors into a FAISS
        index. Call this once, after loading your chunk data.
        """
        if not chunks:
            raise ValueError(
                "build_index() received an empty chunk list -- "
                "nothing to index. Check your extraction/loading step."
            )

        self.chunks = chunks
        texts = [c.text for c in chunks]

        embeddings = self._embed(texts)          # shape: (num_chunks, vector_dim)
        vector_dim = embeddings.shape[1]

        # IndexFlatIP = "Flat" (brute-force, exact search) using
        # "Inner Product" as the similarity score. Because we normalized
        # every embedding to length 1 above, inner product here is
        # mathematically equivalent to cosine similarity -- a standard
        # and simple way to compare text meaning.
        self.index = faiss.IndexFlatIP(vector_dim)

        # Load all vectors into the index. Row order here must match
        # self.chunks order, since that's how we map results back later.
        self.index.add(embeddings)

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        prioritize_current: bool = True,
        current_boost: float = 0.05,
        exclude_withdrawn: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Embed the query, search the FAISS index, and return the top_k
        matching chunks with their similarity score and full metadata.

        filters              : optional exact-match filter on metadata,
                                e.g. {"product": "Cement"} or
                                {"standard_number": "IS 456"}. Only chunks
                                matching every key/value pair are kept.
        prioritize_current   : if True, chunks whose status == "current"
                                are ranked higher than equally-similar
                                superseded/withdrawn ones.
        current_boost        : how much score to add to "current" chunks
                                when prioritize_current is True. Since
                                similarity scores are cosine-like values
                                between -1 and 1, a small boost (e.g. 0.05)
                                is usually enough to reorder close matches
                                without overriding a much better match.
        exclude_withdrawn    : if True, chunks with status == "withdrawn"
                                are dropped entirely -- a withdrawn standard
                                is no longer a valid answer, not just a
                                lower-priority one.
        """
        if self.index is None:
            raise ValueError("Index not built yet. Call build_index() first.")

        query_vector = self._embed([query])   # embed the query the same way as chunks

        # FAISS itself has no idea about "product", "status", etc. -- it only
        # ranks by vector similarity. So we ask it for more candidates than
        # top_k (a "candidate pool"), then filter/re-rank that pool in plain
        # Python using the metadata. This is the simplest way to combine
        # FAISS with metadata filtering for a small/medium dataset.
        pool_size = min(top_k * 5, len(self.chunks))
        scores, indices = self.index.search(query_vector, pool_size)

        candidates = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                # FAISS returns -1 if there are fewer chunks than pool_size.
                continue
            chunk = self.chunks[idx]

            # --- exact-match metadata filtering -------------------------
            if filters:
                # getattr(chunk, key, None) reads e.g. chunk.product safely;
                # if any requested field doesn't match, skip this chunk.
                if any(getattr(chunk, key, None) != value for key, value in filters.items()):
                    continue

            # --- drop withdrawn standards entirely -----------------------
            if exclude_withdrawn and chunk.status == "withdrawn":
                continue

            # --- compute the score used for ranking -----------------------
            # adjusted_score is only used to decide ordering; the original,
            # unmodified similarity_score is still what gets returned, so
            # results stay honest about actual semantic closeness.
            adjusted_score = float(score)
            if prioritize_current and chunk.status == "current":
                adjusted_score += current_boost

            candidates.append((adjusted_score, float(score), chunk))

        # Re-sort the filtered/boosted pool, highest adjusted_score first,
        # then keep only the top_k we actually want to return.
        candidates.sort(key=lambda c: c[0], reverse=True)
        top_candidates = candidates[:top_k]

        results = []
        for _, similarity_score, chunk in top_candidates:
            results.append({
                "similarity_score": similarity_score,
                "standard_number": chunk.standard_number,
                "edition": chunk.edition,
                "clause": chunk.clause,
                "page": chunk.page,
                "text": chunk.text,
                "status": chunk.status,
            })
        return results


# ---------------------------------------------------------------------------
# 3. Module-level convenience: a single global retriever + retrieve(query)
# ---------------------------------------------------------------------------

# One shared retriever instance for the whole module, so callers can just
# do `from bis_rag_retrieval import retrieve` without managing an object.
_retriever = BISRetriever()
_is_built = False


def initialize(chunks: List[Chunk]) -> None:
    """Build the index once, at startup, from your real chunk data."""
    global _is_built
    _retriever.build_index(chunks)
    _is_built = True


def retrieve(
    query: str,
    top_k: int = 5,
    filters: Optional[Dict[str, Any]] = None,
    prioritize_current: bool = True,
    current_boost: float = 0.05,
    exclude_withdrawn: bool = True,
) -> List[Dict[str, Any]]:
    """
    The main function you asked for. Returns a list of dicts like:
    {
        "similarity_score": 0.83,
        "standard_number": "IS 456",
        "edition": "2000",
        "clause": "5.3.2",
        "page": 12,
        "text": "...",
        "status": "current"
    }

    Examples:
        retrieve("grade of concrete")
            -> current standards ranked slightly above superseded ones

        retrieve("grade of concrete", filters={"product": "Cement"})
            -> only chunks whose product == "Cement"

        retrieve("grade of concrete", prioritize_current=False)
            -> pure similarity ranking, no status-based boosting
    """
    if not _is_built:
        raise RuntimeError(
            "Call initialize(chunks) once before calling retrieve()."
        )
    return _retriever.retrieve(
        query,
        top_k=top_k,
        filters=filters,
        prioritize_current=prioritize_current,
        current_boost=current_boost,
        exclude_withdrawn=exclude_withdrawn,
    )


# ---------------------------------------------------------------------------
# 4. Demo run with sample data (replace with load_chunks_from_json in real use)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sample_chunks = [
        Chunk(
            text="Minimum grade of concrete for reinforced concrete work "
                 "shall not be less than M20 in mild exposure conditions.",
            standard_number="IS 456",
            edition="2000, Reaffirmed 2016",
            clause="6.1.2",
            page=14,
            product="Reinforced Cement Concrete",
        ),
        Chunk(
            text="Ordinary Portland Cement 43 Grade shall conform to the "
                 "physical requirements specified in Table 5.",
            standard_number="IS 8112",
            edition="2013",
            clause="7.2",
            page=6,
            product="Cement",
        ),
        Chunk(
            text="Water used for mixing and curing concrete shall be clean "
                 "and free from injurious amounts of oil, acid, and alkali.",
            standard_number="IS 456",
            edition="2000, Reaffirmed 2016",
            clause="5.4",
            page=11,
            product="Reinforced Cement Concrete",
        ),
        Chunk(
            text="Minimum grade of concrete for reinforced work shall not "
                 "be less than M15 in mild exposure conditions.",
            standard_number="IS 456",
            edition="1978",
            clause="6.1",
            page=9,
            product="Reinforced Cement Concrete",
            status="superseded",   # replaced by the 2000 edition, clause 6.1.2
        ),
    ]

    initialize(sample_chunks)

    print("=== Default: current standards prioritized ===")
    results = retrieve("what grade of concrete is required?", top_k=2)
    for r in results:
        print(f"\nSimilarity score: {r['similarity_score']:.3f} | Status: {r['status']}")
        print(f"Standard: {r['standard_number']} ({r['edition']})")
        print(f"Clause: {r['clause']} | Page: {r['page']}")
        print(f"Text: {r['text']}")

    print("\n=== Filtered to a specific product ===")
    filtered_results = retrieve(
        "what grade of concrete is required?",
        top_k=2,
        filters={"product": "Cement"},
    )
    for r in filtered_results:
        print(f"\nSimilarity score: {r['similarity_score']:.3f} | Status: {r['status']}")
        print(f"Standard: {r['standard_number']} ({r['edition']})")
        print(f"Text: {r['text']}")
