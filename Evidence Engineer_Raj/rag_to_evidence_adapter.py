"""
rag_to_evidence_adapter.py
============================
Bridges M3 (RAG Retrieval) and M4 (Evidence Engine).

Problem this solves:
    M3's retrieve() returns chunks shaped like:
        {"similarity_score": ..., "standard_number": ..., "edition": ...,
         "clause": ..., "page": ..., "text": ..., "status": ...}

    M4's evidence engine expects chunks shaped like:
        {"score": ..., "standard": ..., "clause": ..., "page": ...,
         "text": ..., "edition": ..., "status": ...}

    Without this adapter, feeding M3's output straight into M4 either
    crashes (bis_evidence_check.py, KeyError on "score") or silently
    fails (evidence_engine_v2.py, .get("score", 0) defaults every
    chunk to 0 -> engine always says "insufficient evidence").

Use it like this:
    from rag_to_evidence_adapter import adapt_for_evidence_engine

    m3_results = retrieve(query, top_k=5)                # from M3
    engine_input = adapt_for_evidence_engine(m3_results)  # translate
    result = engine.generate_answer(query, engine_input, ask_llm)  # M4
"""

from typing import List, Dict, Any


def adapt_for_evidence_engine(m3_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Translate a list of chunks from M3's retrieve() schema into the
    schema M4's evidence engine (v1 or v2) expects.

    Uses .get(...) with sensible defaults rather than direct ["..."]
    indexing, so this still works (rather than crashing) even if M3's
    output is missing a field -- e.g. if an older version of retrieve()
    without the "status" field is used.
    """
    adapted = []
    for chunk in m3_results:
        adapted.append({
            "text": chunk.get("text", ""),
            # M3 calls this "similarity_score"; M4 calls it "score".
            "score": chunk.get("similarity_score", 0.0),
            # M3 calls this "standard_number"; M4 calls it "standard".
            "standard": chunk.get("standard_number", ""),
            "clause": chunk.get("clause", ""),
            "page": chunk.get("page", ""),
            "edition": chunk.get("edition", ""),
            # Pass "status" through unchanged -- this is what lets the
            # patched evidence engine warn about superseded/withdrawn
            # standards instead of citing them with full confidence.
            "status": chunk.get("status", "current"),
        })
    return adapted


# ---------------------------------------------------------------------------
# Quick self-test: confirms the translation is correct on its own,
# without needing the real embedding model or a live LLM.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    fake_m3_output = [
        {
            "similarity_score": 0.82,
            "standard_number": "IS 10322",
            "edition": "2023",
            "clause": "4.2",
            "page": 12,
            "text": "Insulation resistance testing is required for LED products.",
            "status": "current",
        },
        {
            "similarity_score": 0.41,
            "standard_number": "IS 10322",
            "edition": "1998",
            "clause": "4.2",
            "page": 9,
            "text": "Insulation testing under older classification rules.",
            "status": "superseded",
        },
    ]

    adapted_output = adapt_for_evidence_engine(fake_m3_output)

    print("Before adaptation (M3 schema):")
    for c in fake_m3_output:
        print(" ", c)

    print("\nAfter adaptation (M4 schema):")
    for c in adapted_output:
        print(" ", c)

    # Sanity checks -- these will raise AssertionError if the mapping is wrong
    assert adapted_output[0]["score"] == 0.82
    assert adapted_output[0]["standard"] == "IS 10322"
    assert adapted_output[1]["status"] == "superseded"
    print("\nAll checks passed.")
