from langchain_openai import OpenAIEmbeddings
from app.config import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL

def get_embedding_model():
    clean_key = OPENAI_API_KEY.splitlines()[0].strip()

    return OpenAIEmbeddings(
        model=OPENAI_EMBEDDING_MODEL,
        api_key=clean_key
    )

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    embedding_model = get_embedding_model()
    return embedding_model.embed_documents(texts)

def generate_query_embedding(text: str) -> list[float]:
    embedding_model = get_embedding_model()
    return embedding_model.embed_query(text)