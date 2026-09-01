import logging
import time

# Configure logging (in a real setup, move this to your app's entry point)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("vidhi")


def _safe_call(func, *args, retries=2, delay=1, step_name="step", **kwargs):
    """
    Calls a function with retry logic and logging.
    Raises the last exception if all retries fail.
    """
    last_exception = None
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"[{step_name}] attempt {attempt}/{retries}")
            return func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            logger.warning(f"[{step_name}] failed on attempt {attempt}: {e}")
            if attempt < retries:
                time.sleep(delay)
    logger.error(f"[{step_name}] all {retries} attempts failed")
    raise last_exception


def ask_vidi(query):
    """
    Orchestrates the VIDHI pipeline:
    Ask -> Retrieve -> Generate -> Validate -> Structured cited answer

    Assumes:
      retrieve(query) -> list of dicts, e.g.
          [{"standard": "IS 732:2019", "clause": "5.2.1",
            "page": 34, "text": "..."}, ...]
      generate_answer(query, context) -> str
      validate_evidence(answer, evidence) -> dict, e.g.
          {"is_supported": True, "confidence": 0.87}
    """

    if not query or not query.strip():
        logger.warning("Empty query received")
        return _empty_response("Please enter a question about a BIS standard.")

    # Step 1: Retrieve relevant clauses/passages
    try:
        evidence = _safe_call(retrieve, query, step_name="retrieve")
    except Exception as e:
        logger.error(f"Retrieval failed permanently: {e}")
        return _empty_response(
            "Sorry, I couldn't search the standards database right now. Please try again."
        )

    if not evidence:
        logger.info("No evidence found for query")
        return _empty_response(
            "No relevant BIS standard or clause could be found for this query."
        )

    # Step 2: Generate answer grounded ONLY in retrieved context
    try:
        answer = _safe_call(generate_answer, query, evidence, step_name="generate_answer")
    except Exception as e:
        logger.error(f"Answer generation failed permanently: {e}")
        return _empty_response(
            "Sorry, I couldn't generate an answer right now. Please try again.",
            evidence=evidence
        )

    # Step 3: Validate the answer against the retrieved evidence
    try:
        validation = _safe_call(
            validate_evidence, answer, evidence, step_name="validate_evidence", retries=1
        )
    except Exception as e:
        logger.error(f"Validation failed permanently: {e}")
        # Fail safe: don't show an unvalidated answer as confident/definitive
        return _empty_response(
            "The answer could not be verified against the standard. Please try rephrasing your query.",
            evidence=evidence
        )

    if not validation.get("is_supported", False):
        logger.info("Answer not supported by evidence; returning fallback")
        return {
            "answer": "The retrieved evidence does not sufficiently support a definitive answer. Please rephrase your query or consult the official standard directly.",
            "standard": None,
            "clause": None,
            "page": None,
            "evidence": evidence,
            "confidence": validation.get("confidence", 0.0)
        }

    # Step 4: Build final structured, cited response
    top_evidence = evidence[0]
    logger.info("Query answered successfully")

    return {
        "answer": answer,
        "standard": top_evidence.get("standard"),
        "clause": top_evidence.get("clause"),
        "page": top_evidence.get("page"),
        "evidence": evidence,
        "confidence": validation.get("confidence", 0.0)
    }


def _empty_response(message, evidence=None):
    """Helper to build a consistent fallback response shape."""
    return {
        "answer": message,
        "standard": None,
        "clause": None,
        "page": None,
        "evidence": evidence or [],
        "confidence": 0.0
    }
