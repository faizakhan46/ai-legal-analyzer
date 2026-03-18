import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api"

st.set_page_config(page_title="AI Legal Document Analyzer", layout="wide")

st.title("AI Legal Document Analyzer")
st.caption("Upload contracts, ask legal questions, summarize documents, and compare contracts.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Upload & Ingest",
    "Ask Question",
    "Summarize",
    "Compare",
    "Orchestrator"
])

with tab1:
    st.subheader("Upload and ingest legal documents")
    uploaded_files = st.file_uploader(
        "Choose PDF or DOCX files",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if st.button("Upload & Ingest"):
        if not uploaded_files:
            st.warning("Please select at least one file.")
        else:
            files_payload = []
            for file in uploaded_files:
                files_payload.append(
                    ("files", (file.name, file, file.type or "application/octet-stream"))
                )

            response = requests.post(f"{API_URL}/upload-documents", files=files_payload)

            if response.status_code == 200:
                st.success("Documents ingested successfully.")
                st.json(response.json())
            else:
                st.error(response.text)

with tab2:
    st.subheader("Ask a legal question")
    question = st.text_area("Example: What is the termination clause in this contract?")

    if st.button("Get Answer"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            response = requests.post(
                f"{API_URL}/ask-question",
                data={"query": question}
            )

            if response.status_code == 200:
                st.write(response.json()["answer"])
            else:
                st.error(response.text)

with tab3:
    st.subheader("Summarize one document")
    summary_file = st.file_uploader(
        "Upload one document",
        type=["pdf", "docx"],
        key="summary_file"
    )

    if st.button("Summarize Document"):
        if not summary_file:
            st.warning("Please upload a document.")
        else:
            files_payload = {
                "file": (summary_file.name, summary_file, summary_file.type or "application/octet-stream")
            }

            response = requests.post(
                f"{API_URL}/summarize-document",
                files=files_payload
            )

            if response.status_code == 200:
                st.write(response.json()["summary"])
            else:
                st.error(response.text)

with tab4:
    st.subheader("Compare two contracts")
    compare_file1 = st.file_uploader(
        "Upload first contract",
        type=["pdf", "docx"],
        key="compare_file1"
    )
    compare_file2 = st.file_uploader(
        "Upload second contract",
        type=["pdf", "docx"],
        key="compare_file2"
    )

    if st.button("Compare Contracts"):
        if not compare_file1 or not compare_file2:
            st.warning("Please upload both documents.")
        else:
            files_payload = [
                ("file1", (compare_file1.name, compare_file1, compare_file1.type or "application/octet-stream")),
                ("file2", (compare_file2.name, compare_file2, compare_file2.type or "application/octet-stream"))
            ]

            response = requests.post(
                f"{API_URL}/compare-documents",
                files=files_payload
            )

            if response.status_code == 200:
                st.write(response.json()["comparison"])
            else:
                st.error(response.text)

with tab5:
    st.subheader("Agent orchestration")
    orchestrator_query = st.text_area(
        "Ask naturally. Example: summarize this contract / compare these two contracts / what is the confidentiality clause?"
    )
    orchestrator_files = st.file_uploader(
        "Optional files for summarize or compare",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        key="orchestrator_files"
    )

    if st.button("Run Orchestrator"):
        if not orchestrator_query.strip():
            st.warning("Please enter a query.")
        else:
            files_payload = []
            if orchestrator_files:
                for file in orchestrator_files:
                    files_payload.append(
                        ("files", (file.name, file, file.type or "application/octet-stream"))
                    )

            response = requests.post(
                f"{API_URL}/orchestrate",
                data={"query": orchestrator_query},
                files=files_payload if files_payload else None
            )

            if response.status_code == 200:
                st.write(response.json()["result"])
            else:
                st.error(response.text)
