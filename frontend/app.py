import streamlit as st
import os
import tempfile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Legal Document Analyzer",
    page_icon="⚖️",
    layout="wide"
)

# ── API Key ───────────────────────────────────────────────────────────────────
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
if not OPENAI_API_KEY:
    st.error("⚠️ OPENAI_API_KEY not found. Please add it in Space Settings → Secrets.")
    st.stop()

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# ── Session state ─────────────────────────────────────────────────────────────
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "ingested_files" not in st.session_state:
    st.session_state.ingested_files = []

# ── Helpers ───────────────────────────────────────────────────────────────────
def load_document(uploaded_file):
    """Load PDF or DOCX into LangChain documents."""
    suffix = "." + uploaded_file.name.split(".")[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    if suffix == ".pdf":
        loader = PyPDFLoader(tmp_path)
    else:
        loader = Docx2txtLoader(tmp_path)
    docs = loader.load()
    os.unlink(tmp_path)
    return docs


def build_vectorstore(docs):
    """Chunk documents and store in in-memory Chroma."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(chunks, embeddings)
    return vectorstore


def get_qa_chain(vectorstore):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "You are an expert legal assistant. Use the context below to answer "
            "the legal question accurately and concisely.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        ),
    )
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
    )


def summarize_text(text: str) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = (
        "You are a legal expert. Provide a comprehensive summary of the following "
        "legal document. Highlight key clauses, obligations, rights, and any risks.\n\n"
        f"Document:\n{text[:8000]}\n\nSummary:"
    )
    return llm.invoke(prompt).content


def compare_texts(text1: str, text2: str) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = (
        "You are a legal expert. Compare the two contracts below. Identify key "
        "differences in clauses, obligations, rights, risks, and terms.\n\n"
        f"Contract 1:\n{text1[:4000]}\n\n"
        f"Contract 2:\n{text2[:4000]}\n\n"
        "Comparison:"
    )
    return llm.invoke(prompt).content

# ── UI ────────────────────────────────────────────────────────────────────────
st.title("⚖️ AI Legal Document Analyzer")
st.caption("Upload contracts · Ask questions · Summarize · Compare — powered by RAG + GPT-4o")

tab1, tab2, tab3, tab4 = st.tabs([
    "📂 Upload & Ingest",
    "❓ Ask Question",
    "📝 Summarize",
    "🔍 Compare Contracts",
])

# ── Tab 1: Upload ─────────────────────────────────────────────────────────────
with tab1:
    st.subheader("Upload and ingest legal documents")
    uploaded_files = st.file_uploader(
        "Choose PDF or DOCX files",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        key="ingest_files"
    )

    if st.button("📥 Upload & Ingest", type="primary"):
        if not uploaded_files:
            st.warning("Please select at least one file.")
        else:
            all_docs = []
            names = []
            with st.spinner("Ingesting documents…"):
                for f in uploaded_files:
                    docs = load_document(f)
                    all_docs.extend(docs)
                    names.append(f.name)
                st.session_state.vectorstore = build_vectorstore(all_docs)
                st.session_state.ingested_files = names
            st.success(f"✅ Ingested: {', '.join(names)}")

    if st.session_state.ingested_files:
        st.info(f"📚 Currently loaded: {', '.join(st.session_state.ingested_files)}")

# ── Tab 2: Ask Question ───────────────────────────────────────────────────────
with tab2:
    st.subheader("Ask a legal question about ingested documents")
    question = st.text_area(
        "Example: What is the termination clause in this contract?",
        height=100
    )

    if st.button("🔎 Get Answer", type="primary"):
        if not question.strip():
            st.warning("Please enter a question.")
        elif st.session_state.vectorstore is None:
            st.warning("Please upload and ingest documents first (Tab 1).")
        else:
            with st.spinner("Analyzing…"):
                chain = get_qa_chain(st.session_state.vectorstore)
                answer = chain.run(question)
            st.markdown("### Answer")
            st.write(answer)

# ── Tab 3: Summarize ──────────────────────────────────────────────────────────
with tab3:
    st.subheader("Summarize a single document")
    summary_file = st.file_uploader(
        "Upload one document to summarize",
        type=["pdf", "docx"],
        key="summary_file"
    )

    if st.button("📋 Summarize", type="primary"):
        if not summary_file:
            st.warning("Please upload a document.")
        else:
            with st.spinner("Summarizing…"):
                docs = load_document(summary_file)
                full_text = " ".join([d.page_content for d in docs])
                summary = summarize_text(full_text)
            st.markdown("### Summary")
            st.write(summary)

# ── Tab 4: Compare ────────────────────────────────────────────────────────────
with tab4:
    st.subheader("Compare two contracts side by side")
    col1, col2 = st.columns(2)
    with col1:
        file1 = st.file_uploader("Upload Contract 1", type=["pdf", "docx"], key="cmp1")
    with col2:
        file2 = st.file_uploader("Upload Contract 2", type=["pdf", "docx"], key="cmp2")

    if st.button("⚖️ Compare Contracts", type="primary"):
        if not file1 or not file2:
            st.warning("Please upload both documents.")
        else:
            with st.spinner("Comparing…"):
                docs1 = load_document(file1)
                docs2 = load_document(file2)
                text1 = " ".join([d.page_content for d in docs1])
                text2 = " ".join([d.page_content for d in docs2])
                comparison = compare_texts(text1, text2)
            st.markdown("### Comparison")
            st.write(comparison)
