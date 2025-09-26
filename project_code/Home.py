import streamlit as st
import os
from ui_components import HomePageUI

st.set_page_config(
    page_title="LLM Bootcamp Project",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Apply centralized home page styling
HomePageUI.apply_home_styling()

# Render hero section using centralized component
HomePageUI.render_hero_section()

st.markdown("### Available AI Assistants:")

# Explicitly defined page configurations
pages = [
    {"icon": "💬", "title": "Basic AI Chat", "description": "Simple AI conversation", "file": "pages/1_basic.py"},
    {"icon": "🔍", "title": "Search Enabled Chat", "description": "AI with internet search capabilities", "file": "pages/2_chatbot_agent.py"},
    {"icon": "📚", "title": "RAG", "description": "Retrieval-Augmented Generation with documents", "file": "pages/3_chat_with_your_data.py"},
    {"icon": "🔧", "title": "MCP Chatbot", "description": "Model Context Protocol integration", "file": "pages/4_mcp_agent.py"},
]

# Create columns based on number of pages
num_pages = len(pages)
cols = st.columns(num_pages)

for i, page_info in enumerate(pages):
    with cols[i]:
        button_text = f"{page_info["icon"]} {page_info["title"]}"
        
        if st.button(button_text, key=page_info["file"], use_container_width=True):
            st.switch_page(page_info["file"])

# Enhanced feature list using centralized components
st.markdown("""
<div class="feature-list">
    <h3 style="color: #00d4aa; margin-bottom: 1.5rem; text-align: center;">✨ Available Features</h3>
</div>
""", unsafe_allow_html=True)

for page_info in pages:
    HomePageUI.render_feature_card(page_info["icon"], page_info["title"], page_info["description"])

