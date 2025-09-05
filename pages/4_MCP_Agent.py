"""
MCP Agent Chatbot
Demonstrates Model Context Protocol (MCP) integration for enhanced AI capabilities.
Uses MCP server to provide tools and resources beyond standard LLM functionality.
"""

import streamlit as st
import os
import asyncio
from pathlib import Path
from agent_service import get_agent

def setup_page():
    """Set up the page with basic config."""
    st.set_page_config(
        page_title="MCP Agent",
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Force light theme
    st.markdown("""
    <style>
        .stApp {
            background-color: #ffffff !important;
            color: #262730 !important;
        }
        .stApp > div {
            background-color: #ffffff !important;
        }
        [data-testid="stSidebar"] {
            background-color: #f0f2f6 !important;
        }
    </style>
    """, unsafe_allow_html=True)

def configure_mcp_settings():
    """Configure OpenAI API key and MCP URL."""
    api_key = st.session_state.get("mcp_openai_key", "")
    mcp_url = st.session_state.get("mcp_server_url", "")
    
    if not api_key or not mcp_url:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔧 Enter Configuration")
            
            # Check if we just connected (avoid showing form again)
            if st.session_state.get("mcp_keys_connected", False):
                st.session_state["mcp_keys_connected"] = False
                return True
                
            api_key_input = st.text_input(
                "OpenAI API Key",
                type="password",
                placeholder="sk-proj-...",
                value=api_key,
                key="mcp_api_key_input"
            )
                
            mcp_url_input = st.text_input(
                "MCP Server URL",
                placeholder="http://localhost:8000",
                value=mcp_url if mcp_url else "http://localhost:8000",
                key="mcp_url_input"
            )
            
            if st.button("Connect", type="primary", use_container_width=True):
                if api_key_input and api_key_input.startswith("sk-") and mcp_url_input:
                    st.session_state["mcp_openai_key"] = api_key_input
                    st.session_state["mcp_server_url"] = mcp_url_input
                    st.session_state["mcp_keys_connected"] = True
                    st.rerun()
                else:
                    if not api_key_input or not api_key_input.startswith("sk-"):
                        st.error("❌ Please enter a valid OpenAI API key")
                    if not mcp_url_input:
                        st.error("❌ Please enter a valid MCP URL")
        return False
    
    return True

def display_messages():
    """Display chat messages using pure Streamlit components."""
    if not st.session_state.mcp_messages:
        st.info("""🔧 **MCP Agent Ready!** 

Ask me anything! I'm powered by Model Context Protocol.

**I can help with:**
• General questions and conversations
• Using any tools from connected MCP servers
• Accessing enhanced capabilities beyond standard LLM features""")
    else:
        for message in st.session_state.mcp_messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(message["content"])

def main():
    """Main application function."""
    setup_page()
    
    # Page title - centered
    st.markdown("<h1 style='text-align: center; margin-top: -75px;'>🔧 MCP Agent</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Check configuration - Show login screen
    if not configure_mcp_settings():
        return
    
    # Initialize messages with unique key for MCP Agent
    if "mcp_messages" not in st.session_state:
        st.session_state.mcp_messages = []
    
    # Display messages
    display_messages()
    
    # Generate response if needed
    if (st.session_state.mcp_messages and 
        st.session_state.mcp_messages[-1]["role"] == "user" and
        not st.session_state.get("mcp_processing", False)):
        
        st.session_state.mcp_processing = True
        try:
            # Show processing indicator
            with st.chat_message("assistant"):
                with st.spinner("Processing with MCP agent..."):
                    # Get the last user message
                    user_query = st.session_state.mcp_messages[-1]["content"]
                    
                    # Get OpenAI API key
                    openai_api_key = st.session_state.get("mcp_openai_key", "")
                    mcp_server_url = st.session_state.get("mcp_server_url", "")
                    
                    if openai_api_key and mcp_server_url:
                        try:
                            # Create event loop for async MCP agent
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            
                            try:
                                # Get MCP agent instance
                                agent = loop.run_until_complete(
                                    get_agent(openai_api_key, mcp_server_url)
                                )
                                
                                # Prepare messages for agent
                                messages = [{"role": msg["role"], "content": msg["content"]} 
                                          for msg in st.session_state.mcp_messages]
                                
                                # Invoke agent
                                response_text = loop.run_until_complete(agent.invoke(messages))
                                
                            finally:
                                loop.close()
                                
                        except Exception as e:
                            response_text = f"❌ MCP Agent Error: {str(e)}"
                    else:
                        response_text = "❌ Configuration missing. Please check API key and MCP URL."
                    
                    # Add assistant response
                    st.session_state.mcp_messages.append({"role": "assistant", "content": response_text})
            
            st.session_state.mcp_processing = False
            st.rerun()
            
        except Exception as e:
            st.session_state.mcp_processing = False
            st.error(f"Error: {str(e)}")
            st.rerun()

    # Chat input - outside container to prevent shifting
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message and rerun to show it first
        st.session_state.mcp_messages.append({"role": "user", "content": prompt})
        st.rerun()

if __name__ == "__main__":
    main()
    