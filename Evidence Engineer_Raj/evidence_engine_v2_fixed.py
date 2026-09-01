# evidence_engine_v2_fixed.py
# M4 - Evidence Engineer logic (VIDHI / BIS BUDDYS)
#
# This is v2 with two fixes layered on top:
#
#   FIX 1 (compatibility): expects chunks in the schema produced by
#   rag_to_evidence_adapter.py -- i.e. "score" / "standard" (not M3's
#   raw "similarity_score" / "standard_number"). Run M3's output
#   through the adapter before calling this engine.
#
#   FIX 2 (correctness bug): format_citation() used to check
#   "if not page", which incorrectly treats page 0 as missing.
#   Now checks "is None" instead, so page 0 is treated as valid.
#
#   NEW (domain requirement): a standard's "status" field is now
#   used, not just displayed. If the best-matching chunk is
#   "superseded" or "withdrawn", the engine will not report high
#   confidence even if the similarity score is high, and both the
#   citation and the answer text carry an explicit warning. This
#   directly supports the brief's rule: never present outdated
#   guidance as if it were current.


class EvidenceEngine:

    def __init__(self, high_threshold=0.75, low_threshold=0.45):
        # Two cutoffs instead of one:
        #   score >= high_threshold        -> confident, answer directly
        #   low_threshold <= score < high  -> answer, but flag it as unverified
        #   score < low_threshold          -> refuse to answer
        self.high_threshold = high_threshold
        self.low_threshold = low_threshold

    def _confidence_score(self, retrieved_chunks):
        """
        Uses the average of the top 2 chunk scores (not just the single best one).
        Reasoning: if only one chunk matches well and everything else is weak,
        that's a shakier signal than two chunks agreeing on relevance.
        Falls back to a single score if only one chunk was retrieved.
        """
        if not retrieved_chunks:
            return 0.0

        scores = sorted((c.get("score", 0) for c in retrieved_chunks), reverse=True)
        top_scores = scores[:2]
        return sum(top_scores) / len(top_scores)

    def _confidence_level(self, score):
        if score >= self.high_threshold:
            return "high"
        elif score >= self.low_threshold:
            return "medium"
        else:
            return "low"

    def format_citation(self, chunk):
        """
        Builds a citation string, including edition year if present.
        Never fabricates a missing field - says so explicitly instead.

        FIX: checks "is None" / "" rather than plain truthiness, so a
        legitimate page number of 0 is not mistaken for a missing field.
        """
        standard = chunk.get("standard")
        clause = chunk.get("clause")
        page = chunk.get("page")
        edition = chunk.get("edition")
        status = chunk.get("status", "current")

        missing = (
            standard in (None, "")
            or clause in (None, "")
            or page is None
        )
        if missing:
            return "Citation unavailable (missing metadata)"

        citation = f"{standard}, Clause {clause}, Page {page}"
        if edition:
            citation += f" ({edition} edition)"

        # NEW: make outdated status impossible to miss in the citation itself.
        if status == "superseded":
            citation += " -- WARNING: this standard has been superseded, verify against the current edition"
        elif status == "withdrawn":
            citation += " -- WARNING: this standard has been withdrawn, do not rely on it"

        return citation

    def generate_answer(self, question, retrieved_chunks, llm_call_function):
        confidence_score = self._confidence_score(retrieved_chunks)
        level = self._confidence_level(confidence_score)

        best_chunk = max(retrieved_chunks, key=lambda c: c.get("score", 0)) if retrieved_chunks else None
        best_status = best_chunk.get("status", "current") if best_chunk else "current"

        # NEW: a high similarity score on an outdated standard is not the
        # same thing as a high-confidence current answer. Cap the level
        # at "medium" so it always gets the verify-this treatment below,
        # even if the raw score alone would have counted as "high".
        if best_status in ("superseded", "withdrawn") and level == "high":
            level = "medium"

        # Debug info kept regardless of outcome - useful when tuning thresholds later
        debug_info = {
            "confidence_score": round(confidence_score, 2),
            "level": level,
            "best_chunk_status": best_status,
        }

        if level == "low" or not retrieved_chunks:
            return {
                "answer": "Insufficient evidence to answer this question confidently. "
                          "Please rephrase, or this may not be covered in our current documents.",
                "citation": None,
                "debug": debug_info
            }

        prompt = (
            "Answer the question using ONLY the text below. "
            "Do not add outside information. "
            "If the text does not contain the answer, say you are unsure.\n\n"
            f"Text: {best_chunk['text']}\n\n"
            f"Question: {question}"
        )

        llm_answer = llm_call_function(prompt)
        citation = self.format_citation(best_chunk)

        # Flag medium-confidence answers so the user knows to double check.
        # A superseded/withdrawn chunk always gets this treatment too,
        # since it was force-downgraded to "medium" above.
        if level == "medium":
            if best_status == "superseded":
                prefix = "(Please verify -- this cites a superseded standard) "
            elif best_status == "withdrawn":
                prefix = "(Please verify -- this cites a withdrawn standard) "
            else:
                prefix = "(Please verify -- moderate confidence match) "
            llm_answer = prefix + llm_answer

        return {
            "answer": llm_answer,
            "citation": citation,
            "debug": debug_info
        }


