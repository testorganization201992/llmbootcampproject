"""API Configuration using environment variables.

Simple and clean API key management.
Uses .env file for local development with clear error messages.
"""
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_openai_api_key():
    """Get OpenAI API key from environment variables.
    
    Returns:
        str: OpenAI API key
        
    Raises:
        ValueError: If API key is not found or invalid
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file")
    if not api_key.startswith("sk-"):
        raise ValueError("Invalid OPENAI_API_KEY format (should start with 'sk-')")
    return api_key

def get_tavily_api_key():
    """Get Tavily API key from environment variables.
    
    Returns:
        str: Tavily API key
        
    Raises:
        ValueError: If API key is not found or invalid
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in .env file")
    if not api_key.startswith("tvly-"):
        raise ValueError("Invalid TAVILY_API_KEY format (should start with 'tvly-')")
    return api_key

def get_mcp_server_url():
    """Get MCP Server URL from environment variables.
    
    Returns:
        str: MCP server URL (defaults to localhost:8000 if not specified)
    """
    return os.getenv("MCP_SERVER_URL", "http://localhost:8000")

def get_mcp_config():
    """Get complete MCP configuration.
    
    Returns:
        dict: MCP configuration with server URLs
    """
    server_url = get_mcp_server_url()
    return {
        "server_url": server_url,
        "health_endpoint": f"{server_url}/health",
        "optimize_endpoint": f"{server_url}/optimize"
    }

def display_missing_keys_error(missing_keys, include_mcp_info=False):
    """Display helpful error message for missing API keys.
    
    Args:
        missing_keys: List of missing API key names
        include_mcp_info: Whether to include MCP server setup info
    """
    st.error("❌ Missing API Keys")
    
    st.markdown("**Required API keys not found:**")
    for key in missing_keys:
        st.markdown(f"- `{key}`")
    
    st.markdown("**Setup Instructions:**")
    st.markdown("1. Create a `.env` file in your project root")
    st.markdown("2. Add your API keys:")
    
    env_example = """# .env file
OPENAI_API_KEY=sk-proj-your-openai-key-here
TAVILY_API_KEY=tvly-your-tavily-key-here"""
    
    if include_mcp_info:
        env_example += """
MCP_SERVER_URL=http://localhost:8000"""
    
    st.code(env_example)
    
    st.markdown("3. Restart the application")
    
    with st.expander("🔗 Get API Keys"):
        st.markdown("- **OpenAI**: https://platform.openai.com/api-keys")
        st.markdown("- **Tavily**: https://tavily.com/")
        if include_mcp_info:
            st.markdown("- **MCP Server**: Run `python server.py` to start local server")

def check_required_keys(keys_needed):
    """Check if required API keys are available.
    
    Args:
        keys_needed: List of required keys ('openai', 'tavily', 'mcp')
        
    Returns:
        tuple: (bool success, list missing_keys)
    """
    missing_keys = []
    
    if 'openai' in keys_needed:
        try:
            get_openai_api_key()
        except ValueError:
            missing_keys.append("OPENAI_API_KEY")
    
    if 'tavily' in keys_needed:
        try:
            get_tavily_api_key()
        except ValueError:
            missing_keys.append("TAVILY_API_KEY")
    
    # MCP URL is optional with default fallback
    if 'mcp' in keys_needed:
        mcp_url = get_mcp_server_url()
        if not mcp_url:
            missing_keys.append("MCP_SERVER_URL")
    
    return len(missing_keys) == 0, missing_keys
