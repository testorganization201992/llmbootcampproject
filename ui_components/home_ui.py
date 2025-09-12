"""UI Components and Styling Module.

Centralized UI styling and components for the LLM Bootcamp Project.
Provides reusable UI components and consistent styling across all pages.
"""

import streamlit as st


class ChatbotUI:
    """Centralized UI components and styling for chatbot pages."""
    
    @staticmethod
    def apply_enhanced_styling() -> None:
        """Apply enhanced dark theme styling to the page."""
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
            
            /* Chat input enhancement */
            .stChatInput {
                background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
                border-radius: 15px;
                border: 2px solid rgba(0, 212, 170, 0.2);
            }
            
            /* Info boxes */
            .stInfo {
                background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
                border-left: 4px solid #00d4aa;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 212, 170, 0.2);
            }
            
            /* Success boxes */
            .stSuccess {
                background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
                border-left: 4px solid #00d4aa;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 212, 170, 0.2);
            }
            
            /* Error boxes */
            .stError {
                background: linear-gradient(135deg, #2e1e1e, #3a2a2a);
                border-left: 4px solid #ff6b6b;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(255, 107, 107, 0.2);
            }
            
            /* Warning boxes */
            .stWarning {
                background: linear-gradient(135deg, #2e2e1e, #3a3a2a);
                border-left: 4px solid #ffaa00;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(255, 170, 0, 0.2);
            }
            
            /* Enhanced file uploader */
            .stFileUploader > div {
                background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
                border: 2px dashed rgba(0, 212, 170, 0.3);
                border-radius: 15px;
                padding: 2rem;
                text-align: center;
                transition: all 0.3s ease;
            }
            
            .stFileUploader > div:hover {
                border-color: #00d4aa;
                box-shadow: 0 0 20px rgba(0, 212, 170, 0.2);
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def setup_page(title: str, icon: str, layout: str = "wide", sidebar_state: str = "collapsed") -> None:
        """Setup page configuration with enhanced styling."""
        st.set_page_config(
            page_title=title,
            page_icon=icon,
            layout=layout,
            initial_sidebar_state=sidebar_state
        )
        ChatbotUI.apply_enhanced_styling()
    
    @staticmethod
    def render_page_header(icon: str, title: str, subtitle: str) -> None:
        """Render enhanced page header with title and subtitle."""
        st.markdown(f"""
        <div style='text-align: center; margin: 0.5rem 0 1rem 0;'>
            <h1 style='font-size: 2.625rem; margin-bottom: 1rem; text-shadow: 0 0 30px rgba(0, 212, 170, 0.5);'>
                {icon} {title}
            </h1>
            <p style='font-size: 0.9rem; color: #a0a0a0; margin-top: -0.5rem;'>
                {subtitle}
            </p>
        </div>
        """, unsafe_allow_html=True)


class HomePageUI:
    """UI components specific to the home page."""
    
    @staticmethod
    def apply_home_styling() -> None:
        """Apply enhanced styling specific to the home page."""
        st.markdown("""
        <style>
            /* Enhanced navigation buttons */
            .stButton > button {
                height: 4rem;
                width: 100%;
                border-radius: 15px;
                border: 2px solid rgba(0, 212, 170, 0.3);
                background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
                color: white;
                font-size: 1.1rem;
                font-weight: 600;
                transition: all 0.3s ease;
                margin-bottom: 1rem;
            }
            
            .stButton > button:hover {
                transform: translateY(-3px);
                border-color: #00d4aa;
                box-shadow: 0 8px 25px rgba(0, 212, 170, 0.4);
                background: linear-gradient(135deg, #00d4aa, #00a883);
            }
            
            /* Feature cards styling */
            .feature-card {
                background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
                border: 1px solid rgba(0, 212, 170, 0.2);
                border-radius: 15px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
            }
            
            .feature-card:hover {
                transform: translateY(-2px);
                border-color: #00d4aa;
                box-shadow: 0 6px 20px rgba(0, 212, 170, 0.3);
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_hero_section() -> None:
        """Render the hero section for the home page."""
        st.markdown("""
        <div style='text-align: center; margin: 2rem 0;'>
            <h1 style='font-size: 3rem; margin-bottom: 1rem; background: linear-gradient(135deg, #00d4aa, #ffffff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                🤖 AI Chatbot Platform
            </h1>
            <p style='font-size: 1.2rem; color: #a0a0a0; margin-bottom: 2rem;'>
                Enterprise-grade conversational AI with intelligent agents, document processing, and web search integration
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_feature_card(icon: str, title: str, description: str) -> None:
        """Render a feature card with icon, title, and description."""
        st.markdown(f"""
        <div class="feature-card">
            <h3 style="color: #00d4aa; margin-bottom: 0.5rem;">
                {icon} {title}
            </h3>
            <p style="color: #cccccc; font-size: 0.9rem; margin: 0;">
                {description}
            </p>
        </div>
        """, unsafe_allow_html=True)
