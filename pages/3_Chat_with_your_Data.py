import os
import streamlit as st
from typing import List, TypedDict, Literal
from langchain_core.documents import Document

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

from langgraph.graph import StateGraph, END

# --------------------------
# Page config
# --------------------------
def setup_page():
    """Set up the page with basic config."""
    st.set_page_config(
        page_title="Chat with Documents", 
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Force light theme
    st.markdown("""
    <style>
        .stApp {
            background-color: #ffffff !important;
            color: #262730 !important;
        }
        .stApp > div {
            background-color: #ffffff !important;
        }
        [data-testid="stSidebar"] {
            background-color: #f0f2f6 !important;
        }
    </style>
    """, unsafe_allow_html=True)

def configure_api_key():
    """Configure OpenAI API key."""
    api_key = st.session_state.get("rag_openai_key", "")
    
    if not api_key:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔑 Enter API Key")
            
            # Check if we just connected (avoid showing form again)
            if st.session_state.get("rag_key_connected", False):
                st.session_state["rag_key_connected"] = False
                return True
                
            api_key_input = st.text_input(
                "OpenAI API Key",
                type="password",
                placeholder="sk-proj-...",
                key="rag_api_key_input"
            )
            
            if st.button("Connect", type="primary", use_container_width=True):
                if api_key_input and api_key_input.startswith("sk-"):
                    st.session_state["rag_openai_key"] = api_key_input
                    st.session_state["rag_key_connected"] = True
                    st.rerun()
                else:
                    st.error("❌ Invalid key format")
        return False
    
    return True

# --------------------------
# Utilities
# --------------------------
def save_file(file, folder="tmp") -> str:
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getvalue())
    return file_path

