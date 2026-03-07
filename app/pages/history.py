"""
History Page - View past analyses
"""
import streamlit as st
from datetime import datetime

def show():
    """History page"""
    
    st.markdown("## 🕐 Analysis History")
    st.markdown("View your past document analyses")
    
    # Initialize history in session state
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    
    # Add last analysis to history if exists
    if 'last_analysis' in st.session_state and st.session_state.last_analysis:
        # Check if not already in history
        last = st.session_state.last_analysis
        if not any(h['filename'] == last['filename'] and h['timestamp'] == last['timestamp'] 
                   for h in st.session_state.analysis_history):
            st.session_state.analysis_history.insert(0, last)
    
    if not st.session_state.analysis_history:
        st.info("📭 No analysis history yet. Analyze a document to see it here!")
        return
    
    # Display history
    st.markdown(f"### 📊 Total Analyses: {len(st.session_state.analysis_history)}")
    
    for i, analysis in enumerate(st.session_state.analysis_history):
        with st.expander(f"📄 {analysis['filename']} - {analysis['timestamp'].strftime('%Y-%m-%d %H:%M')}", expanded=(i==0)):
            results = analysis['results']
            final_scores = results.get('final_scores', {})
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Overall Score", f"{final_scores.get('overall_score', 0):.0f}")
            col2.metric("Originality", f"{final_scores.get('originality_score', 0):.0f}")
            col3.metric("Tone", f"{final_scores.get('tone_score', 0):.0f}")
            col4.metric("Citations", f"{final_scores.get('citation_score', 0):.0f}")
            
            if st.button(f"View Full Report", key=f"view_{i}"):
                st.session_state.selected_history = analysis
                st.rerun()
