"""Optional local LaMini-Flan-T5 explanation provider.

Install requirements-local.txt before selecting EXPLANATION_PROVIDER=local.
The model weights are downloaded by Hugging Face on first use.
"""

MODEL_NAME = "MBZUAI/LaMini-Flan-T5-783M"
_pipe = None


def explain_with_lamini(topic: str) -> str:
    global _pipe
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local explanation requires transformers/torch. Install requirements-local.txt."
        ) from exc

    if _pipe is None:
        _pipe = pipeline("text2text-generation", model=MODEL_NAME)

    prompt = (
        "Explain this educational topic for a beginner. Use simple language, one example, "
        "and two key points. Topic: " + topic
    )
    result = _pipe(prompt, max_new_tokens=220, do_sample=False)
    return result[0]["generated_text"].strip()
