from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_pages_into_chunks(
    pages: List[Dict],
    chunk_size: int = 1200,
    chunk_overlap: int = 200
) -> List[Dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = []

    for page_data in pages:
        page_number = page_data["page"]
        page_text = page_data["text"]

        split_texts = splitter.split_text(page_text)

        for idx, chunk_text in enumerate(split_texts):
            chunks.append({
                "page": page_number,
                "chunk_index": idx,
                "text": chunk_text
            })

    return chunks