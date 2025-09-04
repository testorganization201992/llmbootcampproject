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

# + BEGIN: memory imports # Assignment 1
from typing import Dict, List
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
# + END: memory imports

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.header("Basic Chatbot (No Memory → With Memory)")
st.write("This file runs with memory. Diff-style comments show changes.")

if "messages" not in st.session_state:
    st.session_state["messages"] = []  # [{role, content}]

utils.configure_openai_api_key()

# + BEGIN: memory store # Assignment 1 
class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    messages: List[BaseMessage] = Field(default_factory=list)
    def add_messages(self, messages: List[BaseMessage]) -> None:
        self.messages.extend(messages)
    def clear(self) -> None:
        self.messages = []

_hist_store: Dict[str, InMemoryHistory] = {}

def get_history_by_session(session_key: str) -> BaseChatMessageHistory:
    if session_key not in _hist_store:
        _hist_store[session_key] = InMemoryHistory()
    return _hist_store[session_key]
# + END: memory store

def build_chain(model: str = "gpt-4o-mini"):
    llm = ChatOpenAI(model=model, temperature=0, streaming=True)

    # - prompt = ChatPromptTemplate.from_messages(
    # -     [
    # -         ("system", "You are a helpful assistant."),
    # -         ("human", "{input}"),
    # -     ]
    # - )
    # - return prompt | llm

    # + BEGIN: memory-enabled prompt # Assignment 1 
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            MessagesPlaceholder("history"),   # include past turns
            ("human", "{input}"),
        ]
    )
    chain = prompt | llm
    return RunnableWithMessageHistory(
        chain,
        get_history_by_session,
        input_messages_key="input",
        history_messages_key="history",
    )
    # + END: memory-enabled prompt

if "chat_chain_nomem" not in st.session_state:
    st.session_state.chat_chain_nomem = build_chain()

# + BEGIN: memory session key # Assignment 1. 
MEMORY_SESSION_KEY = "chat-session-1"
# + END: memory session key

