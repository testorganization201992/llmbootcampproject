"""
Modern Beautiful Chatbot
A sleek, modern chatbot with the best appearance and functionality.
"""

import streamlit as st
import os
import sys
sys.path.append('..')
from themes.modern_theme import apply_modern_theme, show_processing_animation
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def setup_page():
    """Set up the page with modern styling."""
    st.set_page_config(
        page_title="Modern AI Chat",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply modern theme
    apply_modern_theme()

def build_chain(config):
    """Build the LangChain chain."""
    llm = ChatOpenAI(
        model=config["model"],
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
        streaming=False
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Provide clear, concise, and friendly responses."),
        ("human", "{input}"),
    ])
    
    return prompt | llm

def configure_api_key():
    """Configure OpenAI API key."""
    api_key = os.environ.get("OPENAI_API_KEY") or st.session_state.get("OPENAI_API_KEY", "")
    
    if not api_key:
        # Simple API key input in sidebar instead of modal
        with st.sidebar:
            st.markdown("### 🔑 API Key")
            api_key_input = st.text_input(
                "OpenAI API Key",
                type="password",
                placeholder="sk-proj-...",
                key="api_key_input"
            )
            
            if st.button("Connect", type="primary", use_container_width=True):
                if api_key_input and api_key_input.startswith("sk-"):
                    st.session_state["OPENAI_API_KEY"] = api_key_input
                    os.environ["OPENAI_API_KEY"] = api_key_input
                    st.success("✅ Connected!")
                    st.rerun()
                else:
                    st.error("❌ Invalid key format")
        return False
    
    return True

def display_messages():
    """Display chat messages."""
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-screen">
            <div class="welcome-icon">🤖</div>
            <h3>Welcome to Modern AI Chat</h3>
            <p>Ask me anything and I'll be happy to help!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="messages-area">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                st.markdown(f"""
                <div class="chat-message user">
                    <div class="message-bubble user">{content}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant">
                    <div class="message-bubble assistant">{content}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application function."""
    setup_page()
    
    
    # Check API key - Show login screen
    if not configure_api_key():
        st.markdown("""
        <div class="welcome-screen" style="height: 500px;">
            <div class="welcome-icon">🔐</div>
            <h3>API Key Required</h3>
            <p>Please enter your OpenAI API key in the sidebar to continue</p>
            <div style="margin-top: 2rem; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px; backdrop-filter: blur(5px);">
                <p style="font-size: 1rem; margin: 0.5rem 0;">1. Get your API key from <a href="https://platform.openai.com/api-keys" target="_blank" style="color: #667eea;">OpenAI Platform</a></p>
                <p style="font-size: 1rem; margin: 0.5rem 0;">2. Enter it in the sidebar</p>
                <p style="font-size: 1rem; margin: 0.5rem 0;">3. Click "Connect" to start chatting</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        model = st.selectbox(
            "Model",
            ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
            index=0
        )
        
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
        max_tokens = st.number_input("Max Tokens", 100, 4000, 1500, 100)
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🚀 Features")
        st.markdown("• Modern UI Design")
        st.markdown("• Real-time Responses") 
        st.markdown("• Multiple AI Models")
        st.markdown("• Customizable Settings")
    
    # Build chain
    config = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    if "chain" not in st.session_state or st.session_state.get("last_config") != str(config):
        st.session_state.chain = build_chain(config)
        st.session_state.last_config = str(config)
    
    # Initialize messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display messages
    display_messages()
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate response
        try:
            # Show processing animation
            st.markdown(show_processing_animation(), unsafe_allow_html=True)
            
            response = st.session_state.chain.invoke({"input": prompt})
                
            # Add assistant response
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response.content
            })
            
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()