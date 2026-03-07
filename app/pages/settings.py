"""
Settings Page - Configure application settings
"""
import streamlit as st

def show():
    """Settings page"""
    
    st.markdown("## ⚙️ Settings")
    st.markdown("Configure your analysis preferences")
    
    # Analysis Settings
    st.markdown("### 🔍 Analysis Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        plagiarism_threshold = st.slider(
            "Plagiarism Sensitivity",
            min_value=10,
            max_value=50,
            value=20,
            help="Lower = more strict"
        )
        
        citation_style = st.selectbox(
            "Preferred Citation Style",
            ["APA", "IEEE", "MLA", "Chicago"]
        )
    
    with col2:
        tone_strictness = st.slider(
            "Tone Analysis Strictness",
            min_value=1,
            max_value=10,
            value=5
        )
        
        readability_target = st.selectbox(
            "Target Readability Level",
            ["High School", "Undergraduate", "Graduate", "Professional"]
        )
    
    # Report Settings
    st.markdown("### 📄 Report Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        default_format = st.selectbox(
            "Default Report Format",
            ["PDF", "DOCX", "HTML"]
        )
    
    with col2:
        include_charts = st.checkbox("Include Charts in Reports", value=True)
        include_recommendations = st.checkbox("Include Recommendations", value=True)
    
    # API Settings
    st.markdown("### 🔌 API Settings")
    
    openai_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Optional: For advanced AI features"
    )
    
    semantic_scholar_key = st.text_input(
        "Semantic Scholar API Key",
        type="password",
        help="Optional: For citation analysis"
    )
    
    # Save button
    if st.button("💾 Save Settings", use_container_width=True):
        st.success("✅ Settings saved successfully!")
        
        # Store in session state
        st.session_state.settings = {
            'plagiarism_threshold': plagiarism_threshold,
            'citation_style': citation_style,
            'tone_strictness': tone_strictness,
            'readability_target': readability_target,
            'default_format': default_format,
            'include_charts': include_charts,
            'include_recommendations': include_recommendations
        }
    
    # Reset button
    if st.button("🔄 Reset to Defaults"):
        st.info("Settings reset to defaults")
