import streamlit as st
import json
import asyncio
from pathlib import Path
from agent_service import get_agent

# Configuration
STATE_FILE = Path("theme_state.json")

# Define theme configurations
THEMES = {
    "light": {
        "primary": "#FF4B4B",
        "bg": "#FFFFFF",
        "secondary_bg": "#F0F2F6",
        "text": "#31333F"
    },
    "dark": {
        "primary": "#FF4B4B",
        "bg": "#0E1117",
        "secondary_bg": "#262730",
        "text": "#FFFFFF"
    }
}

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_theme' not in st.session_state:
    st.session_state.current_theme = "light"

# Function to get current theme from shared state
def get_current_theme():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r") as f:
                state = json.load(f)
                return state["theme"]
        except Exception as e:
            st.error(f"Error reading theme state: {str(e)}")
    return "light"

# Get current theme (check on each rerun)
current_theme = get_current_theme()
st.session_state.current_theme = current_theme

# Apply theme via CSS injection
def apply_theme():
    theme = THEMES[st.session_state.current_theme]
    st.markdown(f"""
        <style>
            .stApp {{
                background-color: {theme['bg']};
                color: {theme['text']};
            }}
            .stTextInput > div > div > input,
            .stTextInput > div > div > textarea {{
                color: {theme['text']};
            }}
            .stButton > button {{
                background-color: {theme['primary']};
                color: white;
            }}
            .st-emotion-cache-4oy321 {{
                background-color: {theme['secondary_bg']};
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: {theme['primary']};
            }}
            .stChatMessage {{
                background-color: {theme['secondary_bg']};
            }}
        </style>
    """, unsafe_allow_html=True)

# Apply theme before any UI elements
apply_theme()

# Home button at the top
col1, col2 = st.columns([1, 10])
with col1:
    st.markdown("""
        <button onclick="window.location.href='/'" style="
            background-color: #FF4B4B;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        ">🏠 Home</button>
    """, unsafe_allow_html=True)

with col2:
    st.title("MCP Theme Chatbot")

# Sidebar for settings
with st.sidebar:
    st.subheader("Settings")
    
    # OpenAI API Key input
    st.write("### OpenAI Configuration")
    openai_api_key = st.text_input("OpenAI API Key", type="password", 
                                  help="Enter your OpenAI API key here.")
    
    # MCP Server Configuration
    st.write("### MCP Server")
    mcp_server_url = st.text_input("Theme Server URL", "http://localhost:8000", 
                                  help="URL of your MCP theme server")
    
    # Theme info
    st.write("### Theme Control")
    st.write(f"Current theme: **{st.session_state.current_theme}**")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input handler
if prompt := st.chat_input("Type a message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process with agent if API key is provided
    if openai_api_key:
        try:
            # Create a new event loop for this execution context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Get the agent instance
                agent = loop.run_until_complete(get_agent(openai_api_key, mcp_server_url))
                
                # Invoke the agent
                response_text = loop.run_until_complete(agent.invoke(st.session_state.messages))
                
            finally:
                # Clean up the event loop
                loop.close()
                
        except Exception as e:
            response_text = f"❌ Error with AI agent: {str(e)}"
    else:
        response_text = "⚠️ Please enter your OpenAI API key to enable AI-powered responses."
    
    # Add assistant response to chat
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)
    
    # After agent response, check if theme changed
    current_theme = get_current_theme()
    if current_theme != st.session_state.current_theme:
        st.session_state.current_theme = current_theme
        st.rerun()