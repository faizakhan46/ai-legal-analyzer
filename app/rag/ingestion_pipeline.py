import os
from app.services.document_loader import load_document
from app.services.text_splitter import split_pages_into_chunks
from app.services.embedding_service import generate_embeddings
from app.db.chroma_client import get_or_create_collection

def ingest_document(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    pages = load_document(file_path)
    chunks = split_pages_into_chunks(pages)

    if not chunks:
        raise ValueError("No readable text found in the document.")

    texts = [chunk["text"] for chunk in chunks]
    embeddings = generate_embeddings(texts)

    collection = get_or_create_collection()

    ids = []
    documents = []
    metadatas = []

    filename = os.path.basename(file_path)

    for i, chunk in enumerate(chunks):
        ids.append(f"{filename}_{chunk['page']}_{chunk['chunk_index']}_{i}")
        documents.append(chunk["text"])
        metadatas.append({
            "source": filename,
            "page": chunk["page"],
            "chunk_index": chunk["chunk_index"]
        })

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    return {
        "file": filename,
        "pages_loaded": len(pages),
        "chunks_created": len(chunks)
    }