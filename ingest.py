import json
import os

from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS


# =========================================================
# VIDI LOCAL EMBEDDING INGESTION
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHUNK_FILE = os.path.join(
    BASE_DIR,
    "BIS Data Manager_Priyanshu",
    "output",
    "chunks",
    "bis_chunks.json"
)

INDEX_DIR = os.path.join(
    BASE_DIR,
    "faiss_index"
)


print("=" * 60)
print("VIDHI BIS RAG INGESTION")
print("=" * 60)


# =========================================================
# LOAD BIS CHUNKS
# =========================================================

print("\nStep 1: Loading validated BIS chunks...")

with open(
    CHUNK_FILE,
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)

chunks = data.get("chunks", [])

print(f"  Loaded {len(chunks)} BIS chunks.")


# =========================================================
# CONVERT TO LANGCHAIN DOCUMENTS
# =========================================================

documents = []

for chunk in chunks:

    metadata = {
        "standard_number": chunk.get("standard_number", ""),
        "title": chunk.get("title", ""),
        "edition": chunk.get("edition", ""),
        "status": chunk.get("status", ""),
        "sector": chunk.get("sector", ""),
        "product": chunk.get("product", ""),
        "source": chunk.get("source", ""),
        "filename": chunk.get("filename", ""),
        "clause": chunk.get("clause", ""),
        "page_start": chunk.get("page_start", ""),
        "page_end": chunk.get("page_end", ""),
        "chunk_id": chunk.get("chunk_id", "")
    }

    documents.append(
        Document(
            page_content=chunk.get("text", ""),
            metadata=metadata
        )
    )


# =========================================================
# LOCAL EMBEDDING MODEL
# =========================================================

print("\nStep 2: Loading local embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("  Local embedding model ready.")


# =========================================================
# CUSTOM EMBEDDING CLASS
# =========================================================

class LocalEmbeddings:

    def embed_documents(self, texts):
        return model.encode(
            texts,
            normalize_embeddings=True
        ).tolist()

    def embed_query(self, text):
        return model.encode(
            text,
            normalize_embeddings=True
        ).tolist()


embeddings = LocalEmbeddings()


# =========================================================
# CREATE FAISS INDEX
# =========================================================

print("\nStep 3: Creating FAISS index...")

vectorstore = FAISS.from_documents(
    documents,
    embeddings
)


# =========================================================
# SAVE
# =========================================================

print("\nStep 4: Saving FAISS index...")

vectorstore.save_local(
    INDEX_DIR
)


print("\n" + "=" * 60)
print("INGESTION COMPLETE")
print("=" * 60)

print(f"Documents embedded : {len(documents)}")
print(f"FAISS index        : {INDEX_DIR}")

print("\n✅ LOCAL RAG VECTOR DATABASE READY")
print("✅ No Gemini embedding quota required")
print("=" * 60)