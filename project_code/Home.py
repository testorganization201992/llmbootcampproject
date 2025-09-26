import streamlit as st
import os
import glob
from ui_components import HomePageUI

st.set_page_config(
    page_title="LLM Bootcamp Project",
    page_icon=\'🤖\',
    layout=\'wide\',
    initial_sidebar_state="expanded"
)


# Apply centralized home page styling
HomePageUI.apply_home_styling()

# Render hero section using centralized component
HomePageUI.render_hero_section()

st.markdown("### Available AI Assistants:")

    # Enhanced feature list using centralized components
    st.markdown("""
    <div class="feature-list">
        <h3 style="color: #00d4aa; margin-bottom: 1.5rem; text-align: center;">✨ Available Features</h3>
    </div>
    """, unsafe_allow_html=True)
    


