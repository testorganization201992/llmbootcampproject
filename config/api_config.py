"""API Configuration for both local development and Streamlit Cloud deployment.

Supports two modes:
- Local development: Uses .env file for automatic API key loading
- Cloud deployment: Requires users to input their own API keys for security and cost control
"""
import os
import streamlit as st
from dotenv import load_dotenv

def is_local_development():
    """Safely detect if running in local development environment."""
    # Check for .env file (most reliable indicator of local dev)
    if os.path.exists('.env'):
        return True
    
    # Check for common local development indicators
    local_indicators = [
        'localhost' in os.environ.get('SERVER_NAME', ''),
        'localhost' in os.environ.get('HTTP_HOST', ''),
        os.environ.get('ENVIRONMENT') == 'local',
        os.environ.get('STREAMLIT_ENV') == 'development'
    ]
    
    return any(local_indicators)

def is_streamlit_cloud():
    """Safely detect if running on Streamlit Cloud."""
    try:
        # Try to access secrets without triggering error
        import streamlit as st
        # Check for Streamlit Cloud environment variables
        cloud_indicators = [
            'streamlit.io' in os.environ.get('SERVER_NAME', ''),
            os.environ.get('STREAMLIT_SHARING') == 'true',
            os.environ.get('STREAMLIT_CLOUD') == 'true'
        ]
        return any(cloud_indicators)
    except:
        return False

def get_streamlit_secret(key, default=None):
    """Safely get a Streamlit secret without causing errors."""
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError, Exception):
        return default

# Load environment variables only for local development
if is_local_development():
    load_dotenv()

def get_user_api_keys():
    """Get API keys and MCP server URL from user input or local environment.
    
    Returns:
        dict: Contains API keys, MCP server URL, and local environment status
    """
    # For local development, use .env file
    if is_local_development():
        return {
            "openai": os.getenv("OPENAI_API_KEY"),
            "tavily": os.getenv("TAVILY_API_KEY"),
            "mcp_server_url": os.getenv("MCP_SERVER_URL", "http://localhost:8000"),
            "has_local_keys": True
        }
    
    # For cloud deployment, require user input
    return {
        "openai": None,
        "tavily": None,
        "mcp_server_url": None,
        "has_local_keys": False
    }

def setup_api_keys_ui():
    """Setup UI for users to input their API keys and MCP server URL.
    
    Returns:
        bool: True if API keys are properly configured
    """
    user_keys = get_user_api_keys()
    
    # If running locally with .env file, use those keys
    if user_keys["has_local_keys"] and user_keys["openai"]:
        st.session_state.user_openai_key = user_keys["openai"]
        st.session_state.user_tavily_key = user_keys["tavily"]
        st.session_state.user_mcp_server_url = user_keys["mcp_server_url"]
        
        # Show local development status in sidebar
        with st.sidebar:
            st.markdown("### 🔑 API Configuration")
            st.success("🏠 Local Development Mode")
            st.info("Using keys from .env file")
            st.markdown("🟢 **OpenAI**: Connected")
            st.markdown("🟢 **Tavily**: Connected")
            st.markdown("🟢 **MCP Server**: Configured")
            st.markdown("---")
        
        return True
    
    # Otherwise, show input form for cloud deployment
    with st.sidebar:
        st.markdown("### 🔑 API Configuration")
        st.markdown("Enter your API keys and MCP server URL:")
        
        # OpenAI API Key
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=st.session_state.get("user_openai_key", ""),
            help="Get your key from https://platform.openai.com/api-keys",
            placeholder="sk-proj-..."
        )
        
        # Tavily API Key
        tavily_key = st.text_input(
            "Tavily API Key (for web search)",
            type="password", 
            value=st.session_state.get("user_tavily_key", ""),
            help="Get your key from https://tavily.com/",
            placeholder="tvly-..."
        )
        
        # MCP Server URL
        mcp_server_url = st.text_input(
            "MCP Server URL (for advanced tools)",
            value=st.session_state.get("user_mcp_server_url", ""),
            help="URL of your deployed MCP server (e.g., https://your-mcp-server.com)",
            placeholder="https://your-mcp-server.com"
        )
        
        # Save button
        if st.button("💾 Save Configuration", use_container_width=True):
            success_count = 0
            
            # Validate OpenAI key
            if openai_key and openai_key.startswith("sk-"):
                st.session_state.user_openai_key = openai_key
                success_count += 1
            elif openai_key:
                st.error("❌ Please enter a valid OpenAI key (starts with 'sk-')")
                
            # Validate Tavily key
            if tavily_key and tavily_key.startswith("tvly-"):
                st.session_state.user_tavily_key = tavily_key
                success_count += 1
            elif tavily_key:
                st.error("❌ Please enter a valid Tavily key (starts with 'tvly-')")
                
            # Validate MCP Server URL
            if mcp_server_url and (mcp_server_url.startswith("http://") or mcp_server_url.startswith("https://")):
                st.session_state.user_mcp_server_url = mcp_server_url
                success_count += 1
            elif mcp_server_url:
                st.error("❌ Please enter a valid URL (starts with 'http://' or 'https://')")
            
            if success_count > 0:
                st.success(f"✅ {success_count} configuration(s) saved!")
        
        # Show current status
        st.markdown("**Status:**")
        if "user_openai_key" in st.session_state:
            st.markdown("🟢 **OpenAI**: Connected")
        else:
            st.markdown("🟡 **OpenAI**: Not configured")
            
        if "user_tavily_key" in st.session_state:
            st.markdown("🟢 **Tavily**: Connected")
        else:
            st.markdown("🟡 **Tavily**: Not configured")
            
        if "user_mcp_server_url" in st.session_state:
            st.markdown("🟢 **MCP Server**: Configured")
        else:
            st.markdown("🟡 **MCP Server**: Not configured")
        
        st.markdown("---")
    
    return "user_openai_key" in st.session_state

