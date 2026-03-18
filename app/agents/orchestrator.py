from app.rag.prompt_templates import ORCHESTRATOR_SYSTEM_PROMPT
from app.services.llm_service import chat_completion
from app.agents.rag_agent import answer_legal_question
from app.agents.summarizer_agent import summarize_document
from app.agents.comparison_agent import compare_contracts

def classify_intent(query: str) -> str:
    result = chat_completion(
        system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
        user_prompt=query,
        temperature=0.0
    ).lower().strip()

    if result not in {"qa", "summarize", "compare"}:
        return "qa"
    return result

def handle_query(query: str, files: list[str] | None = None) -> str:
    intent = classify_intent(query)

    if intent == "compare":
        if not files or len(files) != 2:
            return "Please provide exactly two documents for comparison."
        return compare_contracts(files[0], files[1])

    if intent == "summarize":
        if not files or len(files) != 1:
            return "Please provide one document for summarization."
        return summarize_document(files[0])

    return answer_legal_question(query)