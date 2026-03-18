from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="AI Legal Document Analyzer")
app.include_router(router, prefix="/api")