def get_openai_api_key():
    """Get OpenAI API key from user session or raise error.
    
    Returns:
        str: OpenAI API key
        
    Raises:
        ValueError: If API key is not configured
    """
    if "user_openai_key" not in st.session_state:
        raise ValueError("Please configure your OpenAI API key in the sidebar")
    return st.session_state.user_openai_key

def get_tavily_api_key():
    """Get Tavily API key from user session or raise error.
    
    Returns:
        str: Tavily API key
        
    Raises:
        ValueError: If API key is not configured
    """
    if "user_tavily_key" not in st.session_state:
        raise ValueError("Please configure your Tavily API key in the sidebar")
    return st.session_state.user_tavily_key

def get_user_mcp_server_url():
    """Get MCP Server URL from user session or return default.
    
    Returns:
        str: MCP server URL
        
    Raises:
        ValueError: If MCP server URL is not configured for cloud deployment
    """
    if "user_mcp_server_url" not in st.session_state:
        # For local development, return default
        if is_local_development():
            return "http://localhost:8000"
        else:
            raise ValueError("Please configure your MCP Server URL in the sidebar")
    return st.session_state.user_mcp_server_url

def get_mcp_server_url():
    """Get MCP Server URL from user configuration or environment variables.
    
    Returns:
        str: MCP server URL
    """
    try:
        return get_user_mcp_server_url()
    except ValueError:
        # Fallback to environment variables or default
        if is_streamlit_cloud():
            url = get_streamlit_secret("MCP_SERVER_URL")
            if url:
                return url
        
        # Fall back to environment variables (for local development)
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
    st.error("❌ Configuration Required")
    st.info("👈 Please configure the required settings in the sidebar to continue")
    
    with st.expander("🔗 Where to get API keys"):
        st.markdown("- **OpenAI**: https://platform.openai.com/api-keys")
        st.markdown("- **Tavily**: https://tavily.com/ (free tier available)")
        if include_mcp_info:
            st.markdown("- **MCP Server**: Deploy your own or use a public server")
        
    with st.expander("💡 Why do I need my own configuration?"):
        st.markdown("""
        - **Cost Control**: You control your usage and costs
        - **Rate Limits**: Your personal rate limits, not shared
        - **Privacy**: Your conversations stay with your account
        - **Reliability**: No dependency on shared resources
        - **Flexibility**: Use your preferred MCP server deployment
        """)
    
    with st.expander("💰 Estimated API Costs"):
        st.markdown("""
        **OpenAI GPT-4 Pricing (approximate):**
        - Basic chat: ~$0.01-0.05 per conversation
        - Document analysis: ~$0.05-0.20 per document
        - Web search agent: ~$0.02-0.10 per query
        
        **Tavily Search:**
        - Free tier: 1,000 searches/month
        - Pro: $0.005 per search
        
        **MCP Server:**
        - Self-hosted: Only server hosting costs
        - Public servers: Varies by provider
        """)
    
    if include_mcp_info:
        with st.expander("🚀 MCP Server Quick Setup"):
            st.markdown("""
            **Option 1: Quick Deploy (Recommended)**
            1. Fork this repository
            2. Deploy on Railway/Render/Heroku
            3. Use the deployment URL here
            
            **Option 2: Local Development**
            1. Run `python server.py` locally
            2. Use `http://localhost:8000`
            
            **Option 3: Public Server**
            1. Find a compatible MCP server
            2. Ensure it has `/health` and `/optimize` endpoints
            """)

def show_getting_started_info():
    """Show getting started information when API keys are not configured."""
    st.markdown("### 🚀 Getting Started")
    st.info("👈 Configure your API keys and MCP server in the sidebar to access all AI assistants")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔑 Required Configuration")
        st.markdown("- **OpenAI API Key**: For all AI chat functionality")
        st.markdown("- **Tavily API Key**: For web search capabilities")
        st.markdown("- **MCP Server URL**: For advanced tool integration")
        
        st.markdown("#### 🆓 Free Tiers Available")
        st.markdown("- **OpenAI**: $5 free credits for new accounts")
        st.markdown("- **Tavily**: 1,000 free searches/month")
    
    with col2:
        st.markdown("#### 💡 Why Your Own Configuration?")
        st.markdown("- Full control over usage and costs")
        st.markdown("- Better privacy and security")
        st.markdown("- Personal rate limits")
        st.markdown("- Professional development practice")
        
        st.markdown("#### 🔒 Security")
        st.markdown("- Keys stored only in your browser session")
        st.markdown("- No server-side storage")
        st.markdown("- Clear when you close the browser")
    
    with st.expander("🛠️ MCP Server Deployment Options"):
        st.markdown("""
        **For MCP Agent functionality, you can:**
        
        1. **Deploy your own MCP server** (recommended):
           - Use services like Railway, Render, or Heroku
           - Deploy the `server.py` file from this project
           - Use the deployment URL in the configuration
        
        2. **Run locally** (for development):
           - Run `python server.py` in your local environment
           - Use `http://localhost:8000` as the server URL
        
        3. **Use a public MCP server** (if available):
           - Find publicly available MCP servers
           - Ensure they support the required endpoints
        """)
        
        st.markdown("**Example deployment commands:**")
        st.code("""
# For Railway deployment
railway login
railway new
railway add
railway deploy

# For Render deployment  
# Connect your GitHub repo to Render
# Set build command: pip install -r requirements.txt
# Set start command: python server.py
        """, language="bash")

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
