"""Application configuration settings"""
import streamlit as st

def setup_page_config():
    st.set_page_config(
        page_title="LLM Bootcamp Project",
        page_icon='🤖',
        layout='wide',
        initial_sidebar_state="expanded"
    )

PAGE_CONFIG = {
    '1_basic': {'icon': '💬', 'title': 'Basic AI Chat', 'description': 'Simple AI conversation'},
    '2_chatbot_agent': {'icon': '🔍', 'title': 'Search Enabled Chat', 'description': 'AI with internet search capabilities'},
    '3_chat_with_your_data': {'icon': '📚', 'title': 'RAG', 'description': 'Retrieval-Augmented Generation with documents'},
    '4_mcp_agent': {'icon': '🔧', 'title': 'MCP Chatbot', 'description': 'Model Context Protocol integration'}
}