def build_vectorstore(files) -> FAISS:
    docs: List[Document] = []
    progress_bar = st.progress(0, text=f"Processing {len(files)} files...")

    for idx, file in enumerate(files):
        path = save_file(file)
        loader = PyPDFLoader(path)
        docs.extend(loader.load())
        progress_bar.progress((idx + 1) / len(files), text=f"Processed {idx+1}/{len(files)}")

    progress_bar.progress(100, text="Building vector store...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    vectordb = FAISS.from_documents(chunks, embeddings)
    
    # Remove the progress bar after completion
    progress_bar.empty()
    
    return vectordb

# --------------------------
# Simple Agentic RAG Graph
# --------------------------
class RAGState(TypedDict):
    question: str
    mode: Literal["summary", "fact"]
    documents: List[Document]
    generation: str

def build_simple_agentic_rag(retriever, llm: ChatOpenAI):
    """
    Graph:
      classify_mode -> retrieve -> generate -> END
    """

    # --- Node: classify mode (summary vs fact) ---
    SUMMARY_HINTS = ("summarize", "summary", "overview", "key points", "bullet", "synthesize")
    FACT_HINTS = ("when", "date", "who", "where", "amount", "total", "price", "figure", "specific", "exact")

    def classify_mode(state: RAGState) -> RAGState:
        q = state["question"].lower()
        if any(w in q for w in SUMMARY_HINTS) and not any(w in q for w in FACT_HINTS):
            mode: Literal["summary", "fact"] = "summary"
        elif any(w in q for w in FACT_HINTS):
            mode = "fact"
        else:
            # default to fact unless they asked to summarize
            mode = "summary" if "summary" in q or "summarize" in q else "fact"
        return {**state, "mode": mode}

    # --- Node: retrieve ---
    def retrieve(state: RAGState) -> RAGState:
        q = state["question"]
        k = 8 if state["mode"] == "summary" else 3
        docs = retriever.invoke(q)
        return {**state, "documents": docs[:k]}

    # --- Node: generate ---
    gen_prompt_summary = ChatPromptTemplate.from_messages(
        [
            ("system",
             "You are a helpful assistant. Create a concise, faithful summary ONLY using the provided context. "
             "Prefer bullet points if helpful. Do not use outside knowledge."),
            ("human",
             "Question:\n{question}\n\n"
             "Context (multiple document chunks):\n{context}\n\n"
             "Write a grounded summary:")
        ]
    )

    gen_prompt_fact = ChatPromptTemplate.from_messages(
        [
            ("system",
             "You are a helpful assistant. Answer precisely and ONLY using the provided context. "
             "If the context is insufficient, say so."),
            ("human",
             "Question:\n{question}\n\n"
             "Context:\n{context}\n\n"
             "Answer:")
        ]
    )

    def generate(state: RAGState) -> RAGState:
        ctx = "\n\n---\n\n".join(d.page_content for d in state.get("documents", []))
        if not ctx.strip():
            return {**state, "generation": "I couldn't find enough information in the documents to answer that."}

        if state["mode"] == "summary":
            answer = llm.invoke(gen_prompt_summary.format_messages(
                question=state["question"], context=ctx
            )).content
        else:
            answer = llm.invoke(gen_prompt_fact.format_messages(
                question=state["question"], context=ctx
            )).content
        return {**state, "generation": answer}

    # --- Build graph ---
    graph = StateGraph(RAGState)
    graph.add_node("classify_mode", classify_mode)
    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)

    graph.set_entry_point("classify_mode")
    graph.add_edge("classify_mode", "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()

# --------------------------
# App
# --------------------------
class CustomDataChatbot:
    def __init__(self):
        self.openai_model = "gpt-4o-mini"

    def setup_graph(self, uploaded_files):
        vectordb = build_vectorstore(uploaded_files)
        retriever = vectordb.as_retriever()
        llm = ChatOpenAI(model=self.openai_model, temperature=0, streaming=False)
        return build_simple_agentic_rag(retriever, llm)
    
    def display_messages(self):
        """Display chat messages using pure Streamlit components."""
        if st.session_state.rag_messages:
            for message in st.session_state.rag_messages:
                if message["role"] == "user":
                    with st.chat_message("user"):
                        st.write(message["content"])
                else:
                    with st.chat_message("assistant"):
                        st.write(message["content"])

    def main(self):
        # Initialize session state with unique keys
        if "rag_uploaded_files" not in st.session_state:
            st.session_state.rag_uploaded_files = []
        if "rag_app" not in st.session_state:
            st.session_state.rag_app = None
        if "rag_messages" not in st.session_state:
            st.session_state.rag_messages = []

        # Document upload section - centered
        col1, col2, col3 = st.columns([2, 1.5, 2])
        with col2:
            uploaded_files = st.file_uploader(
                label="**Upload PDF files to chat with your documents**",
                type=["pdf"],
                accept_multiple_files=True
            )
            
            # Files are handled automatically - no need for success message
                
        st.markdown("<br>", unsafe_allow_html=True)

        if uploaded_files:
            current = {f.name for f in uploaded_files}
            prev = {f.name for f in st.session_state.get("rag_uploaded_files", [])}
            if current != prev or st.session_state.rag_app is None:
                st.session_state.rag_uploaded_files = uploaded_files
                with st.spinner("📚 Processing documents..."):
                    st.session_state.rag_app = self.setup_graph(uploaded_files)
        else:
            # Show welcome screen when no documents uploaded
            if not st.session_state.rag_messages:
                self.display_messages()
            return
            
        # Display messages
        self.display_messages()
        
        # Generate response if needed
        if (st.session_state.rag_messages and 
            st.session_state.rag_messages[-1]["role"] == "user" and
            not st.session_state.get("rag_processing", False)):
            
            st.session_state.rag_processing = True
            try:
                # Show processing indicator
                with st.chat_message("assistant"):
                    with st.spinner("Analyzing documents..."):
                        # Get the last user message
                        user_query = st.session_state.rag_messages[-1]["content"]
                        
                        result = st.session_state.rag_app.invoke(
                            {"question": user_query, "mode": "fact", "documents": [], "generation": ""}
                        )
                        answer = result.get("generation", "").strip() or "I couldn't find enough information in the documents to answer that."
                        
                        # Add assistant response
                        st.session_state.rag_messages.append({"role": "assistant", "content": answer})
                
                st.session_state.rag_processing = False
                st.rerun()
                
            except Exception as e:
                st.session_state.rag_processing = False
                st.error(f"Error: {str(e)}")
                st.rerun()

        # Chat input - outside container to prevent shifting
        if prompt := st.chat_input("Ask about your documents..."):
            # Add user message and rerun to show it first
            st.session_state.rag_messages.append({"role": "user", "content": prompt})
            st.rerun()

def main():
    """Main application function."""
    setup_page()
    
    # Page title - centered
    st.markdown("<h1 style='text-align: center; margin-top: -75px;'>📄 Chat with your Data</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Check API key - Show login screen
    if not configure_api_key():
        return
    
    # Run chatbot
    app = CustomDataChatbot()
    app.main()

# --------------------------
# Run
# --------------------------
if __name__ == "__main__":
    main()
