import os
import streamlit as st
from config.app_config import setup_page_config
from config.api_config import setup_api_keys_ui, show_getting_started_info
from utils.page_utils import PageDiscovery
from ui_components.home_ui import HomePageUI, ChatbotUI

# Configure the app
setup_page_config()

# Setup API keys UI - this will show the key input form or local dev status
api_keys_configured = setup_api_keys_ui()

# Add logo to the sidebar
ChatbotUI.add_sidebar_logo()

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
            
            # Professional feature overview
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; margin: 3rem 0 2rem 0;">
                <h3 style="color: #00d4aa; font-size: 1.8rem; font-weight: 600; margin-bottom: 0.5rem;">
                    ✨ Powered by Advanced AI
                </h3>
                <p style="color: #6b7280; font-size: 1rem; margin: 0;">
                    Choose from specialized AI assistants tailored for different tasks
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Feature grid with modern cards
            feature_cols = st.columns(2)
            features_data = []
            
            for page_file in page_files:
                icon, title, description = page_discovery.get_page_info(page_file)
                features_data.append((icon, title, description))
            
            for i, (icon, title, description) in enumerate(features_data):
                with feature_cols[i % 2]:
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(0, 212, 170, 0.05) 0%, rgba(0, 212, 170, 0.02) 100%);
                        border: 1px solid rgba(0, 212, 170, 0.2);
                        border-radius: 12px;
                        padding: 1.5rem;
                        margin-bottom: 1rem;
                        transition: all 0.3s ease;
                        backdrop-filter: blur(10px);
                    ">
                        <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                            <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
                            <h4 style="color: #00d4aa; margin: 0; font-size: 1.1rem; font-weight: 600;">{title}</h4>
                        </div>
                        <p style="color: #64748b; margin: 0; font-size: 0.9rem; line-height: 1.5;">
                            {description}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No AI assistant pages found in the pages directory.")
    else:
        st.error("Pages directory not found!")
else:
    # Show getting started info when keys are not configured
    show_getting_started_info()