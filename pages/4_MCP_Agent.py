"""
MCP Agent Chatbot
Demonstrates Model Context Protocol (MCP) integration with dynamic theme switching.
Uses MCP server to provide enhanced capabilities beyond standard LLM functionality.
"""

import streamlit as st
import utils
import json
import asyncio
import sys
import os
from pathlib import Path

sys.path.append('..')
from themes.modern_theme import apply_modern_theme, show_processing_animation

# Add the MCP directory to Python path
mcp_path = Path(__file__).parent.parent / "3_agentic_automation_with_mcp"
sys.path.insert(0, str(mcp_path))

try:
    from agent_service import get_agent
except ImportError:
    st.error("MCP agent_service not found. Please ensure the MCP components are available.")
    st.stop()

st.set_page_config(
    page_title="MCP Agent",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply modern theme
apply_modern_theme()

# Configuration
STATE_FILE = mcp_path / "theme_state.json"

# Define theme configurations  
THEMES = {
    "light": {
        "primary": "#667eea",
        "bg": "#ffffff",
        "secondary_bg": "#f8fafc",
        "text": "#2d3748"
    },
    "dark": {
        "primary": "#667eea", 
        "bg": "#1a202c",
        "secondary_bg": "#2d3748",
        "text": "#f7fafc"
    }
}

class MCPChatbot:
    def __init__(self):
        utils.configure_openai_api_key()
        self.mcp_server_url = "http://localhost:8000"
        
    def get_current_theme(self):
        """Get current theme from shared MCP state file"""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, "r") as f:
                    state = json.load(f)
                    return state.get("theme", "light")
            except Exception:
                pass
        return "light"
    
    def apply_mcp_theme(self):
        """Apply dynamic theme based on MCP state"""
        current_theme = self.get_current_theme()
        theme = THEMES.get(current_theme, THEMES["light"])
        
        st.markdown(f"""
            <style>
                .stApp {{
                    background: linear-gradient(135deg, {theme['bg']} 0%, {theme['secondary_bg']} 100%);
                    color: {theme['text']};
                }}
                .stButton > button {{
                    background: linear-gradient(45deg, {theme['primary']}, #764ba2);
                    color: white;
                    border: none;
                    border-radius: 25px;
                    padding: 0.5rem 2rem;
                    transition: all 0.3s ease;
                }}
                .stButton > button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                }}
                .stTextInput > div > div > input {{
                    background-color: {theme['secondary_bg']};
                    color: {theme['text']};
                    border: 2px solid {theme['primary']};
                    border-radius: 15px;
                }}
                h1, h2, h3 {{
                    color: {theme['primary']};
                }}
                .mcp-status {{
                    background: rgba(102, 126, 234, 0.1);
                    border: 1px solid {theme['primary']};
                    border-radius: 10px;
                    padding: 1rem;
                    margin: 1rem 0;
                }}
            </style>
        """, unsafe_allow_html=True)
        
        return current_theme
    
    def setup_sidebar(self):
        """Setup sidebar with MCP configuration"""
        with st.sidebar:
            st.markdown("### 🔧 MCP Configuration")
            
            # MCP Server Status
            st.markdown("""
                <div class="mcp-status">
                    <h4>🌐 MCP Server</h4>
                    <p>Theme Server: localhost:8000</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Current theme display
            current_theme = self.get_current_theme()
            theme_emoji = "🌙" if current_theme == "dark" else "☀️"
            st.markdown(f"**Current Theme:** {theme_emoji} {current_theme.title()}")
            
            st.markdown("---")
            st.markdown("### 🚀 MCP Features")
            st.markdown("• Dynamic Theme Control")
            st.markdown("• Real-time State Management")
            st.markdown("• Server Communication")
            st.markdown("• Context Protocol Integration")
            
            st.markdown("---")
            st.markdown("### 💡 Try These Commands")
            st.markdown("""
            - "Change to dark theme"
            - "Switch to light theme"  
            - "What theme am I using?"
            - "Show me the current state"
            """)

    def display_messages(self):
        """Display chat messages with modern styling"""
        if not st.session_state.messages:
            st.markdown("""
            <div class="welcome-screen">
                <div class="welcome-icon">🔧</div>
                <h3>MCP Agent Assistant</h3>
                <p>Experience Model Context Protocol with dynamic theme switching!</p>
                <p style="font-size: 0.9em; opacity: 0.8;">Try: "Change to dark theme" or "Switch to light theme"</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="messages-area">', unsafe_allow_html=True)
            for message in st.session_state.messages:
                role = message["role"]
                content = message["content"]
                
                if role == "user":
                    st.markdown(f"""
                    <div class="chat-message user">
                        <div class="message-bubble user">{content}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message assistant">
                        <div class="message-bubble assistant">{content}</div>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    def main(self):
        """Main application function"""
        # Apply MCP theme dynamically
        current_theme = self.apply_mcp_theme()
        
        # Setup sidebar
        self.setup_sidebar()
        
        # Initialize messages
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        # Track theme changes for rerun
        if "last_theme" not in st.session_state:
            st.session_state.last_theme = current_theme
        elif st.session_state.last_theme != current_theme:
            st.session_state.last_theme = current_theme
            st.rerun()
        
        # Display messages
        self.display_messages()
        
        # Chat input
        if user_prompt := st.chat_input("Ask me to change themes or anything else..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            
            # Generate response using MCP agent
            try:
                # Show processing animation
                st.markdown(show_processing_animation(), unsafe_allow_html=True)
                
                # Get OpenAI API key
                openai_api_key = os.environ.get("OPENAI_API_KEY")
                if not openai_api_key:
                    response_text = "⚠️ OpenAI API key not configured. Please set it in the sidebar."
                else:
                    # Create event loop for async MCP agent
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    try:
                        # Get MCP agent instance
                        agent = loop.run_until_complete(
                            get_agent(openai_api_key, self.mcp_server_url)
                        )
                        
                        # Prepare messages for agent
                        messages = [{"role": msg["role"], "content": msg["content"]} 
                                  for msg in st.session_state.messages]
                        
                        # Invoke agent
                        response_text = loop.run_until_complete(agent.invoke(messages))
                        
                    except Exception as e:
                        response_text = f"❌ MCP Agent Error: {str(e)}\n\nMake sure the MCP theme server is running:\n```bash\ncd 3_agentic_automation_with_mcp\nbash run.sh\n```"
                    finally:
                        loop.close()
                
                # Add assistant response
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    chatbot = MCPChatbot()
    chatbot.main()