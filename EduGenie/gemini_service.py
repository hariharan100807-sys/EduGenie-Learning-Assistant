import json
from typing import Type, TypeVar

from pydantic import BaseModel

from config import settings

T = TypeVar("T", bound=BaseModel)

_client = None


def get_client():
    global _client
    if _client is None:
        if not settings.gemini_api_key:
            return None
        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError(
                "The google-genai package is not installed. Run: pip install -r requirements.txt"
            ) from exc
        _client = genai.Client(api_key=settings.gemini_api_key)
    return _client


def generate_text(prompt: str) -> str:
    client = get_client()
    if client is None:
        return ""

    from google.genai import types

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.4,
            max_output_tokens=2048,
        ),
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()


def generate_structured(prompt: str, schema: Type[T]) -> T:
    from google.genai import types

    client = get_client()
    if client is None:
        raise RuntimeError("Gemini API key is not configured.")

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=3000,
            response_mime_type="application/json",
            response_schema=schema,
        ),
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty structured response.")
    try:
        return schema.model_validate(json.loads(text))
    except Exception as exc:
        raise RuntimeError(f"Could not parse Gemini JSON response: {exc}") from exc
