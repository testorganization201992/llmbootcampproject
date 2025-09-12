"""Agent Chatbot Page.

AI agent with real-time web search capabilities using Tavily API.
Features intelligent web search integration and streaming responses
for current information and real-time data queries.
"""

import streamlit as st
import asyncio
from config.api_config import get_openai_api_key, get_tavily_api_key, display_missing_keys_error
from utils.langchain_helpers import AgentChatbotHelper
from ui_components.home_ui import ChatbotUI


def main():
    """Main agent chatbot function."""
    # Setup page
    ChatbotUI.setup_page("Agent Chat", "🔍")
    ChatbotUI.render_page_header(
        "🔍", 
        "Search Enabled Chat", 
        "AI with internet search capabilities"
    )
    
    # Validate API keys
    try:
        openai_key = get_openai_api_key()
        tavily_key = get_tavily_api_key()
    except ValueError as e:
        st.error(f"❌ {e}")
        display_missing_keys_error(["OPENAI_API_KEY", "TAVILY_API_KEY"])
        return
    
    # Initialize agent service
    if "agent_service" not in st.session_state:
        st.session_state.agent_service = AgentChatbotHelper.setup_agent(openai_key, tavily_key)
    
    # Initialize messages and processing flag
    if "agent_messages" not in st.session_state:
        st.session_state.agent_messages = []
    if "agent_processing" not in st.session_state:
        st.session_state.agent_processing = False
    
    # Display all messages
    for message in st.session_state.agent_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if not st.session_state.agent_messages:
        st.info("🔍 Ask me anything and I'll search the web for current information!")
    
    # Show processing state if needed
    if st.session_state.agent_processing:
        with st.chat_message("assistant"):
            with st.spinner("Searching and thinking..."):
                try:
                    # Get the last user message
                    last_user_msg = next((msg["content"] for msg in reversed(st.session_state.agent_messages) if msg["role"] == "user"), "")
                    
                    # Process query through agent with search capabilities
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        response = loop.run_until_complete(
                            AgentChatbotHelper.process_agent_response(st.session_state.agent_service, last_user_msg)
                        )
                    finally:
                        loop.close()
                    
                    st.markdown(response)
                    st.session_state.agent_messages.append({
                        "role": "assistant", 
                        "content": response
                    })
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.agent_messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
                finally:
                    st.session_state.agent_processing = False
                    st.rerun()
    
    # Handle user input - only accept new input when not processing
    if prompt := st.chat_input("Ask me anything..."):
        if not st.session_state.agent_processing:
            # Add user message and set processing flag
            st.session_state.agent_messages.append({"role": "user", "content": prompt})
            st.session_state.agent_processing = True
            st.rerun()


if __name__ == "__main__":
    main()
