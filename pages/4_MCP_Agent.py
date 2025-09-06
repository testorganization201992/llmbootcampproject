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
    
    # Enhanced visual styling
    st.markdown("""
    <style>
        /* Enhanced chat styling */
        .stChatMessage {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 15px;
            background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
            border: 1px solid rgba(0, 212, 170, 0.1);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }
        
        /* Enhanced buttons */
        .stButton > button {
            background: linear-gradient(135deg, #00d4aa, #00a883);
            border: none;
            border-radius: 10px;
            color: white;
            font-weight: 600;
            padding: 0.75rem 2rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 212, 170, 0.4);
            background: linear-gradient(135deg, #00e6c0, #00cc99);
        }
        
        /* Enhanced text inputs */
        .stTextInput > div > div > input {
            background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
            border: 2px solid rgba(0, 212, 170, 0.2);
            border-radius: 10px;
            color: #ffffff;
            font-size: 16px;
            padding: 12px;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #00d4aa;
            box-shadow: 0 0 20px rgba(0, 212, 170, 0.3);
        }
        
        /* Enhanced titles */
        h1 {
            background: linear-gradient(135deg, #00d4aa, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            text-shadow: 0 0 30px rgba(0, 212, 170, 0.5);
        }
        
        /* Enhanced info boxes */
        .stInfo {
            background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
            border-left: 4px solid #00d4aa;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 212, 170, 0.2);
        }
        
        /* Enhanced warning boxes */
        .stWarning {
            background: linear-gradient(135deg, #2e2e1e, #3a3a2a);
            border-left: 4px solid #ffaa00;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(255, 170, 0, 0.2);
        }
        
        /* Enhanced error boxes */
        .stError {
            background: linear-gradient(135deg, #2e1e1e, #3a2a2a);
            border-left: 4px solid #ff6b6b;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(255, 107, 107, 0.2);
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
                placeholder="https://example.com/mcp",
                value=mcp_url if mcp_url else "https://example.com/mcp",
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
                with st.chat_message("user", avatar="https://em-content.zobj.net/source/apple/354/man-technologist-medium-skin-tone_1f468-1f3fd-200d-1f4bb.png"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant", avatar="https://em-content.zobj.net/source/apple/354/robot_1f916.png"):
                    st.write(message["content"])

def main():
    """Main application function."""
    setup_page()
    
    # Page title - centered with enhanced styling
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0;'>
        <h1 style='font-size: 3.5rem; margin-bottom: 1rem; text-shadow: 0 0 30px rgba(0, 212, 170, 0.5);'>
            🔧 MCP Agent
        </h1>
        <p style='font-size: 1.2rem; color: #a0a0a0; margin-top: -0.5rem;'>
            Advanced AI agent powered by Model Context Protocol
        </p>
    </div>
    """, unsafe_allow_html=True)
    
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
            with st.chat_message("assistant", avatar="https://em-content.zobj.net/source/apple/354/robot_1f916.png"):
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
    