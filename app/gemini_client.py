from typing import Optional
from google import genai
from app.config import get_gemini_api_key


def get_gemini_client() -> Optional[genai.Client]:
    """
    Initialize and return the official Google GenAI client if an API key is configured.
    Returns None cleanly if GEMINI_API_KEY is missing or empty.
    """
    api_key = get_gemini_api_key()
    if not api_key:
        return None

    return genai.Client(api_key=api_key)
