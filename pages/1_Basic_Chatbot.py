"""Basic Chatbot Page.

A modern, conversational AI chatbot with customizable response styles
and conversation memory. Features a clean interface with enhanced styling
and reliable message processing.
"""

import streamlit as st
from config.api_config import get_openai_api_key, display_missing_keys_error
from utils.langchain_helpers import BasicChatbotHelper
from ui_components.home_ui import ChatbotUI


def main():
    """Main chatbot function - simplified with environment variables."""
    # Setup page
    ChatbotUI.setup_page("AI Chat", "🚀")
    ChatbotUI.render_page_header(
        "🚀", 
        "Basic Chatbot", 
        "AI conversation assistant with memory"
    )
    
    # API key handling
    try:
        api_key = get_openai_api_key()
    except ValueError as e:
        st.error(f"❌ {e}")
        display_missing_keys_error(["OPENAI_API_KEY"])
        return
    
    # Initialize chain once
    if "basic_chain" not in st.session_state:
        config = BasicChatbotHelper.get_default_config()
        st.session_state.basic_chain = BasicChatbotHelper.build_chain(config, api_key)
    
    # Initialize messages and processing flag
    if "basic_messages" not in st.session_state:
        st.session_state.basic_messages = []
    if "processing" not in st.session_state:
        st.session_state.processing = False
    
    # Display all messages
    for message in st.session_state.basic_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if not st.session_state.basic_messages:
        st.info("🤖 Ask me anything and I'll be happy to help!")
    
    # Show processing state if needed
    if st.session_state.processing:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Get the last user message
                    last_user_msg = next((msg["content"] for msg in reversed(st.session_state.basic_messages) if msg["role"] == "user"), "")
                    
                    response = BasicChatbotHelper.invoke_with_memory(
                        st.session_state.basic_chain, 
                        last_user_msg, 
                        st.session_state.basic_messages[:-1]  # Exclude the last user message for memory
                    )
                    st.markdown(response.content)
                    st.session_state.basic_messages.append({
                        "role": "assistant", 
                        "content": response.content
                    })
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.basic_messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
                finally:
                    st.session_state.processing = False
                    st.rerun()
    
    # Handle user input - only accept new input when not processing
    if prompt := st.chat_input("Type your message here..."):
        if not st.session_state.processing:
            # Add user message and set processing flag
            st.session_state.basic_messages.append({"role": "user", "content": prompt})
            st.session_state.processing = True
            st.rerun()


if __name__ == "__main__":
    main()