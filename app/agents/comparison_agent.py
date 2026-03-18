from app.services.document_loader import load_document
from app.rag.prompt_templates import LEGAL_COMPARISON_SYSTEM_PROMPT
from app.services.llm_service import chat_completion

def compare_contracts(file_path1: str, file_path2: str) -> str:
    pages1 = load_document(file_path1)
    pages2 = load_document(file_path2)

    doc1 = "\n\n".join([f"[Page {p['page']}]\n{p['text']}" for p in pages1])
    doc2 = "\n\n".join([f"[Page {p['page']}]\n{p['text']}" for p in pages2])

    user_prompt = f"""
Contract A:
{doc1}

Contract B:
{doc2}

Compare both contracts.
"""

    return chat_completion(
        system_prompt=LEGAL_COMPARISON_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.0
    )