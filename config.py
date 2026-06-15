import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")


def _setting(name: str, default: str = "") -> str:
    """Read config from env (.env locally) or Streamlit Cloud secrets."""
    value = os.environ.get(name)
    if value:
        return value
    try:
        import streamlit as st

        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass
    return default


OPENROUTER_API_KEY = _setting("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL = _setting("OPENROUTER_MODEL", "openai/gpt-4o-mini")

DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "sessions.db"
COUNTRY_RULES_PATH = DATA_DIR / "country_rules.json"
