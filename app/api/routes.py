import os
import shutil
import traceback
from typing import Annotated, List, Optional

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse

from app.rag.ingestion_pipeline import ingest_document
from app.agents.rag_agent import answer_legal_question
from app.agents.summarizer_agent import summarize_document
from app.agents.comparison_agent import compare_contracts
from app.agents.orchestrator import handle_query

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_upload_file(upload_file: UploadFile) -> str:
    file_path = os.path.join(UPLOAD_DIR, upload_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path


@router.post("/upload-documents")
async def upload_documents(
    files: Annotated[List[UploadFile], File(...)]
):
    try:
        results = []

        for file in files:
            file_path = save_upload_file(file)
            ingest_result = ingest_document(file_path)
            results.append(ingest_result)

        return JSONResponse({
            "status": "success",
            "ingested_files": results
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )


@router.post("/ask-question")
async def ask_question(query: str = Form(...)):
    try:
        answer = answer_legal_question(query)
        return JSONResponse({
            "query": query,
            "answer": answer
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )


@router.post("/summarize-document")
async def summarize_uploaded_document(
    file: Annotated[UploadFile, File(...)]
):
    try:
        file_path = save_upload_file(file)
        summary = summarize_document(file_path)

        return JSONResponse({
            "file": file.filename,
            "summary": summary
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )


@router.post("/compare-documents")
async def compare_uploaded_documents(
    file1: Annotated[UploadFile, File(...)],
    file2: Annotated[UploadFile, File(...)]
):
    try:
        file_path1 = save_upload_file(file1)
        file_path2 = save_upload_file(file2)

        comparison = compare_contracts(file_path1, file_path2)

        return JSONResponse({
            "file1": file1.filename,
            "file2": file2.filename,
            "comparison": comparison
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )


@router.post("/orchestrate")
async def orchestrate_query(
    query: str = Form(...),
    files: Optional[List[UploadFile]] = File(default=None)
):
    try:
        saved_paths = []

        if files:
            for file in files:
                saved_paths.append(save_upload_file(file))

        result = handle_query(
            query=query,
            files=saved_paths if saved_paths else None
        )

        return JSONResponse({
            "query": query,
            "result": result
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )