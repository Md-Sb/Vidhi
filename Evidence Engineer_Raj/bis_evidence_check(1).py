# bis_evidence_check.py
# Evidence threshold logic for the BIS chatbot (VIDHI)
# Written by: [Your Name] - Evidence Engineer (M4)
#
# Goal (from team lead's brief):
#   - Every answer must show standard/clause/page when available
#   - Never invent a citation
#   - If retrieved evidence is too weak, refuse to answer confidently

# --- Setting: how relevant a match needs to be before we trust it ---
# I picked 0.6 as a starting point (mid-range) - can be tuned after
# we test with real BIS questions and see how it performs.
MIN_RELEVANCE = 0.6


def is_evidence_strong_enough(chunks):
    """
    Beginner-friendly relevance check.
    We just look at the single best match among all retrieved chunks
    and compare it against our minimum bar.
    """
    if len(chunks) == 0:
        return False

    top_score = 0
    for chunk in chunks:
        if chunk["score"] > top_score:
            top_score = chunk["score"]

    return top_score >= MIN_RELEVANCE


def build_citation(chunk):
    """
    Turns chunk metadata into a readable citation.
    If something's missing, we say so plainly - we never guess a
    standard number or page just to fill the gap.
    """
    if "standard" not in chunk or "clause" not in chunk or "page" not in chunk:
        return "Citation not available for this answer"

    return "Standard: " + chunk["standard"] + " | Clause: " + chunk["clause"] + " | Page: " + str(chunk["page"])


def answer_question(question, chunks, ask_llm):
    """
    Main function. 'ask_llm' is whatever function the team wires up
    to actually call the language model - kept separate here so this
    file can be tested on its own before that part is ready.
    """

    # Rule 1: block the answer early if nothing meets our bar
    if not is_evidence_strong_enough(chunks):
        return {
            "answer": "Insufficient evidence to confidently answer this question. "
                      "This may not be covered in the documents we have indexed.",
            "citation": "N/A"
        }

    # Rule 2: find the strongest matching chunk to answer from
    best_match = chunks[0]
    for chunk in chunks:
        if chunk["score"] > best_match["score"]:
            best_match = chunk

    # Rule 3: force the LLM to stick to this text only
    instructions = (
        "Using only the passage below, answer the question in simple language. "
        "If the passage does not actually answer it, say you're not sure.\n"
        "Passage: " + best_match["text"] + "\n"
        "Question: " + question
    )

    generated_answer = ask_llm(instructions)
    citation_text = build_citation(best_match)

    return {
        "answer": generated_answer,
        "citation": citation_text
    }


# --- quick manual test, so you can see it work before wiring up the real LLM ---
if __name__ == "__main__":

    def dummy_llm(instructions):
        return "The product must pass an insulation resistance test before certification."

    sample_chunks = [
        {"text": "Insulation resistance testing is required for LED products.",
         "score": 0.71, "standard": "IS 10322", "clause": "4.2", "page": 12},
        {"text": "Packaging labeling guidance for electronics.",
         "score": 0.33, "standard": "IS 9000", "clause": "1.4", "page": 3},
    ]

    print("Test with good evidence:")
    print(answer_question("What test is required for LED product certification?", sample_chunks, dummy_llm))

    weak_chunks = [
        {"text": "Unrelated packaging clause.", "score": 0.28, "standard": "IS 9000", "clause": "1.4", "page": 3},
    ]

    print("\nTest with weak evidence:")
    print(answer_question("What test is required for LED product certification?", weak_chunks, dummy_llm))
