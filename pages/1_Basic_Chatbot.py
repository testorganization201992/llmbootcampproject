"""
Modern Beautiful Chatbot
A sleek, modern chatbot with the best appearance and functionality.
"""

import streamlit as st
import os
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
