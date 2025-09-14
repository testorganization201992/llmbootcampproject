import os
import streamlit as st
from config.app_config import setup_page_config
from config.api_config import setup_api_keys_ui, show_getting_started_info
from utils.page_utils import PageDiscovery
from ui_components.home_ui import HomePageUI

# Configure the app
setup_page_config()

# Setup API keys UI - this will show the key input form or local dev status
api_keys_configured = setup_api_keys_ui()

# Add logo to the sidebar
with st.sidebar:
    # Open a div for centering
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    
    # Use st.image so Streamlit can load the file
    st.image("assets/dsd_logo.png", width=150, caption="Data Science Dojo")
    
    # Close the div
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

# Apply styling and render hero
HomePageUI.apply_home_styling()
HomePageUI.render_hero_section()

# Show main content only if API keys are configured
if api_keys_configured:
    st.markdown("### Available AI Assistants:")

    # Initialize page discovery
    page_discovery = PageDiscovery()

    if page_discovery.validate_pages_directory():
        page_files = page_discovery.get_available_pages()
        
        if page_files:
            # Navigation buttons
            cols = st.columns(len(page_files))
            
            for i, page_file in enumerate(page_files):
                with cols[i]:
                    icon, title, description = page_discovery.get_page_info(page_file)
                    button_text = f"{icon} {title}"
                    
                    if st.button(button_text, key=os.path.basename(page_file), use_container_width=True):
                        st.switch_page(page_file)
            
            # Feature showcase
            st.markdown("""
            <div class="feature-list">
                <h3 style="color: #00d4aa; margin-bottom: 1.5rem; text-align: center;">✨ Available Features</h3>
            </div>
            """, unsafe_allow_html=True)
            
            for page_file in page_files:
                icon, title, description = page_discovery.get_page_info(page_file)
                HomePageUI.render_feature_card(icon, title, description)
        else:
            st.info("No AI assistant pages found in the pages directory.")
    else:
        st.error("Pages directory not found!")
else:
    # Show getting started info when keys are not configured
    show_getting_started_info()