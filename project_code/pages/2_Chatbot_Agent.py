import streamlit as st
import os
from ui_components import ChatbotUI, APIKeyUI
from langchain_helpers import AgentChatbotHelper, ValidationHelper
import asyncio

# Use centralized UI setup - no need for separate function
    

def configure_api_keys():
    """Configure OpenAI and Tavily API keys."""
    openai_key = st.session_state.get("agent_openai_key", "")
    tavily_key = st.session_state.get("agent_tavily_key", "")
    
    if not openai_key or not tavily_key:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔑 Enter API Keys")
            
            # Check if we just connected (avoid showing form again)
            if st.session_state.get("agent_keys_connected", False):
                st.session_state["agent_keys_connected"] = False
                return True
                
            if not openai_key:
                openai_input = st.text_input(
                    "OpenAI API Key",
                    type="password",
                    placeholder="sk-proj-...",
                    key="agent_openai_input"
                )
            else:
                openai_input = openai_key
                st.success("✅ OpenAI API key configured")
            
            tavily_input = st.text_input(
                "Tavily API Key", 
                type="password",
                placeholder="tvly-...",
                key="agent_tavily_input"
            )
            
            if st.button("Connect", type="primary", use_container_width=True):
                valid_openai = ValidationHelper.validate_openai_key(openai_input)
                valid_tavily = ValidationHelper.validate_tavily_key(tavily_input)
                
                if valid_openai and valid_tavily:
                    st.session_state["agent_openai_key"] = openai_input
                    st.session_state["agent_tavily_key"] = tavily_input
                    st.session_state["agent_keys_connected"] = True
                    st.rerun()
                else:
                    if not valid_openai:
                        st.error("❌ Invalid OpenAI key format")
                    if not valid_tavily:
                        st.error("❌ Invalid Tavily key format")
        return False
    
    return True

class ChatbotTools:
    def __init__(self):
        pass

    def setup_agent(self):
        openai_key = st.session_state.get("agent_openai_key", "")
        tavily_key = st.session_state.get("agent_tavily_key", "")
        return AgentChatbotHelper.setup_agent(openai_key, tavily_key)
    
    def display_messages(self):
        """Display chat messages using pure Streamlit components."""
        if not st.session_state.agent_messages:
            st.info("🌐 Ask me anything and I'll search the web for real-time information!")
        else:
            for message in st.session_state.agent_messages:
                if message["role"] == "user":
                    with st.chat_message("user", avatar="https://em-content.zobj.net/source/apple/354/man-technologist-medium-skin-tone_1f468-1f3fd-200d-1f4bb.png"):
                        st.write(message["content"])
                else:
                    with st.chat_message("assistant", avatar="https://em-content.zobj.net/source/apple/354/robot_1f916.png"):
                        st.write(message["content"])

    def main(self):
        # Initialize messages with unique key
        if "agent_messages" not in st.session_state:
            st.session_state.agent_messages = []
            
        # Setup agent
        agent = self.setup_agent()
        
        # Display messages
        self.display_messages()
        
        # Generate response if needed
        if (st.session_state.agent_messages and 
            st.session_state.agent_messages[-1]["role"] == "user" and
            not st.session_state.get("agent_processing", False)):
            
            st.session_state.agent_processing = True
            try:
                # Show processing indicator
                with st.chat_message("assistant", avatar="https://em-content.zobj.net/source/apple/354/robot_1f916.png"):
                    with st.spinner("Searching the web..."):
                        # Get the last user message
                        user_query = st.session_state.agent_messages[-1]["content"]
                        
                        # Process with helper function
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        try:
                            response = loop.run_until_complete(
                                AgentChatbotHelper.process_agent_response(agent, user_query)
                            )
                        finally:
                            loop.close()
                        
                        # Add assistant response
                        st.session_state.agent_messages.append({"role": "assistant", "content": response})
                
                st.session_state.agent_processing = False
                st.rerun()
                
            except Exception as e:
                st.session_state.agent_processing = False
                st.error(f"Error: {str(e)}")
                st.rerun()
        
        # Chat input - outside container to prevent shifting
        if prompt := st.chat_input("Ask me anything about current events..."):
            # Add user message and rerun to show it first
            st.session_state.agent_messages.append({"role": "user", "content": prompt})
            st.rerun()


def main():
    """Main application function."""
    # Use centralized UI setup and header
    ChatbotUI.setup_page("Agent Chatbot", "🌐")
    ChatbotUI.render_page_header(
        "🌐", 
        "Chatbot Agent", 
        "AI agent with real-time web search capabilities"
    )
    
    # Check API keys - Show login screen
    if not configure_api_keys():
        return
    
    # Run chatbot
    obj = ChatbotTools()
    obj.main()

if __name__ == "__main__":
    main()
