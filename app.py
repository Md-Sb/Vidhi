"""
app.py
------
VIDHI - AI Assistant for Indian Standards

Run with:
    streamlit run app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)

from langchain_community.vectorstores import FAISS


# ---------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

load_dotenv()

INDEX_DIR = "faiss_index"


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# LOAD VECTOR DATABASE
# ---------------------------------------------------------

@st.cache_resource
def load_vectorstore():

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    vectorstore = FAISS.load_local(
        INDEX_DIR,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    return vectorstore


# ---------------------------------------------------------
# LOAD GEMINI
# ---------------------------------------------------------

@st.cache_resource
def load_llm():

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0.2,
    )

    return llm


# ---------------------------------------------------------
# EXTRACT TEXT FROM GEMINI RESPONSE
# ---------------------------------------------------------

def extract_answer(response):

    content = response.content

    # Case 1: Gemini returns normal string
    if isinstance(content, str):
        return content

    # Case 2: Gemini returns a list of content blocks
    if isinstance(content, list):

        text_parts = []

        for item in content:

            # Dictionary content block
            if isinstance(item, dict):

                if "text" in item:
                    text_parts.append(str(item["text"]))

                elif "content" in item:
                    text_parts.append(str(item["content"]))

            # Plain string inside list
            elif isinstance(item, str):

                text_parts.append(item)

            # Other object
            else:

                text_parts.append(str(item))

        if text_parts:
            return "\n".join(text_parts)

    # Fallback
    return str(content)


# ---------------------------------------------------------
# CHECK INDEX
# ---------------------------------------------------------

if not os.path.exists(INDEX_DIR):

    st.error(
        "No FAISS index found.\n\n"
        "1. Put a BIS PDF inside the `data/` folder.\n"
        "2. Run `python ingest.py` in your terminal.\n"
        "3. Refresh this page."
    )

else:

    # Load vector database
    vectorstore = load_vectorstore()

    # Load Gemini
    llm = load_llm()


    # -----------------------------------------------------
    # USER QUESTION
    # -----------------------------------------------------

    query = st.text_input(
        "Ask a question about the Indian Standard:"
    )


    # -----------------------------------------------------
    # PROCESS QUESTION
    # -----------------------------------------------------

    if query:

        # -------------------------------------------------
        # RETRIEVE RELEVANT DOCUMENT CHUNKS
        # -------------------------------------------------

        with st.spinner("Searching BIS documents..."):

            docs = vectorstore.similarity_search(
                query,
                k=4,
            )


        # -------------------------------------------------
        # BUILD CONTEXT
        # -------------------------------------------------

        context_parts = []

        for i, doc in enumerate(docs):

            source = doc.metadata.get(
                "source",
                "Unknown document"
            )

            page = doc.metadata.get(
                "page",
                "Unknown"
            )

            context_parts.append(
                f"""
SOURCE {i + 1}

Document: {source}

Page: {page}

Content:

{doc.page_content}
"""
            )


        context = "\n".join(context_parts)


        # -------------------------------------------------
        # PROMPT GEMINI
        # -------------------------------------------------

        prompt = f"""
You are VIDHI, an AI assistant specialized in
Indian Standards and BIS documents.

Your job is to answer the user's question ONLY using
the evidence provided below.

IMPORTANT RULES:

1. Do not invent information.

2. Do not use general knowledge if the answer is not
   present in the provided BIS evidence.

3. If the evidence does not contain enough information,
   clearly say:

   "I could not find sufficient information in the
   provided BIS documents."

4. Give a clear and concise answer.

5. When possible, mention the relevant document and page.

6. Do not claim that a requirement exists unless the
   retrieved evidence supports it.

USER QUESTION:

{query}

BIS DOCUMENT EVIDENCE:

{context}

Now answer the user's question using ONLY the
BIS document evidence above.
"""


        # -------------------------------------------------
        # GENERATE ANSWER
        # -------------------------------------------------

        with st.spinner("Generating VIDHI answer..."):

            response = llm.invoke(prompt)


        # -------------------------------------------------
        # DISPLAY ANSWER
        # -------------------------------------------------

        st.subheader("VIDHI Answer")

        answer = extract_answer(response)

        st.markdown(answer)


        # -------------------------------------------------
        # DISPLAY SOURCES
        # -------------------------------------------------

        st.subheader("📚 Sources Used")

        if docs:

            for i, doc in enumerate(docs):

                source = doc.metadata.get(
                    "source",
                    "Unknown document"
                )

                page = doc.metadata.get(
                    "page",
                    "Unknown"
                )

                with st.expander(
                    f"Source {i + 1}: {source} — Page {page}"
                ):

                    st.write(doc.page_content)