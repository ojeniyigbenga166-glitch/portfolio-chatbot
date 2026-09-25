import os
from pathlib import Path
from dotenv import load_dotenv

# Determine project base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env if present
env_file = BASE_DIR / ".env"
if env_file.exists():
    load_dotenv(dotenv_path=env_file, override=True)

# Expose configuration safely
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()


def get_gemini_api_key() -> str:
    """Return the current GEMINI_API_KEY environment variable."""
    return os.getenv("GEMINI_API_KEY", "").strip()
