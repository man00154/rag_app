import streamlit as st
import os
from utils import ensure_data, load_pdfs_from_folder, load_html_from_folder, load_vectorstore, create_vectorstore
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="RAG PDF + Web Chat", layout="wide")
st.title("📄🔗 RAG Chatbot —MANISH SINGH- PDFs + Websites")

# Step 1 — Auto download data on first run
ensure_data()

# Sidebar upload
st.sidebar.header("📂 Upload PDFs")
uploaded_files = st.sidebar.file_uploader("Upload multiple PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    save_dir = "sample_data"
    for file in uploaded_files:
        with open(os.path.join(save_dir, file.name), "wb") as f:
            f.write(file.getbuffer())
    st.sidebar.success(f"{len(uploaded_files)} PDFs uploaded.")

# PDF preview
with st.expander("📑 View PDF Files"):
    for pdf in os.listdir("sample_data"):
        if pdf.endswith(".pdf"):
            st.markdown(f"**{pdf}**")
            st.markdown(f'<iframe src="file://{os.path.abspath("sample_data/"+pdf)}" width="100%" height="500"></iframe>', unsafe_allow_html=True)

# Step 2 — Build vectorstore if not exists
if not os.path.exists("vectorstore"):
    st.write("Creating vectorstore (this may take a while)...")
    pdf_docs = load_pdfs_from_folder("sample_data")
    html_docs = load_html_from_folder("html_data")
    create_vectorstore(pdf_docs, html_docs)

vectorstore = load_vectorstore()

# Step 3 — Chatbot
llm = ChatOpenAI(temperature=0)
qa_chain = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())

if "history" not in st.session_state:
    st.session_state.history = []

user_question = st.text_input("Ask a question about the PDFs & Websites:")
if user_question:
    response = qa_chain.run({"question": user_question, "chat_history": st.session_state.history})
    st.session_state.history.append((user_question, response))
    st.markdown(f"**Answer:** {response}")

# Show chat history
st.subheader("💬 Chat History")
for q, a in st.session_state.history:
    st.write(f"**You:** {q}")
    st.write(f"**Bot:** {a}")
