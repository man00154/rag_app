import streamlit as st
from utils import ensure_data, load_pdfs_from_folder, load_html_from_folder, create_vectorstore, load_vectorstore
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
import os

st.set_page_config(page_title="RAG App", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("📄 RAG App with PDF/HTML Sources")

with st.sidebar:
    st.header("Data Management")
    if st.button("Download Default Data"):
        ensure_data()
        st.success("Default PDFs and HTML downloaded!")

    uploaded_files = st.file_uploader("Upload PDFs or TXT files", type=["pdf", "txt"], accept_multiple_files=True)
    if st.button("Build Vectorstore"):
        pdf_docs = load_pdfs_from_folder("sample_data")
        html_docs = load_html_from_folder("html_data")
        create_vectorstore(pdf_docs, html_docs)
        st.success("Vectorstore created!")

if os.path.exists("vectorstore"):
    vectorstore = load_vectorstore()
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=vectorstore.as_retriever())

    query = st.chat_input("Ask something about the documents...")
    if query:
        st.session_state.messages.append(("user", query))
        result = qa_chain({"question": query, "chat_history": st.session_state.messages})
        st.session_state.messages.append(("assistant", result["answer"]))

for role, text in st.session_state.messages:
    st.chat_message(role).write(text)
