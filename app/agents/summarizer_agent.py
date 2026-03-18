from app.services.document_loader import load_document
from app.rag.prompt_templates import LEGAL_SUMMARY_SYSTEM_PROMPT
from app.services.llm_service import chat_completion

def summarize_document(file_path: str) -> str:
    pages = load_document(file_path)
    document_text = "\n\n".join([f"[Page {p['page']}]\n{p['text']}" for p in pages])

    user_prompt = f"""
Summarize this legal document:

{document_text}
"""

    return chat_completion(
        system_prompt=LEGAL_SUMMARY_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.0
    )