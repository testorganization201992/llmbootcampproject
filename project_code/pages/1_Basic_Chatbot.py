"""
Modern Beautiful Chatbot
A sleek, modern chatbot with the best appearance and functionality.
"""

import streamlit as st
import os
from ui_components import ChatbotUI, APIKeyUI
from langchain_helpers import BasicChatbotHelper, ValidationHelper
    


def configure_api_key():
    """Configure OpenAI API key."""
    api_key = st.session_state.get("basic_openai_key", "")
    
    if not api_key:
        # Check if we just connected (avoid showing form again)
        if st.session_state.get("basic_api_key_connected", False):
            st.session_state["basic_api_key_connected"] = False
            return True
        
        # Use centralized API key form
        inputs = APIKeyUI.render_api_key_form(
            title="🔑 Enter API Key",
            inputs=[{
                "key": "basic_api_key_input",
                "label": "OpenAI API Key",
                "placeholder": "sk-proj-...",
                "password": True
            }]
        )
        
        if inputs:
            api_key_input = inputs.get("basic_api_key_input", "")
            if ValidationHelper.validate_openai_key(api_key_input):
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
        
        # Simple chain with default configuration
        config = BasicChatbotHelper.get_default_config()
        api_key = st.session_state.get("basic_openai_key", "")
        
        # Always recreate chain if API key exists and chain doesn't exist or API key changed
        if api_key and ("basic_chain" not in st.session_state or 
                       st.session_state.get("basic_current_api_key") != api_key):
            st.session_state.basic_chain = BasicChatbotHelper.build_chain(config, api_key)
            st.session_state.basic_current_api_key = api_key
        elif not api_key:
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
                # Show processing indicator
                with st.chat_message("assistant", avatar="https://em-content.zobj.net/source/apple/354/robot_1f916.png"):
                    with st.spinner("Thinking..."):
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
                st.error(f"Error: {str(e)}")
                st.rerun()

    # Chat input - outside container to prevent shifting
    if prompt := st.chat_input("Type your message here..."):
        # Add user message and rerun to show it first
        st.session_state.basic_messages.append({"role": "user", "content": prompt})
        st.rerun()

if __name__ == "__main__":
    main()