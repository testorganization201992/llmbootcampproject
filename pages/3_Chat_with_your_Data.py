"""Chat with your Data Page.

RAG (Retrieval-Augmented Generation) powered chatbot that enables
intelligent question-answering over user-uploaded PDF documents.
Features automatic document processing, vector search, and contextual responses.
"""

import streamlit as st
from typing import List, Any
from config.api_config import get_openai_api_key, display_missing_keys_error
from utils.langchain_helpers import RAGHelper
from ui_components.home_ui import ChatbotUI


def main():
    """Main RAG chatbot function."""
    # Setup page
    ChatbotUI.setup_page("Chat with Documents", "📚")
    ChatbotUI.render_page_header(
        "📚", 
        "Chat with your Data", 
        "RAG-powered document Q&A with intelligent retrieval"
    )
    
    # Validate API key
    try:
        api_key = get_openai_api_key()
    except ValueError as e:
        st.error(f"❌ {e}")
        display_missing_keys_error(["OPENAI_API_KEY"])
        return
    
    # Initialize session state
    if "rag_uploaded_files" not in st.session_state:
        st.session_state.rag_uploaded_files = []
    if "rag_app" not in st.session_state:
        st.session_state.rag_app = None
    if "rag_messages" not in st.session_state:
        st.session_state.rag_messages = []
    if "rag_processing" not in st.session_state:
        st.session_state.rag_processing = False

    # Document upload interface
    col1, col2, col3 = st.columns([2, 1.5, 2])
    with col2:
        uploaded_files = st.file_uploader(
            label="**Upload PDF files to chat with your documents**",
            type=["pdf"],
            accept_multiple_files=True
        )

    # Process documents when uploaded
    if uploaded_files:
        current_files = {f.name for f in uploaded_files}
        previous_files = {f.name for f in st.session_state.get("rag_uploaded_files", [])}
        
        # Rebuild RAG system if files changed
        if current_files != previous_files or st.session_state.rag_app is None:
            st.session_state.rag_uploaded_files = uploaded_files
            with st.spinner("📚 Processing documents..."):
                st.session_state.rag_app = RAGHelper.setup_rag_system(uploaded_files, api_key)
    else:
        # Show welcome message when no documents uploaded
        if not st.session_state.rag_messages:
            st.info("📄 Upload PDF documents above to start asking questions about them!")
        return

    # Display all messages
    for message in st.session_state.rag_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if not st.session_state.rag_messages:
        st.info("📄 Ask questions about your uploaded documents!")

    # Show processing state if needed
    if st.session_state.rag_processing:
        with st.chat_message("assistant"):
            with st.spinner("Analyzing documents..."):
                try:
                    # Get the last user message
                    last_user_msg = next((msg["content"] for msg in reversed(st.session_state.rag_messages) if msg["role"] == "user"), "")
                    
                    result = st.session_state.rag_app.invoke({
                        "question": last_user_msg, 
                        "mode": "fact", 
                        "documents": [], 
                        "generation": ""
                    })
                    
                    answer = (
                        result.get("generation", "").strip() or 
                        "I couldn't find enough information in the documents to answer that."
                    )
                    
                    st.markdown(answer)
                    st.session_state.rag_messages.append({
                        "role": "assistant", 
                        "content": answer
                    })
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.rag_messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
                finally:
                    st.session_state.rag_processing = False
                    st.rerun()

    # Handle user input - only accept new input when not processing
    if prompt := st.chat_input("Ask about your documents..."):
        if not st.session_state.rag_processing:
            # Add user message and set processing flag
            st.session_state.rag_messages.append({"role": "user", "content": prompt})
            st.session_state.rag_processing = True
            st.rerun()


if __name__ == "__main__":
    main()
