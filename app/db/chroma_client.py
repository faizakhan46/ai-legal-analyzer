import chromadb
from app.config import CHROMA_DIR, COLLECTION_NAME

client = chromadb.PersistentClient(path=CHROMA_DIR)

def get_or_create_collection(name: str = COLLECTION_NAME):
    try:
        return client.get_collection(name)
    except Exception:
        return client.create_collection(name=name)