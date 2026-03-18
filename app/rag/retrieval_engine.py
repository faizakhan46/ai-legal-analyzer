from app.db.chroma_client import get_or_create_collection
from app.services.embedding_service import generate_query_embedding

def retrieve_relevant_documents(query: str, k: int = 5) -> list[dict]:
    collection = get_or_create_collection()
    query_embedding = generate_query_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    output = []
    for doc, meta in zip(documents, metadatas):
        output.append({
            "document": doc,
            "metadata": meta
        })

    return output