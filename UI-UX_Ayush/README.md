# VIDI — AI Assistant for Indian Standards
### Smart India Hackathon 2026 Prototype

---

## Overview

**VIDI** is an AI-powered knowledge assistant designed to help industries, manufacturers,
engineers, quality-control teams, consumers, and other stakeholders understand and navigate
**Indian Standards (IS)** and **BIS (Bureau of Indian Standards)** documentation.

The interface emphasises:
- Evidence-backed answers with clause-level citations
- Transparent reasoning ("Why am I seeing this answer?")
- Role-aware explanations
- Professional, government/enterprise-grade aesthetics

---

## Quick Start

```bash
# 1. Clone or navigate to the project directory
cd "Vidhi UI"

# 2. (Recommended) Create a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## Project Structure

```
Vidhi UI/
│
├── app.py            ← Main Streamlit application (entry point)
├── styles.py         ← All custom CSS (injected via st.markdown)
├── components.py     ← Reusable UI rendering functions
├── mock_data.py      ← Demo data and mock AI responses
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```

---

## Features

| Feature | Description |
|---|---|
| **Role Selector** | Adapts explanations for Manufacturer, Engineer, QC Professional, Consumer, etc. |
| **Query Pipeline** | Animated processing steps: Understanding → Searching → Verifying → Answering |
| **Answer Card** | Markdown-formatted answer with evidence badge |
| **Confidence Indicator** | Visual progress bar with High / Moderate / Low states |
| **Standard Card** | Applicable IS standard with metadata |
| **Evidence Card** | Clause number, page number, verbatim snippet, relevance score |
| **Transparency Panel** | "Why am I seeing this?" — shows the evidence chain |
| **Insufficient Evidence** | Warning card with suggestions when confidence < 70% |
| **Standards Explorer** | Searchable, filterable library of 10 sample standards |
| **Dashboard** | Mock metrics and activity overview |
| **Demo Mode** | Predefined realistic responses without a backend |
| **Right Context Panel** | Shows role, topic, source count, confidence at a glance |
| **Chat History Sidebar** | Recent queries list with clear history |

---

## Demo Queries

The following queries return rich mock responses (Demo Mode must be ON):

| Query | Standard | Confidence |
|---|---|---|
| *What are the requirements for Portland cement under IS 269?* | IS 269:2015 | 92% High |
| *Which Indian Standard applies to electrical safety testing?* | IS 13252:2010 | 88% High |
| *What does IS 456 Clause 5.2 require for concrete?* | IS 456:2000 | 95% High |
| *Explain the BIS certification process for electronics.* | BIS Act 2016 | 90% High |
| *What are the labelling requirements for packaged drinking water?* | IS 14772:2000 | 94% High |
| Any query containing *"insufficient"* or *"test low"* | — | 48% Low (warning demo) |

---

## Connecting a Real AI Backend

All mock logic is isolated in **`mock_data.py`** → `get_demo_response()`.

### Step 1 — Replace `get_demo_response()`

Open `mock_data.py` and replace the function body:

```python
def get_demo_response(query: str, role: str) -> dict:
    # REPLACE THIS with your actual backend call:
    from your_backend import rag_pipeline
    raw = rag_pipeline.query(query, user_role=role)
    return {
        "answer":           raw.answer_text,
        "confidence":       raw.confidence_score,        # int 0–100
        "confidence_label": raw.confidence_label,        # e.g. "High Confidence"
        "standard": {
            "id":       raw.standard_id,
            "title":    raw.standard_title,
            "category": raw.standard_category,
            "year":     raw.standard_year,
            "relevance": raw.relevance_label,
            "source":   "BIS Standards Database",
        },
        "evidence": [
            {
                "clause":          ev.clause,
                "page":            ev.page_number,
                "snippet":         ev.text_snippet,
                "standard":        ev.standard_id,
                "relevance_score": ev.relevance_score,
            }
            for ev in raw.evidence_list
        ],
        "related_standards": raw.related_standard_ids,
        "topic":             raw.detected_topic,
        "sources_count":     len(raw.evidence_list),
    }
```

### Step 2 — Update `app.py`

In `app.py`, find the comment block labelled **`REAL BACKEND HOOK`** and uncomment your
import and call.

### Step 3 — Disable Demo Mode

Set the default in `init_session_state()`:
```python
"demo_mode": False,
```

---

## Suggested RAG Stack

| Component | Recommended Tool |
|---|---|
| Document ingestion | LlamaIndex / LangChain |
| Vector store | FAISS / Chroma / Pinecone |
| Embeddings | OpenAI `text-embedding-3-small` or `sentence-transformers` |
| LLM | GPT-4o / Gemini 1.5 Pro / Claude 3.5 |
| Chunking | Clause-aware PDF chunking (PyMuPDF + regex) |
| Reranking | Cohere Rerank / FlashRank |

---

## Design System

| Token | Value |
|---|---|
| Primary navy | `#0d1b2a` |
| Industrial blue | `#1d6fa4` |
| Light blue accent | `#2589c9` |
| Background white | `#ffffff` |
| Surface gray | `#f9fafb` |
| Border | `#e5e7eb` |
| Verified green | `#16a34a` |
| Warning amber | `#d97706` |
| Border radius | 8–16 px |
| Font | Inter (Google Fonts) |

---

## Disclaimer

> This is a **hackathon prototype** for SIH 2026.
> All responses are mock/demo data and do **not** constitute official BIS advice.
> VIDI does not claim to reproduce or redistribute BIS copyrighted standards.

---

*Built for Smart India Hackathon 2026 — AI Track*
