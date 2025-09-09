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
                    st.session_state["basic_openai_key"] = api_key_input
                    st.session_state["basic_api_key_connected"] = True
                    st.rerun()
                else:
                    st.error("❌ Invalid key format")
        return False
    
    return True

def display_messages():
    """Display chat messages using centralized UI components."""
    if not ChatbotUI.display_chat_messages(st.session_state.basic_messages):
        st.info("🤖 Ask me anything and I'll be happy to help!")

def main():
    """Main application function."""
    # Use centralized UI setup
    ChatbotUI.setup_page("Modern AI Chat", "🚀")
    
    # Use centralized header component
    ChatbotUI.render_page_header(
        "🚀", 
        "Basic Chatbot", 
        "Your intelligent AI conversation partner with memory"
    )
    
    # Check API key - Show login screen
    if not configure_api_key():
        return
    
    
    # Main chat container
    with st.container():
        
        # Create personality selector in sidebar
        st.sidebar.markdown("### 🎭 Choose AI Personality")
        config_type = st.sidebar.selectbox(
            "Pick your AI's vibe:",
            ["Default", "Creative", "Analytical", "Conversational"],
            key="basic_config_type"
        )

        # Map personalities to configs
        config_map = {
            "Default": BasicChatbotHelper.get_default_config(),
            "Creative": BasicChatbotHelper.get_creative_config(),
            "Analytical": BasicChatbotHelper.get_analytical_config(), 
            "Conversational": BasicChatbotHelper.get_conversational_config()
        }

        config = config_map[config_type]

        # Show what's under the hood
        with st.sidebar.expander("🔧 Current Settings"):
            st.json(config)
        
        # Add smart memory toggle
        use_smart_memory = st.sidebar.checkbox(
            "🧠 Enable Smart Memory", 
            help="AI will remember things about you and summarize conversations"
        )

        if use_smart_memory:
            # Initialize smart memory state
            if "smart_memory_state" not in st.session_state:
                st.session_state.smart_memory_state = {
                    "messages": [],
                    "user_info": {},
                    "conversation_summary": ""
                }
            
            # Show what the AI remembers about you
            with st.sidebar.expander("🧠 What I Remember"):
                memory_state = st.session_state.smart_memory_state
                
                if memory_state["user_info"]:
                    st.write("**About You:**")
                    for key, value in memory_state["user_info"].items():
                        st.write(f"• {key.title()}: {value}")
                else:
                    st.write("I don't know much about you yet!")
                
                if memory_state["conversation_summary"]:
                    st.write("**Our Conversation:**")
                    st.write(memory_state["conversation_summary"])
        
        api_key = st.session_state.get("basic_openai_key", "")
        
        # Always recreate chain if API key exists and chain doesn't exist or API key changed
        if use_smart_memory:
            # Build smart memory chain if needed
            if api_key and ("smart_memory_chain" not in st.session_state or 
                           st.session_state.get("smart_memory_config") != config_type):
                st.session_state.smart_memory_chain = BasicChatbotHelper.build_smart_memory_chain(config, api_key)
                st.session_state.smart_memory_config = config_type
        else:
            # Regular chain
            if api_key and ("basic_chain" not in st.session_state or 
                           st.session_state.get("basic_current_api_key") != api_key or
                           st.session_state.get("basic_current_config") != config_type):
                st.session_state.basic_chain = BasicChatbotHelper.build_chain(config, api_key)
                st.session_state.basic_current_api_key = api_key
                st.session_state.basic_current_config = config_type
        
        if not api_key:
            st.error("API key not found. Please refresh the page.")
            return
        
        # Initialize messages with unique key
        if "basic_messages" not in st.session_state:
            st.session_state.basic_messages = []
        
        # Display messages
        display_messages()
        
        # Generate response if needed
        if (st.session_state.basic_messages and 
            st.session_state.basic_messages[-1]["role"] == "user" and
            not st.session_state.get("basic_processing", False)):
            
            st.session_state.basic_processing = True
            try:
                if use_smart_memory and "smart_memory_chain" in st.session_state:
                    # Smart Memory Processing
                    avatar = "🧠"
                    spinner_text = "Thinking and remembering..."
                    
                    with st.chat_message("assistant", avatar=avatar):
                        with st.spinner(spinner_text):
                            user_input = st.session_state.basic_messages[-1]["content"]
                            
                            # Prepare state for LangGraph
                            current_state = st.session_state.smart_memory_state.copy()
                            current_state["current_input"] = user_input
                            
                            # Run through the smart memory graph
                            result = st.session_state.smart_memory_chain.invoke(current_state)
                            
                            # Get the response
                            response_content = result["response"]
                            
                            # Update our memory state
                            st.session_state.smart_memory_state["messages"] = current_state["messages"] + [
                                {"role": "user", "content": user_input},
                                {"role": "assistant", "content": response_content}
                            ]
                            st.session_state.smart_memory_state["user_info"] = result.get("user_info", {})
                            st.session_state.smart_memory_state["conversation_summary"] = result.get("conversation_summary", "")
                            
                            # Add to display
                            st.session_state.basic_messages.append({
                                "role": "assistant", 
                                "content": response_content
                            })
                else:
                    # Regular processing
                    avatar = "https://em-content.zobj.net/source/apple/354/robot_1f916.png"
                    spinner_text = "Thinking..."
                    
                    with st.chat_message("assistant", avatar=avatar):
                        with st.spinner(spinner_text):
                            # Get the last user message
                            user_input = st.session_state.basic_messages[-1]["content"]
                            response = BasicChatbotHelper.invoke_with_memory(
                                st.session_state.basic_chain, 
                                user_input, 
                                st.session_state.basic_messages
                            )
                            
                            # Add assistant response
                            st.session_state.basic_messages.append({
                                "role": "assistant", 
                                "content": response.content
                            })
                
                st.session_state.basic_processing = False
                st.rerun()
                
            except Exception as e:
                st.session_state.basic_processing = False
                error_type = "Smart Memory Error" if use_smart_memory else "Error"
                st.error(f"{error_type}: {str(e)}")
                st.rerun()

    # Chat input - outside container to prevent shifting
    if prompt := st.chat_input("Type your message here..."):
        # Add user message and rerun to show it first
        st.session_state.basic_messages.append({"role": "user", "content": prompt})
        st.rerun()

if __name__ == "__main__":
    main()
