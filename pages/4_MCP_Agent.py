"""MCP Agent Chatbot Page.

Demonstrates Model Context Protocol (MCP) integration for enhanced AI capabilities.
Connects to MCP servers to provide specialized tools and resources beyond standard
LLM functionality, enabling extensible and context-aware AI interactions.
"""

import streamlit as st
import asyncio
from config.api_config import get_openai_api_key, get_mcp_config, get_user_mcp_server_url, display_missing_keys_error, setup_api_keys_ui
from services.agent_service import get_agent
from ui_components.home_ui import ChatbotUI


def check_mcp_server_running(mcp_config):
    """Check if MCP server process is running."""
    import requests
    try:
        # Try to connect to the server
        response = requests.get(f"{mcp_config['server_url']}/", timeout=2)
        return True
    except:
        return False

def display_mcp_server_status(mcp_config):
    """Display MCP server connection status."""
    with st.container():
        left_spacer, col1, col2 = st.columns([1, 3, 1])
        
        with col1:
            st.markdown("""
**MCP Server:**
                        
Ask me anything! I'm powered by Model Context Protocol.  

**I can help with:**  
- General questions and conversations  
- Using any tools from connected MCP servers  
- Accessing enhanced capabilities beyond standard LLM features
""")
            # mcp_config['server_url']
        
        with col2:
            if check_mcp_server_running(mcp_config):
                st.success("🟢 Online")
                return True
            else:
                st.error("🔴 Offline")
                
        if not check_mcp_server_running(mcp_config):
            st.warning("⚠️ MCP Server not responding. Start server with: `python server.py`")
            return False
    return True

def main():
    """Main MCP agent function."""
    # Setup page
    ChatbotUI.setup_page("MCP Agent", "🔧")
    
    # Setup API keys UI
    api_keys_configured = setup_api_keys_ui()

    # Add logo to the sidebar
    ChatbotUI.add_sidebar_logo()
    
    # Only proceed if API keys are configured
    if not api_keys_configured:
        st.info("👈 Please configure your API keys and MCP server in the sidebar to use the chatbot")
        return
    
    ChatbotUI.render_page_header(
        "🔧", 
        "MCP Chatbot", 
        "Model Context Protocol integration with specialized tools"
    )
    
    # Validate API keys and MCP server URL
    try:
        openai_key = get_openai_api_key()
    except ValueError as e:
        st.error(f"❌ {e}")
        display_missing_keys_error(["OPENAI_API_KEY"], include_mcp_info=True)
        return
    
    # Validate MCP server URL
    try:
        mcp_server_url = get_user_mcp_server_url()
    except ValueError as e:
        st.error(f"❌ {e}")
        display_missing_keys_error(["MCP_SERVER_URL"], include_mcp_info=True)
        return
    
    # Get MCP configuration
    mcp_config = get_mcp_config()
    
    # Display MCP server status
    if not display_mcp_server_status(mcp_config):
        st.info("💡 Start the MCP server to enable specialized AI tools and capabilities")
        return
    
    # Initialize MCP agent
    if "mcp_agent" not in st.session_state:
        with st.spinner("Initializing MCP agent..."):
            try:
                # Create async event loop for MCP agent initialization
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    st.session_state.mcp_agent = loop.run_until_complete(
                        get_agent(openai_key, mcp_config["server_url"])
                    )
                    st.success("✅ MCP Agent initialized successfully!")
                finally:
                    loop.close()
            except Exception as e:
                st.error(f"❌ Failed to initialize MCP agent: {str(e)}")
                st.info("💡 Make sure the MCP server is running: `python server.py`")
                return
    
    # Initialize messages and processing flag
    if "mcp_messages" not in st.session_state:
        st.session_state.mcp_messages = []
    if "mcp_processing" not in st.session_state:
        st.session_state.mcp_processing = False
    
    # Display all messages
    for message in st.session_state.mcp_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if not st.session_state.mcp_messages:
        st.info("🔧 Ask me anything! I have access to specialized tools through MCP for enhanced capabilities.")
    
    # Show processing state if needed
    if st.session_state.mcp_processing:
        with st.chat_message("assistant"):
            with st.spinner("Processing with MCP tools..."):
                try:
                    # Get the last user message
                    last_user_msg = next((msg["content"] for msg in reversed(st.session_state.mcp_messages) if msg["role"] == "user"), "")
                    
                    # Format messages for MCP agent
                    formatted_messages = [
                        {"role": msg["role"], "content": msg["content"]} 
                        for msg in st.session_state.mcp_messages
                    ]
                    
                    # Process through MCP agent
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        response = loop.run_until_complete(
                            st.session_state.mcp_agent.invoke(formatted_messages)
                        )
                    finally:
                        loop.close()
                    
                    st.markdown(response)
                    st.session_state.mcp_messages.append({
                        "role": "assistant", 
                        "content": response
                    })
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.mcp_messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
                finally:
                    st.session_state.mcp_processing = False
                    st.rerun()
    
    # Handle user input - only accept new input when not processing
    if prompt := st.chat_input("Ask me anything..."):
        if not st.session_state.mcp_processing:
            # Add user message and set processing flag
            st.session_state.mcp_messages.append({"role": "user", "content": prompt})
            st.session_state.mcp_processing = True
            st.rerun()


if __name__ == "__main__":
    main()
    