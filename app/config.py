import os
from dotenv import dotenv_values

env_data = dotenv_values(".env")

def clean_env_value(value: str) -> str:
    if not value:
        return ""
    return str(value).splitlines()[0].strip()

OPENAI_API_KEY = clean_env_value(
    env_data.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY", "")
)

OPENAI_CHAT_MODEL = clean_env_value(
    env_data.get("OPENAI_CHAT_MODEL") or os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
)

OPENAI_EMBEDDING_MODEL = clean_env_value(
    env_data.get("OPENAI_EMBEDDING_MODEL") or os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
)

CHROMA_DIR = clean_env_value(
    env_data.get("CHROMA_DIR") or os.getenv("CHROMA_DIR", "chroma_storage")
)

COLLECTION_NAME = clean_env_value(
    env_data.get("COLLECTION_NAME") or os.getenv("COLLECTION_NAME", "legal_docs")
)

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing.")