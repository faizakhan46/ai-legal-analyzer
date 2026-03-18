from app.rag.retrieval_engine import retrieve_relevant_documents
from app.rag.prompt_templates import LEGAL_QA_SYSTEM_PROMPT
from app.services.llm_service import chat_completion

def answer_legal_question(query: str, top_k: int = 5) -> str:
    retrieved_docs = retrieve_relevant_documents(query, k=top_k)

    if not retrieved_docs:
        return "I could not find that in the uploaded document."

    context_parts = []
    for item in retrieved_docs:
        page = item["metadata"].get("page", "N/A")
        source = item["metadata"].get("source", "Unknown")
        context_parts.append(
            f"[Source: {source}, Page: {page}]\n{item['document']}"
        )

    context = "\n\n".join(context_parts)

    user_prompt = f"""
Contract context:
{context}

Question:
{query}

Answer using only the contract context.
"""

    return chat_completion(
        system_prompt=LEGAL_QA_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.0
    )