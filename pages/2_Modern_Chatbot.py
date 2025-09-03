"""
Modern Beautiful Chatbot
A sleek, modern chatbot with the best appearance and functionality.
"""

import streamlit as st
import os
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
    
    # Modern CSS styling
    st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Main app background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    /* Chat container */
    .chat-container {
        background: transparent;
        margin: 2rem auto;
        max-width: 800px;
        min-height: 600px;
        display: flex;
        flex-direction: column;
    }
    
    /* Header */
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px 20px 0 0;
        text-align: center;
    }
    
    .chat-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin: 0;
    }
    
    /* Messages area */
    .messages-area {
        flex: 1;
        padding: 1rem 0;
        overflow-y: auto;
        max-height: 400px;
        width: 60%;
        margin: 0 auto;
        box-sizing: border-box;
    }
    
    /* Message styling */
    .chat-message {
        margin: 2rem 0;
        display: flex;
        align-items: flex-start;
        padding: 0;
    }
    
    .chat-message.user {
        justify-content: flex-end;
        transform: translateX(-25px) !important;
    }
    
    .chat-message.assistant {
        justify-content: flex-start;
        transform: translateX(25px) !important;
    }
    
    .message-bubble {
        max-width: 30%;
        padding: 1.2rem 1.8rem;
        border-radius: 18px;
        font-size: 1.6rem;
        line-height: 1.6;
        font-weight: 500;
        word-wrap: break-word;
        white-space: pre-wrap;
        overflow-wrap: break-word;
    }
    
    .message-bubble.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 6px;
        transform: translateX(-400px) !important;
    }
    
    .message-bubble.assistant {
        background: #f1f3f4;
        color: #333;
        border-bottom-left-radius: 6px;
        transform: translateX(400px) !important;
    }
    
    /* Input area */
    .input-area {
        padding: 1rem 0;
    }
    
    /* Custom chat input styling */
    .stChatInput {
        width: 60% !important;
        margin: 0 auto !important;
    }
    
    .stChatInput > div,
    .stChatInput > div > div,
    .stChatInput div[data-testid="stChatInputContainer"] {
        border-radius: 25px !important;
        border: none !important;
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        min-height: 160px !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stChatInput input,
    .stChatInput textarea {
        border: none !important;
        background: transparent !important;
        font-size: 1.6rem !important;
        padding: 20px 25px !important;
        min-height: 160px !important;
        line-height: 1.6 !important;
        font-weight: 500 !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        color: #2d3748 !important;
        margin: 0 !important;
        box-shadow: none !important;
    }
    
    /* Force override all Streamlit input containers and elements */
    div[data-testid="stChatInput"],
    div[data-testid="stChatInput"] > div,
    div[data-testid="stChatInput"] > div > div,
    div[data-testid="stChatInputContainer"],
    .stChatInput > div,
    .stChatInput > div > div {
        background: rgba(255, 255, 255, 0.2) !important;
        background-color: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border: none !important;
        outline: none !important;
    }
    
    /* Force override input text elements */
    div[data-testid="stChatInput"] input,
    div[data-testid="stChatInput"] textarea,
    div[data-testid="stChatInput"] div input,
    div[data-testid="stChatInput"] div textarea,
    .stChatInput div div input,
    .stChatInput div div textarea {
        font-size: 1.6rem !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        background: transparent !important;
        background-color: transparent !important;
        color: #2d3748 !important;
        margin: 0 !important;
        border: none !important;
        border-right: none !important;
        border-left: none !important;
        border-top: none !important;
        border-bottom: none !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    /* Welcome screen */
    .welcome-screen {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 300px;
        text-align: center;
        color: #666;
    }
    
    .welcome-screen h3 {
        font-size: 2.5rem;
        margin: 1rem 0;
        color: #2d3748;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(255,255,255,0.8);
        background: rgba(255,255,255,0.9);
        padding: 1rem 2rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    .welcome-screen p {
        font-size: 1.4rem;
        margin: 0.5rem 0;
        color: #2d3748;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
        background: rgba(255,255,255,0.8);
        padding: 0.5rem 1.5rem;
        border-radius: 10px;
        backdrop-filter: blur(5px);
    }
    
    .welcome-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Success/Error messages */
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

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
    
    
    # Check API key
    if not configure_api_key():
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #666;">
            <h3>🔑 Please enter your OpenAI API key in the sidebar to get started</h3>
            <p>Once connected, you can start chatting with the AI assistant!</p>
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
            # Custom spinner positioned like AI response
            st.markdown("""
            <div class="chat-message assistant" style="margin-bottom: 0;">
                <div class="message-bubble assistant" style="background: rgba(241, 243, 244, 0.8); display: flex; align-items: center; min-height: 50px;">
                    <div style="display: flex; gap: 0.5rem;">
                        <div style="width: 8px; height: 8px; background: #667eea; border-radius: 50%; animation: pulse 1.5s infinite;"></div>
                        <div style="width: 8px; height: 8px; background: #764ba2; border-radius: 50%; animation: pulse 1.5s infinite 0.2s;"></div>
                        <div style="width: 8px; height: 8px; background: #667eea; border-radius: 50%; animation: pulse 1.5s infinite 0.4s;"></div>
                    </div>
                </div>
            </div>
            <style>
            @keyframes pulse {
                0%, 60%, 100% { transform: scale(0.8); opacity: 0.5; }
                30% { transform: scale(1.2); opacity: 1; }
            }
            </style>
            """, unsafe_allow_html=True)
            
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