# ---------------------------------------------------------
# Example usage / quick test
# ---------------------------------------------------------

if __name__ == "__main__":

    def fake_llm(prompt):
        return "LED bulbs must meet insulation and safety requirements under this clause."

    engine = EvidenceEngine()

    # Case 1: high confidence, current standard, full metadata
    chunks_high = [
        {"text": "LED bulbs must meet insulation resistance requirements.",
         "score": 0.85, "standard": "IS 10322", "clause": "4.2", "page": 12, "edition": 2023, "status": "current"},
        {"text": "Insulation testing procedure for lighting products.",
         "score": 0.78, "standard": "IS 10322", "clause": "4.3", "page": 13, "edition": 2023, "status": "current"},
    ]
    print("Case 1 (high confidence, current standard):")
    print(engine.generate_answer("What is the safety standard for LED bulbs?", chunks_high, fake_llm))
    print()

    # Case 2: medium confidence
    chunks_medium = [
        {"text": "General lighting product safety notes.",
         "score": 0.55, "standard": "IS 10322", "clause": "3.1", "page": 8, "edition": 2019, "status": "current"},
        {"text": "Related electrical fitting guidance.",
         "score": 0.50, "standard": "IS 10322", "clause": "3.2", "page": 9, "edition": 2019, "status": "current"},
    ]
    print("Case 2 (medium confidence):")
    print(engine.generate_answer("What is the safety standard for LED bulbs?", chunks_medium, fake_llm))
    print()

    # Case 3: low confidence -> should refuse
    chunks_low = [
        {"text": "Unrelated clause about packaging.",
         "score": 0.30, "standard": "IS 999", "clause": "2.1", "page": 5, "edition": 2020, "status": "current"},
    ]
    print("Case 3 (low confidence):")
    print(engine.generate_answer("What is the safety standard for LED bulbs?", chunks_low, fake_llm))
    print()

    # Case 4: high score but missing metadata -> citation should say so
    chunks_missing = [
        {"text": "LED bulbs must meet insulation resistance requirements.",
         "score": 0.80, "standard": "IS 10322", "clause": None, "page": 12, "edition": 2023, "status": "current"},
        {"text": "Insulation testing procedure.",
         "score": 0.77, "standard": "IS 10322", "clause": "4.3", "page": 13, "edition": 2023, "status": "current"},
    ]
    print("Case 4 (missing metadata):")
    print(engine.generate_answer("What is the safety standard for LED bulbs?", chunks_missing, fake_llm))
    print()

    # Case 5: NEW -- high similarity score but the standard is superseded.
    # Should NOT be reported as high confidence, and should carry a warning.
    chunks_superseded = [
        {"text": "Insulation testing under older classification rules.",
         "score": 0.88, "standard": "IS 10322", "clause": "4.2", "page": 9, "edition": 1998, "status": "superseded"},
    ]
    print("Case 5 (high score, but superseded standard):")
    print(engine.generate_answer("What is the safety standard for LED bulbs?", chunks_superseded, fake_llm))
    print()

    # Case 6: NEW -- page number is legitimately 0. Citation should still work.
    chunks_page_zero = [
        {"text": "Cover page notes on scope.",
         "score": 0.80, "standard": "IS 10322", "clause": "0.1", "page": 0, "edition": 2023, "status": "current"},
    ]
    print("Case 6 (page 0, should NOT say citation unavailable):")
    print(engine.generate_answer("What is the safety standard for LED bulbs?", chunks_page_zero, fake_llm))
