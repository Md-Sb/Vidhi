import os
import streamlit as st
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI


# =========================================================
# VIDHI - AI ASSISTANT FOR INDIAN STANDARDS
# =========================================================

load_dotenv()

INDEX_DIR = "faiss_index"

# IMPORTANT:
# This MUST be the same embedding model used when the
# FAISS index was created.
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="VIDHI - AI Assistant for Indian Standards",
    page_icon="🇮🇳",
    layout="centered",
)

st.title("VIDHI 🇮🇳")

st.caption(
    "AI Assistant for Bureau of Indian Standards — "
    "ask questions about BIS documents"
)


# =========================================================
# LOCAL EMBEDDING CLASS
# =========================================================

class LocalEmbeddings(Embeddings):

    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def embed_documents(self, texts):
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        return embeddings.tolist()

    def embed_query(self, text):
        embedding = self.model.encode(
            [text],
            normalize_embeddings=True,
            show_progress_bar=False
        )
        return embedding[0].tolist()


# =========================================================
# LOAD LOCAL EMBEDDINGS
# =========================================================

@st.cache_resource
def load_embeddings():

    return LocalEmbeddings()


# =========================================================
# LOAD FAISS DATABASE
# =========================================================

@st.cache_resource
def load_vectorstore():

    embeddings = load_embeddings()

    vectorstore = FAISS.load_local(
        INDEX_DIR,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    return vectorstore


# =========================================================
# LOAD GEMINI
# =========================================================

@st.cache_resource
def load_llm():

    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0.1,
    )


# =========================================================
# EXTRACT GEMINI RESPONSE
# =========================================================

def extract_answer(response):

    content = response.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict):

                if "text" in item:
                    text_parts.append(str(item["text"]))

                elif "content" in item:
                    text_parts.append(str(item["content"]))

            elif isinstance(item, str):

                text_parts.append(item)

        if text_parts:
            return "\n".join(text_parts)

    return str(content)


# =========================================================
# CHECK FAISS INDEX
# =========================================================

if not os.path.exists(INDEX_DIR):

    st.error(
        "FAISS index not found.\n\n"
        "Please create the FAISS index before running VIDHI."
    )

    st.stop()


# =========================================================
# LOAD SYSTEMS
# =========================================================

try:

    with st.spinner("Loading VIDHI..."):

        vectorstore = load_vectorstore()
        llm = load_llm()

except Exception as e:

    st.error("VIDHI could not start correctly.")

    st.code(str(e))

    st.stop()


# =========================================================
# USER QUESTION
# =========================================================

query = st.text_input(
    "Ask a question about the Indian Standard:",
    placeholder="Example: What are the requirements for packaged drinking water?"
)


# =========================================================
# PROCESS QUESTION
# =========================================================

if query:

    # -----------------------------------------------------
    # RETRIEVE DOCUMENTS
    # -----------------------------------------------------

    with st.spinner("Searching BIS documents..."):

        try:

            # Retrieve more candidates so that the correct
            # clause has a better chance of being found.
            docs_with_scores = vectorstore.similarity_search_with_score(
                query,
                k=8,
            )

        except Exception as e:

            st.error("Error while searching the BIS knowledge base.")

            st.code(str(e))

            st.stop()


    # -----------------------------------------------------
    # REMOVE VERY WEAK RESULTS
    # -----------------------------------------------------

    docs = []

    for doc, score in docs_with_scores:

        docs.append(doc)


    if not docs:

        st.warning(
            "No relevant BIS information was found."
        )

        st.stop()


    # -----------------------------------------------------
    # BUILD BIS CONTEXT
    # -----------------------------------------------------

    context_parts = []

    for i, doc in enumerate(docs):

        metadata = doc.metadata

        standard = metadata.get(
            "standard_number",
            metadata.get("standard", "Unknown Standard")
        )

        title = metadata.get(
            "title",
            "Unknown Title"
        )

        clause = metadata.get(
            "clause_number",
            metadata.get("clause", "Unknown Clause")
        )

        page = metadata.get(
            "page",
            metadata.get("page_start", "Unknown")
        )

        source = metadata.get(
            "source",
            metadata.get("filename", "Unknown Document")
        )

        context_parts.append(
            f"""
========================
BIS EVIDENCE {i + 1}
========================

Standard: {standard}

Title: {title}

Clause: {clause}

Page: {page}

Source: {source}

Content:
{doc.page_content}
"""
        )

    context = "\n".join(context_parts)


    # -----------------------------------------------------
    # GEMINI PROMPT
    # -----------------------------------------------------

    prompt = f"""
You are VIDHI, an AI assistant specialized in
Bureau of Indian Standards (BIS) documents.

Your task is to answer the user's question using
the BIS evidence supplied below.

IMPORTANT RULES:

1. Use the provided BIS evidence as your primary source.

2. Do NOT invent requirements, values, limits, test methods,
   definitions, clauses, or standards.

3. If the answer is clearly present in the evidence,
   answer it directly and confidently.

4. If the evidence only partially answers the question,
   answer the supported part and clearly mention what
   information is not available.

5. Do not automatically say that information is insufficient
   simply because the exact wording of the question does not
   appear in the evidence.

6. Carefully interpret the retrieved BIS clauses and combine
   relevant evidence when multiple clauses relate to the question.

7. Mention the relevant BIS standard and clause number whenever
   possible.

8. Keep the answer concise but useful.

9. If numerical requirements or limits are present in the
   evidence, reproduce them accurately.

10. Never use outside knowledge to create a BIS requirement.

USER QUESTION:

{query}

BIS DOCUMENT EVIDENCE:

{context}

ANSWER FORMAT:

Give a clear answer first.

Then, where applicable, include:

Source:
- BIS Standard
- Clause
- Page

Now answer the user's question.
"""


    # -----------------------------------------------------
    # GENERATE ANSWER
    # -----------------------------------------------------

    with st.spinner("Generating VIDHI answer..."):

        try:

            response = llm.invoke(prompt)

            answer = extract_answer(response)

        except Exception as e:

            st.error("Gemini could not generate the answer.")

            st.code(str(e))

            st.stop()


    # -----------------------------------------------------
    # DISPLAY ANSWER
    # -----------------------------------------------------

    st.subheader("VIDHI Answer")

    st.markdown(answer)


    # -----------------------------------------------------
    # DISPLAY RETRIEVED SOURCES
    # -----------------------------------------------------

    st.subheader("📚 Sources Used")

    for i, doc in enumerate(docs):

        metadata = doc.metadata

        standard = metadata.get(
            "standard_number",
            metadata.get("standard", "Unknown Standard")
        )

        clause = metadata.get(
            "clause_number",
            metadata.get("clause", "Unknown Clause")
        )

        page = metadata.get(
            "page",
            metadata.get("page_start", "Unknown")
        )

        source = metadata.get(
            "source",
            metadata.get("filename", "Unknown Document")
        )

        with st.expander(
            f"Source {i + 1} — {standard} | Clause {clause} | Page {page}"
        ):

            st.write(
                f"**Document:** {source}"
            )

            st.write(
                f"**Standard:** {standard}"
            )

            st.write(
                f"**Clause:** {clause}"
            )

            st.write(
                f"**Page:** {page}"
            )

            st.write(
                doc.page_content
            )