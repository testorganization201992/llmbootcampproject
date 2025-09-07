import os
import streamlit as st
from ui_components import ChatbotUI, APIKeyUI
from langchain_helpers import RAGHelper, ValidationHelper

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
    
    # Enhanced visual styling
    st.markdown("""
    <style>
        /* Enhanced chat styling */
        .stChatMessage {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 15px;
            background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
            border: 1px solid rgba(0, 212, 170, 0.1);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }
        
        /* Enhanced buttons */
        .stButton > button {
            background: linear-gradient(135deg, #00d4aa, #00a883);
            border: none;
            border-radius: 10px;
            color: white;
            font-weight: 600;
            padding: 0.75rem 2rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 212, 170, 0.4);
            background: linear-gradient(135deg, #00e6c0, #00cc99);
        }
        
        /* Enhanced text inputs */
        .stTextInput > div > div > input {
            background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
            border: 2px solid rgba(0, 212, 170, 0.2);
            border-radius: 10px;
            color: #ffffff;
            font-size: 16px;
            padding: 12px;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #00d4aa;
            box-shadow: 0 0 20px rgba(0, 212, 170, 0.3);
        }
        
        /* Enhanced file uploader */
        .stFileUploader > div {
            background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
            border: 2px dashed rgba(0, 212, 170, 0.3);
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .stFileUploader > div:hover {
            border-color: #00d4aa;
            box-shadow: 0 0 20px rgba(0, 212, 170, 0.2);
        }
        
        /* Enhanced titles */
        h1 {
            background: linear-gradient(135deg, #00d4aa, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            text-shadow: 0 0 30px rgba(0, 212, 170, 0.5);
        }
        
        /* Enhanced progress bars */
        .stProgress > div > div {
            background: linear-gradient(135deg, #00d4aa, #00a883);
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
                if ValidationHelper.validate_openai_key(api_key_input):
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

# --------------------------
# Simple Agentic RAG Graph
# --------------------------

# --------------------------
# App
# --------------------------
class CustomDataChatbot:
    def __init__(self):
        self.openai_model = "gpt-4o-mini"

    def setup_graph(self, uploaded_files):
        return RAGHelper.setup_rag_system(uploaded_files)
    
    def display_messages(self):
        """Display chat messages using pure Streamlit components."""
        if st.session_state.rag_messages:
            for message in st.session_state.rag_messages:
                if message["role"] == "user":
                    with st.chat_message("user", avatar="https://em-content.zobj.net/source/apple/354/man-technologist-medium-skin-tone_1f468-1f3fd-200d-1f4bb.png"):
                        st.write(message["content"])
                else:
                    with st.chat_message("assistant", avatar="https://em-content.zobj.net/source/apple/354/robot_1f916.png"):
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
                with st.chat_message("assistant", avatar="https://em-content.zobj.net/source/apple/354/robot_1f916.png"):
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
    
    # Page title - centered with enhanced styling
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0;'>
        <h1 style='font-size: 3.5rem; margin-bottom: 1rem; text-shadow: 0 0 30px rgba(0, 212, 170, 0.5);'>
            📚 Chat with your Data
        </h1>
        <p style='font-size: 1.2rem; color: #a0a0a0; margin-top: -0.5rem;'>
            Upload documents and get intelligent answers using RAG
        </p>
    </div>
    """, unsafe_allow_html=True)
    
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
