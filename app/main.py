"""
Professional Multi-Page Research Intelligence Application
Advanced features comparable to Grammarly and Turnitin
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from streamlit_option_menu import option_menu as streamlit_option_menu

# Set page config FIRST
st.set_page_config(
    page_title="AI Research Intelligence Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar by default
)

# Import page modules
import app.dashboard as dashboard
from app.pages import history, reports, settings, sentence_analysis

def apply_professional_styling():
    """Apply professional CSS styling with centered layout"""
    st.markdown("""
    <style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Lato:wght@300;400;700&display=swap');
    
    /* Hide sidebar completely */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Main background - centered */
    .main {
        background: linear-gradient(135deg, #f5f3ef 0%, #e8e4dd 100%);
        max-width: 100%;
        margin: 0 auto;
    }
    
    .main .block-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 3rem 2rem;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main application with professional navigation"""
    
    # Initialize session state variables
    if 'analysis_count' not in st.session_state:
        st.session_state.analysis_count = 0
    
    apply_professional_styling()
    
    # Professional Header
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem; color: white;">
            🎓 AI Research Intelligence Pro
        </h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9; color: white;">
            Advanced Plagiarism Detection & Quality Analysis Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("### 📊 Navigation")
        
        selected = streamlit_option_menu(
            menu_title=None,
            options=["Dashboard", "Sentence Analysis", "History", "Reports", "Settings"],
            icons=["house", "search", "clock-history", "file-earmark-text", "gear"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#0369a1", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "5px",
                    "padding": "10px",
                    "--hover-color": "#e0f2fe",
                    "border-radius": "8px"
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, #0369a1 0%, #0284c7 100%)",
                    "color": "white",
                    "font-weight": "600"
                },
            }
        )
        
        # Sidebar info
        st.markdown("---")
        st.markdown("### 📈 Quick Stats")
        if 'analysis_count' not in st.session_state:
            st.session_state.analysis_count = 0
        st.metric("Documents Analyzed", st.session_state.analysis_count)
        
        st.markdown("---")
        st.markdown("### 🎯 Features")
        st.markdown("""
        - ✅ Multi-engine plagiarism detection
        - ✅ Sentence-level analysis
        - ✅ Real-time suggestions
        - ✅ Detailed PDF reports
        - ✅ Citation management
        - ✅ Tone analysis
        - ✅ Readability scoring
        """)
    
    # Route to selected page
    if selected == "Dashboard":
        dashboard.run_dashboard()
    elif selected == "Sentence Analysis":
        sentence_analysis.show()
    elif selected == "History":
        history.show()
    elif selected == "Reports":
        reports.show()
    elif selected == "Settings":
        settings.show()

if __name__ == "__main__":
    main()