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

    def to_metadata(self) -> Dict[str, Any]:
        """Return every field except the raw text, as a plain dict.
        Used to attach metadata onto search results."""
        return {
            "standard_number": self.standard_number,
            "edition": self.edition,
            "clause": self.clause,
            "page": self.page,
            "product": self.product,
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
        "product": "Cement Concrete"
      },
      ...
    ]
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

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Embed the query, search the FAISS index, and return the top_k
        matching chunks with their similarity score and full metadata.
        """
        if self.index is None:
            raise ValueError("Index not built yet. Call build_index() first.")

        query_vector = self._embed([query])   # embed the query the same way as chunks

        # index.search returns two arrays:
        #   scores[0]  -> similarity score of each match (higher = closer)
        #   indices[0] -> row number of each match inside the FAISS index
        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                # FAISS returns -1 if there are fewer chunks than top_k.
                continue
            chunk = self.chunks[idx]
            results.append({
                "text": chunk.text,
                "score": float(score),
                **chunk.to_metadata(),   # unpacks standard_number, edition, clause, page, product
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


def retrieve(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    The main function you asked for. Returns a list of dicts like:
    {
        "text": "...",
        "score": 0.83,
        "standard_number": "IS 456",
        "edition": "2000",
        "clause": "5.3.2",
        "page": 12,
        "product": "Cement Concrete"
    }
    """
    if not _is_built:
        raise RuntimeError(
            "Call initialize(chunks) once before calling retrieve()."
        )
    return _retriever.retrieve(query, top_k)


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
    ]

    initialize(sample_chunks)

    results = retrieve("what grade of concrete is required?", top_k=2)

    for r in results:
        print(f"\nScore: {r['score']:.3f}")
        print(f"Standard: {r['standard_number']} ({r['edition']})")
        print(f"Clause: {r['clause']} | Page: {r['page']} | Product: {r['product']}")
        print(f"Text: {r['text']}")
