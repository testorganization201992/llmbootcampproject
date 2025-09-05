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
                    st.session_state["api_key_just_connected"] = True
                    st.rerun()
                else:
                    st.error("❌ Invalid key format")
        return False
    
    return True

def display_messages():
    """Display chat messages using pure Streamlit components."""
    if not st.session_state.messages:
        st.info("🤖 Ask me anything and I'll be happy to help!")
    else:
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(message["content"])
    
    # Show thinking animation if processing
    if st.session_state.get("processing", False):
        with st.chat_message("assistant"):
            st.write("🤔 Thinking...")

def main():
    """Main application function."""
    setup_page()
    
    # Page title - centered
    st.markdown("<h1 style='text-align: center;'>🤖 Basic Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Check API key - Show login screen
    if not configure_api_key():
        return
    
    
    # Main chat container
    with st.container():
        
        # Simple chain with default configuration
        config = {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        if "chain" not in st.session_state:
            st.session_state.chain = build_chain(config)
        
        # Initialize messages
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Create stable messages container
        messages_container = st.container()
        with messages_container:
            display_messages()
        
        # Check if we need to generate a response (last message is from user)
        if (st.session_state.messages and 
            st.session_state.messages[-1]["role"] == "user" and
            not st.session_state.get("processing", False)):
            
            # Set processing flag and rerun to show thinking animation
            st.session_state.processing = True
            st.rerun()
        
        # Generate response if processing
        if st.session_state.get("processing", False):
            try:
                # Get the last user message
                user_input = st.session_state.messages[-1]["content"]
                response = st.session_state.chain.invoke({"input": user_input})
                    
                # Add assistant response
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response.content
                })
                
                # Clear processing flag and rerun to show response
                st.session_state.processing = False
                st.rerun()
                
            except Exception as e:
                st.session_state.processing = False
                st.error(f"Error: {str(e)}")
                st.rerun()

    # Chat input - outside container to prevent shifting
    if prompt := st.chat_input("Type your message here..."):
        # Add user message and rerun to show it first
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

if __name__ == "__main__":
    main()
