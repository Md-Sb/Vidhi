# evidence_engine_v2.py
# M4 - Evidence Engineer logic (VIDHI / BIS BUDDYS)
#
# Improvements over v1:
#   - Two thresholds instead of one (HIGH / LOW) -> a "medium confidence" tier
#   - Confidence is based on the average of the top 2 chunks, not just the best one
#     (more robust: rewards multiple supporting chunks, not a single lucky match)
#   - Citations include edition year when available
#   - Blocked/uncertain answers still log the actual score, for debugging/tuning later
#
# Structured as a class instead of loose functions, so all the settings
# (thresholds) live together and are easy to tune in one place.


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
        """
        standard = chunk.get("standard")
        clause = chunk.get("clause")
        page = chunk.get("page")
        edition = chunk.get("edition")

        if not standard or not clause or not page:
            return "Citation unavailable (missing metadata)"

        citation = f"{standard}, Clause {clause}, Page {page}"
        if edition:
            citation += f" ({edition} edition)"
        return citation

    def generate_answer(self, question, retrieved_chunks, llm_call_function):
        confidence_score = self._confidence_score(retrieved_chunks)
        level = self._confidence_level(confidence_score)

        # Debug info kept regardless of outcome - useful when tuning thresholds later
        debug_info = {"confidence_score": round(confidence_score, 2), "level": level}

        if level == "low" or not retrieved_chunks:
            return {
                "answer": "Insufficient evidence to answer this question confidently. "
                          "Please rephrase, or this may not be covered in our current documents.",
                "citation": None,
                "debug": debug_info
            }

        best_chunk = max(retrieved_chunks, key=lambda c: c.get("score", 0))

        prompt = (
            "Answer the question using ONLY the text below. "
            "Do not add outside information. "
            "If the text does not contain the answer, say you are unsure.\n\n"
            f"Text: {best_chunk['text']}\n\n"
            f"Question: {question}"
        )

        llm_answer = llm_call_function(prompt)
        citation = self.format_citation(best_chunk)

        # Flag medium-confidence answers so the user knows to double check
        if level == "medium":
            llm_answer = "(Please verify — moderate confidence match) " + llm_answer

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

    # Case 1: high confidence, full metadata
    chunks_high = [
        {"text": "LED bulbs must meet insulation resistance requirements.",
         "score": 0.85, "standard": "IS 10322", "clause": "4.2", "page": 12, "edition": 2023},
        {"text": "Insulation testing procedure for lighting products.",
         "score": 0.78, "standard": "IS 10322", "clause": "4.3", "page": 13, "edition": 2023},
    ]
    print("Case 1 (high confidence):")
    print(engine.generate_answer("What is the safety standard for LED bulbs?", chunks_high, fake_llm))
    print()

    # Case 2: medium confidence
    chunks_medium = [
        {"text": "General lighting product safety notes.",
         "score": 0.55, "standard": "IS 10322", "clause": "3.1", "page": 8, "edition": 2019},
        {"text": "Related electrical fitting guidance.",
         "score": 0.50, "standard": "IS 10322", "clause": "3.2", "page": 9, "edition": 2019},
    ]
    print("Case 2 (medium confidence):")
    print(engine.generate_answer("What is the safety standard for LED bulbs?", chunks_medium, fake_llm))
    print()

    # Case 3: low confidence -> should refuse
    chunks_low = [
        {"text": "Unrelated clause about packaging.",
         "score": 0.30, "standard": "IS 999", "clause": "2.1", "page": 5, "edition": 2020},
    ]
    print("Case 3 (low confidence):")
    print(engine.generate_answer("What is the safety standard for LED bulbs?", chunks_low, fake_llm))
    print()

    # Case 4: high score but missing metadata -> citation should say so
    chunks_missing = [
        {"text": "LED bulbs must meet insulation resistance requirements.",
         "score": 0.80, "standard": "IS 10322", "clause": None, "page": 12, "edition": 2023},
        {"text": "Insulation testing procedure.",
         "score": 0.77, "standard": "IS 10322", "clause": "4.3", "page": 13, "edition": 2023},
    ]
    print("Case 4 (missing metadata):")
    print(engine.generate_answer("What is the safety standard for LED bulbs?", chunks_missing, fake_llm))