@utils.enable_chat_history
def main():
    chain = st.session_state.chat_chain_nomem
    user_query = st.chat_input("Ask me anything!")
    if not user_query:
        return

    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)

    with st.chat_message("assistant"):
        try:
            placeholder = st.empty()
            st_cb = StreamHandler(placeholder)

            # - result = chain.invoke({"input": user_query}, config={"callbacks": [st_cb]}) # Assignment 1 
            # + BEGIN: memory-enabled invoke
            result = chain.invoke(
                {"input": user_query},
                config={
                    "callbacks": [st_cb],
                    "configurable": {"session_id": MEMORY_SESSION_KEY},
                },
            )
            # + END: memory-enabled invoke

            st.session_state.messages.append(
                {"role": "assistant", "content": result.content}
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
    
    # Initialize session state variables with persistence
    if "show_settings" not in st.session_state:
        st.session_state.show_settings = False
    
    if "settings_applying" not in st.session_state:
        st.session_state.settings_applying = False
    
    # Ensure settings state persists across reruns
    if "settings_initialized" not in st.session_state:
        st.session_state.settings_initialized = True
    
    # Initialize default settings
    if "model_config" not in st.session_state:
        st.session_state.model_config = {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "max_tokens": 1500,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "system_prompt": "You are a helpful AI assistant. Provide clear, concise, and friendly responses.",
            "response_style": "Balanced",
            "language": "English"
        }
    
    # Settings toggle button (floating) and gray overlay
    st.markdown("""
    <style>
    .settings-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: rgba(255,255,255,0.9);
        border-radius: 50%;
        width: 50px;
        height: 50px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    
    # Create main layout with chat and settings panel
    if st.session_state.show_settings:
        chat_col, settings_col = st.columns([2.5, 1.5])
    else:
        chat_col = st.container()
        settings_col = None
    
    
    with chat_col:
        
        # Settings toggle button in top right of chat area - fixed positioning
        st.markdown("""
        <style>
        .settings-button {
            position: fixed !important;
            top: 20px !important;
            right: 20px !important;
            z-index: 1000 !important;
            background: white !important;
            border: 2px solid #667eea !important;
            border-radius: 50% !important;
            width: 50px !important;
            height: 50px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
            cursor: pointer !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Settings button with persistent state
        button_col1, button_col2, button_col3 = st.columns([8, 1, 1])
        
        # Debug info (remove this later)
        with button_col2:
            st.write(f"Settings: {'ON' if st.session_state.show_settings else 'OFF'}")
        
        with button_col3:
            button_icon = "✖️" if st.session_state.show_settings else "⚙️"
            button_help = "Close Settings" if st.session_state.show_settings else "Open Settings"
            
            # Use a unique key and more explicit handling
            if st.button(button_icon, 
                        key=f"toggle_{st.session_state.show_settings}", 
                        help=button_help,
                        type="secondary",
                        use_container_width=True):
                # Toggle settings state
                new_state = not st.session_state.show_settings
                st.session_state.show_settings = new_state
                st.rerun()
        
        # Get current model configuration
        model = st.session_state.model_config["model"]
        temperature = st.session_state.model_config["temperature"]  
        max_tokens = st.session_state.model_config["max_tokens"]
        
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
    
    # Settings panel on the right
    if st.session_state.show_settings and settings_col:
        with settings_col:
            st.markdown("""
            <style>
            .settings-panel {
                background: rgba(248, 249, 250, 0.95);
                padding: 1.5rem;
                border-radius: 15px;
                box-shadow: -5px 0 15px rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
                border-left: 3px solid #667eea;
                margin-top: -1rem;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="settings-panel">', unsafe_allow_html=True)
            
            st.markdown("### ⚙️ Settings")
            st.markdown("---")
            
            with st.form("settings_form", clear_on_submit=False):
                # Basic Model Settings
                st.subheader("🤖 Model Configuration")
                
                model = st.selectbox(
                    "AI Model",
                    ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
                    index=["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"].index(st.session_state.model_config["model"]),
                    help="Choose the AI model"
                )
                
                response_style = st.selectbox(
                    "🎭 Response Style",
                    ["Professional", "Casual", "Creative", "Technical", "Balanced"],
                    index=["Professional", "Casual", "Creative", "Technical", "Balanced"].index(st.session_state.model_config["response_style"]),
                    help="Set the AI's communication style"
                )
                
                st.markdown("---")
                
                # Advanced Parameters
                with st.expander("🔧 Advanced Parameters"):
                    temperature = st.slider(
                        "🌡️ Temperature", 
                        0.0, 2.0, 
                        st.session_state.model_config["temperature"], 
                        0.1, 
                        help="Controls randomness: 0=focused, 2=creative"
                    )
                    
                    top_p = st.slider(
                        "🎯 Top P", 
                        0.0, 1.0, 
                        st.session_state.model_config["top_p"], 
                        0.05, 
                        help="Controls diversity via nucleus sampling"
                    )
                    
                    max_tokens = st.number_input(
                        "📝 Max Tokens", 
                        100, 4000, 
                        st.session_state.model_config["max_tokens"], 
                        100,
                        help="Maximum response length"
                    )
                    
                    frequency_penalty = st.slider(
                        "🔄 Frequency Penalty",
                        -2.0, 2.0,
                        st.session_state.model_config["frequency_penalty"],
                        0.1,
                        help="Reduce repetition of frequent tokens"
                    )
                    
                    presence_penalty = st.slider(
                        "✨ Presence Penalty",
                        -2.0, 2.0,
                        st.session_state.model_config["presence_penalty"],
                        0.1,
                        help="Encourage new topics"
                    )
                
                st.markdown("---")
                
                # Custom System Prompt
                with st.expander("📝 Custom System Prompt"):
                    custom_prompt = st.text_area(
                        "System Message",
                        value=st.session_state.model_config["system_prompt"],
                        height=100,
                        help="Custom instructions for the AI (only used with 'Balanced' style)"
                    )
                
                st.markdown("---")
                
                # Preset Configurations
                st.subheader("⚡ Quick Presets")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.form_submit_button("💬 Conversational", use_container_width=True):
                        preset_config = {
                            "model": "gpt-4o-mini",
                            "temperature": 0.8,
                            "top_p": 0.9,
                            "max_tokens": 2000,
                            "frequency_penalty": 0.3,
                            "presence_penalty": 0.3,
                            "response_style": "Casual",
                            "system_prompt": st.session_state.model_config["system_prompt"],
                            "language": "English"
                        }
                        st.session_state.model_config.update(preset_config)
                        st.success("💬 Conversational preset applied!")
                        # Small delay to show success message
                        import time
                        time.sleep(0.5)
                        st.rerun()
                
                with col2:
                    if st.form_submit_button("🔬 Analytical", use_container_width=True):
                        preset_config = {
                            "model": "gpt-4o",
                            "temperature": 0.2,
                            "top_p": 0.8,
                            "max_tokens": 3000,
                            "frequency_penalty": 0.0,
                            "presence_penalty": 0.1,
                            "response_style": "Technical",
                            "system_prompt": st.session_state.model_config["system_prompt"],
                            "language": "English"
                        }
                        st.session_state.model_config.update(preset_config)
                        st.success("🔬 Analytical preset applied!")
                        import time
                        time.sleep(0.5)
                        st.rerun()
                
                col3, col4 = st.columns(2)
                
                with col3:
                    if st.form_submit_button("🎨 Creative", use_container_width=True):
                        preset_config = {
                            "model": "gpt-4o",
                            "temperature": 1.2,
                            "top_p": 0.95,
                            "max_tokens": 2500,
                            "frequency_penalty": 0.5,
                            "presence_penalty": 0.6,
                            "response_style": "Creative",
                            "system_prompt": st.session_state.model_config["system_prompt"],
                            "language": "English"
                        }
                        st.session_state.model_config.update(preset_config)
                        st.success("🎨 Creative preset applied!")
                        import time
                        time.sleep(0.5)
                        st.rerun()
                
                with col4:
                    if st.form_submit_button("💼 Professional", use_container_width=True):
                        preset_config = {
                            "model": "gpt-4o-mini",
                            "temperature": 0.3,
                            "top_p": 0.85,
                            "max_tokens": 2000,
                            "frequency_penalty": 0.1,
                            "presence_penalty": 0.1,
                            "response_style": "Professional",
                            "system_prompt": st.session_state.model_config["system_prompt"],
                            "language": "English"
                        }
                        st.session_state.model_config.update(preset_config)
                        st.success("💼 Professional preset applied!")
                        import time
                        time.sleep(0.5)
                        st.rerun()
                
                st.markdown("---")
                
                # Apply custom settings button
                if st.form_submit_button("✅ Apply Custom Settings", type="primary", use_container_width=True):
                    st.session_state.model_config.update({
                        "model": model,
                        "temperature": temperature,
                        "top_p": top_p,
                        "max_tokens": max_tokens,
                        "frequency_penalty": frequency_penalty,
                        "presence_penalty": presence_penalty,
                        "response_style": response_style,
                        "system_prompt": custom_prompt,
                        "language": "English"
                    })
                    st.success("✅ Custom settings applied successfully!")
                    import time
                    time.sleep(0.5)
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
