"""
ingest.py
---------
Run this file ONCE (and again whenever you add new PDFs to data/).

What it does, step by step:
1. Reads every PDF inside the data/ folder.
2. Splits the text into small overlapping chunks (so the model gets
   focused context instead of a whole 50-page document at once).
3. Converts each chunk into a vector (a list of numbers that represents
   its meaning) using Google's embedding model.
4. Stores all those vectors in a FAISS index on disk, so app.py can
   later search them instantly without recomputing anything.
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load GOOGLE_API_KEY from the .env file into the environment
load_dotenv()

DATA_DIR = "data"
INDEX_DIR = "faiss_index"


def load_documents():
    """Load every PDF in data/ into LangChain 'Document' objects (one per page)."""
    docs = []
    if not os.path.isdir(DATA_DIR):
        raise FileNotFoundError(f"'{DATA_DIR}/' does not exist. Create it and add PDFs.")

    pdf_files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith(".pdf")]
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in '{DATA_DIR}/'.")

    for filename in pdf_files:
        path = os.path.join(DATA_DIR, filename)
        print(f"Loading: {filename}")
        loader = PyPDFLoader(path)
        docs.extend(loader.load())  # one Document per PDF page
    return docs


def main():
    print("Step 1: Loading PDFs...")
    docs = load_documents()
    print(f"  Loaded {len(docs)} pages total.\n")

    print("Step 2: Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,      # ~1000 characters per chunk
        chunk_overlap=150,    # slight overlap so context isn't cut mid-sentence
    )
    chunks = splitter.split_documents(docs)
    print(f"  Created {len(chunks)} chunks.\n")



    print("Step 3: Creating embeddings and building FAISS index...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )
    vectorstore = FAISS.from_documents(chunks, embeddings)



    print(f"Step 4: Saving index to '{INDEX_DIR}/'...")
    vectorstore.save_local(INDEX_DIR)

    print("\nDone. You can now run: streamlit run app.py")


if __name__ == "__main__":
    main()
