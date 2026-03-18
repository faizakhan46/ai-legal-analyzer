# ⚖️ AI Legal Document Analyzer

An advanced AI-powered legal-tech platform that enables users to upload contracts, extract insights, and interact with documents using natural language.

This system leverages **Retrieval-Augmented Generation (RAG)**, **LLMs**, and a **multi-agent orchestration architecture** to deliver accurate, context-aware legal analysis.

---

## 🚀 Key Features

* 📂 Upload and ingest legal documents (PDF/DOCX)
* 🔍 Context-aware legal Q&A using RAG
* 📝 Automated document summarization
* ⚖️ Contract comparison (multi-document reasoning)
* 🧠 Session-based chat history (memory)
* 🤖 Agent-based orchestration system
* 📊 Semantic search with vector embeddings (ChromaDB)

---

## 🏗️ Architecture

### Tech Stack

| Layer        | Technology               |
| ------------ | ------------------------ |
| Frontend     | Streamlit                |
| Backend      | FastAPI                  |
| LLM          | OpenAI (GPT-4o-mini)     |
| Embeddings   | OpenAI Embeddings        |
| Vector DB    | ChromaDB                 |
| Storage      | Local (extensible to S3) |
| Architecture | Multi-Agent + RAG        |

---

## 🧠 System Flow

1. User uploads document via UI
2. Backend extracts and chunks text
3. Embeddings are generated and stored in ChromaDB
4. User submits a query
5. Relevant chunks retrieved via similarity search
6. LLM generates contextual response

---

## 📁 Project Structure

```
ai-legal-analyzer/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   │
│   ├── agents/
│   │   ├── rag_agent.py
│   │   ├── summarizer_agent.py
│   │   ├── comparison_agent.py
│   │   └── orchestrator.py
│   │
│   ├── rag/
│   │   ├── ingestion_pipeline.py
│   │   └── retrieval_engine.py
│   │
│   ├── db/
│   │   └── chroma_client.py
│   │
│   ├── services/
│   │   ├── embedding_service.py
│   │   └── llm_service.py
│   │
│   ├── config.py
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── uploads/
├── chroma_storage/
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/ai-legal-analyzer.git
cd ai-legal-analyzer
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_openai_key
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
CHROMA_DIR=chroma_storage
COLLECTION_NAME=legal_docs
```

---

## ▶️ Run the Application

### Start Backend

```bash
uvicorn app.main:app --reload
```

### Start Frontend

```bash
streamlit run frontend/app.py
```
---

## 💡 Example Queries

* What is the termination clause in this contract?
* Summarize this agreement
* Compare liability clauses in both documents
* What are the payment terms?

---

## 🔒 Current Limitations

* In-memory chat history (not persistent)
* No authentication layer
* Local storage (no cloud deployment)

---

## 🚀 Future Enhancements

* Persistent database (PostgreSQL)
* User authentication & session management
* Clause-level highlighting
* Risk analysis scoring
* Exportable PDF reports
* Cloud deployment (AWS/GCP)

---

## 👩‍💻 Author

**Faiza Khan**
BCA Student | AI & Full Stack Enthusiast

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
