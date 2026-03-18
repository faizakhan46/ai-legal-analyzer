import os
from typing import List, Dict
from PyPDF2 import PdfReader
from docx import Document

def load_pdf(file_path: str) -> List[Dict]:
    pages_data = []
    reader = PdfReader(file_path)

    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():
            pages_data.append({
                "page": i + 1,
                "text": text
            })

    return pages_data

def load_docx(file_path: str) -> List[Dict]:
    doc = Document(file_path)
    full_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    return [{
        "page": 1,
        "text": full_text
    }]

def load_document(file_path: str) -> List[Dict]:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return load_pdf(file_path)
    if ext == ".docx":
        return load_docx(file_path)

    raise ValueError(f"Unsupported file type: {ext}")