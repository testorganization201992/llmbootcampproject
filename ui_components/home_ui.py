"""UI Components and Styling Module.

Centralized UI styling and components for the LLM Bootcamp Project.
Provides reusable UI components and consistent styling across all pages.
"""

import streamlit as st


class ChatbotUI:
    """Centralized UI components and styling for chatbot pages."""
    
    @staticmethod
    def apply_enhanced_styling() -> None:
        """Apply theme-responsive styling that adapts to light and dark modes."""
        st.markdown("""
        <style>
            /* Default light theme variables */
            :root {
                --bg-primary: #ffffff;
                --bg-secondary: #f8f9fa;
                --bg-card: linear-gradient(135deg, #ffffff 0%, #f1f5f9 50%, #e2e8f0 100%);
                --bg-card-hover: linear-gradient(135deg, #e2e8f0, #cbd5e1);
                --text-primary: #000000;
                --text-secondary: #6c757d;
                --border-color: rgba(71, 85, 105, 0.9);
                --border-color-hover: rgba(0, 212, 170, 0.8);
                --shadow-light: rgba(71, 85, 105, 0.4);
                --shadow-accent: rgba(0, 212, 170, 0.4);
                --button-bg: linear-gradient(135deg, #ffffff 0%, #f1f5f9 50%, #e2e8f0 100%);
                --button-border: rgba(71, 85, 105, 0.9);
                --card-shadow: 0 8px 25px rgba(71, 85, 105, 0.3), 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            
            /* Dark theme overrides */
            @media (prefers-color-scheme: dark) {
                :root {
                    --bg-primary: #1e1e2e;
                    --bg-secondary: #2a2a3a;
                    --bg-card: linear-gradient(135deg, #374151 0%, #4b5563 50%, #6b7280 100%);
                    --bg-card-hover: linear-gradient(135deg, #4d4d5d, #5d5d6d);
                    --text-primary: #ffffff;
                    --text-secondary: #a0a0a0;
                    --border-color: rgba(156, 163, 175, 0.9);
                    --border-color-hover: rgba(0, 212, 170, 1.0);
                    --shadow-light: rgba(0, 0, 0, 0.8);
                    --button-bg: linear-gradient(135deg, #374151 0%, #4b5563 50%, #6b7280 100%);
                    --button-border: rgba(156, 163, 175, 0.9);
                    --card-shadow: 0 8px 25px rgba(0, 0, 0, 0.7), 0 2px 10px rgba(0, 0, 0, 0.4);
                }
            }
            
            /* Streamlit theme detection - override for Streamlit's dark theme */
            [data-theme="dark"] {
                --bg-primary: #1e1e2e;
                --bg-secondary: #2a2a3a;
                --bg-card: linear-gradient(135deg, #374151 0%, #4b5563 50%, #6b7280 100%);
                --bg-card-hover: linear-gradient(135deg, #4d4d5d, #5d5d6d);
                --text-primary: #ffffff;
                --text-secondary: #a0a0a0;
                --border-color: rgba(156, 163, 175, 0.9);
                --border-color-hover: rgba(0, 212, 170, 1.0);
                --shadow-light: rgba(0, 0, 0, 0.8);
                --button-bg: linear-gradient(135deg, #374151 0%, #4b5563 50%, #6b7280 100%);
                --button-border: rgba(156, 163, 175, 0.9);
                --card-shadow: 0 8px 25px rgba(0, 0, 0, 0.7), 0 2px 10px rgba(0, 0, 0, 0.4);
            }
            
            /* Enhanced chat styling - theme responsive */
            .stChatMessage {
                padding: 1rem;
                margin: 0.5rem 0;
                border-radius: 15px;
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                box-shadow: 0 2px 10px var(--shadow-light);
                color: var(--text-primary);
            }
            
            /* Enhanced buttons - theme responsive with better contrast */
            .stButton > button {
                background: linear-gradient(135deg, #00d4aa, #00a883) !important;
                border: 2px solid var(--button-border) !important;
                border-radius: 12px !important;
                color: white !important;
                font-weight: 600;
                padding: 0.75rem 2rem;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px var(--shadow-accent);
                position: relative;
                overflow: hidden;
            }
            
            .stButton > button::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0, 212, 170, 0.5) !important;
                background: linear-gradient(135deg, #00e6c0, #00cc99) !important;
                border-color: #00d4aa !important;
            }
            
            .stButton > button:hover::before {
                left: 100%;
            }
            
            /* Enhanced text inputs - theme responsive */
            .stTextInput > div > div > input {
                background: var(--bg-secondary) !important;
                border: 2px solid var(--border-color) !important;
                border-radius: 10px;
                color: var(--text-primary) !important;
                font-size: 16px;
                padding: 12px;
                transition: all 0.3s ease;
            }
            
            .stTextInput > div > div > input:focus {
                border-color: #00d4aa !important;
                box-shadow: 0 0 20px rgba(0, 212, 170, 0.3);
            }
            
            /* Password inputs */
            .stTextInput > div > div > input[type="password"] {
                background: var(--bg-secondary) !important;
                border: 2px solid var(--border-color) !important;
                color: var(--text-primary) !important;
            }
            
            /* Enhanced titles */
            h1 {
                background: linear-gradient(135deg, #00d4aa, var(--text-primary));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: 800;
                text-shadow: 0 0 30px rgba(0, 212, 170, 0.5);
            }
            
            /* Chat input enhancement - theme responsive */
            .stChatInput {
                background: var(--bg-secondary);
                border-radius: 15px;
                border: 2px solid var(--border-color);
            }
            
            /* Info/Success/Error/Warning boxes - theme responsive */
            .stInfo {
                background: var(--bg-card) !important;
                border-left: 4px solid #00d4aa;
                border-radius: 10px;
                box-shadow: 0 2px 10px var(--shadow-light);
            }
            
            .stSuccess {
                background: var(--bg-card) !important;
                border-left: 4px solid #00d4aa;
                border-radius: 10px;
                box-shadow: 0 2px 10px var(--shadow-light);
            }
            
            .stError {
                background: var(--bg-card) !important;
                border-left: 4px solid #ff6b6b;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(255, 107, 107, 0.2);
            }
            
            .stWarning {
                background: var(--bg-card) !important;
                border-left: 4px solid #ffaa00;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(255, 170, 0, 0.2);
            }
            
            /* Enhanced file uploader - theme responsive */
            .stFileUploader > div {
                background: var(--bg-secondary);
                border: 2px dashed var(--border-color);
                border-radius: 15px;
                padding: 2rem;
                text-align: center;
                transition: all 0.3s ease;
            }
            
            .stFileUploader > div:hover {
                border-color: #00d4aa;
                box-shadow: 0 0 20px rgba(0, 212, 170, 0.2);
            }
            
            /* Sidebar styling - theme responsive */
            .stSidebar {
                background: var(--bg-secondary);
            }
            
            /* Streamlit components theme fixes */
            div[data-testid="stSidebar"] {
                background: var(--bg-secondary);
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
    def add_sidebar_logo():
        """Add centered logo to sidebar - reusable across all pages"""
        with st.sidebar:
            # Create columns for better centering
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.image("assets/dsd_logo.png", width=120)
            
            # Center the caption text
            st.markdown(
                "<div style='text-align: center; margin-top: -10px; font-size: 14px; color: var(--text-color); font-weight: 500;'>Data Science Dojo</div>", 
                unsafe_allow_html=True
            )
            
            st.markdown("---")
    
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
        """Apply theme-responsive styling specific to the home page with compelling visual design."""
        st.markdown("""
        <style>
            /* Enhanced navigation buttons - ALWAYS visible and standout */
            .stButton > button {
                height: 4.5rem;
                width: 100%;
                border-radius: 16px;
                /* STRONGER borders and gradients for better visibility */
                border: 3px solid #00d4aa !important;
                background: linear-gradient(135deg, #00d4aa 0%, #00a883 50%, #008f70 100%) !important;
                color: white !important;
                font-size: 1.1rem;
                font-weight: 700;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                margin-bottom: 1rem;
                /* ALWAYS visible shadow */
                box-shadow: 0 8px 25px rgba(0, 212, 170, 0.4), 
                           0 4px 15px rgba(0, 0, 0, 0.2),
                           inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
                position: relative;
                overflow: hidden;
                backdrop-filter: blur(10px);
                /* Subtle glow effect always present */
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
            }
            
            .stButton > button::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
                transition: left 0.6s ease;
            }
            
            .stButton > button:hover {
                transform: translateY(-4px) scale(1.02);
                border-color: #00f0cc !important;
                box-shadow: 0 15px 40px rgba(0, 212, 170, 0.6), 
                           0 8px 25px rgba(0, 0, 0, 0.3) !important;
                background: linear-gradient(135deg, #00f0cc 0%, #00d4aa 50%, #00cc99 100%) !important;
            }
            
            .stButton > button:hover::before {
                left: 100%;
            }
            
            .stButton > button:active {
                transform: translateY(-2px) scale(1.01);
            }
            
            /* Modern feature cards - subtle and professional */
            div[style*="rgba(0, 212, 170, 0.05)"] {
                transition: all 0.3s ease !important;
            }
            
            div[style*="rgba(0, 212, 170, 0.05)"]:hover {
                background: linear-gradient(135deg, rgba(0, 212, 170, 0.1) 0%, rgba(0, 212, 170, 0.05) 100%) !important;
                border: 1px solid rgba(0, 212, 170, 0.4) !important;
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0, 212, 170, 0.15);
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_hero_section() -> None:
        """Render the hero section for the home page."""
        st.markdown("""
        <div style='text-align: center; margin: 2rem 0;'>
            <h1 style='font-size: 3rem; margin-bottom: 1rem; background: linear-gradient(135deg, #00d4aa, #ffffff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                🤖 LLM Bootcamp Project 
            </h1>
            <p style='font-size: 1.2rem; color: #a0a0a0; margin-bottom: 2rem;'>
                Explore conversational AI with intelligent agents, document processing, and web search integration
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_feature_card(icon: str, title: str, description: str) -> None:
        """Render a theme-responsive feature card with icon, title, and description."""
        st.markdown(f"""
        <div class="feature-card">
            <h3 style="margin-bottom: 0.5rem;">
                {icon} {title}
            </h3>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)