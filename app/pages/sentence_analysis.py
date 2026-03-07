"""
Sentence-Level Analysis Page - Like Grammarly
Shows detailed analysis for each sentence
"""
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import re
from utils.file_handler import extract_text

def analyze_sentence(sentence):
    """Analyze individual sentence"""
    issues = []
    
    # Check passive voice
    passive_indicators = ['was', 'were', 'been', 'being', 'is', 'are', 'am']
    if any(word in sentence.lower().split() for word in passive_indicators):
        issues.append(("⚠️ Passive Voice", "Consider using active voice for clarity"))
    
    # Check sentence length
    word_count = len(sentence.split())
    if word_count > 30:
        issues.append(("⚠️ Long Sentence", f"{word_count} words - consider breaking into shorter sentences"))
    
    # Check informal words
    informal_words = ['a lot of', 'get', 'got', 'thing', 'stuff', 'big', 'small']
    for word in informal_words:
        if word in sentence.lower():
            issues.append(("📝 Informal Language", f"Replace '{word}' with academic alternative"))
    
    # Check first person
    first_person = ['I ', 'my ', 'me ', 'we ', 'our ', 'us ']
    if any(fp in sentence for fp in first_person):
        issues.append(("👤 First Person", "Consider using third person for academic tone"))
    
    return issues

def show():
    """Sentence analysis page"""
    
    st.markdown("## 🔍 Sentence-Level Analysis")
    st.markdown("Get detailed feedback on every sentence in your document")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload document for sentence analysis",
        type=["pdf", "docx", "txt"],
        key="sentence_upload"
    )
    
    if not uploaded_file:
        st.info("👆 Upload a document to see sentence-by-sentence analysis")
        
        # Show example
        st.markdown("### 📖 Example Analysis")
        example_text = """
        The experiment was conducted by the research team. We found that the results were significant. 
        There was a lot of data collected during the study. The thing is, passive voice makes writing less clear.
        """
        
        st.markdown("**Sample Text:**")
        st.text_area("", example_text, height=100, disabled=True)
        
        st.markdown("**Analysis Results:**")
        sentences = [s.strip() + '.' for s in example_text.split('.') if s.strip()]
        
        for i, sentence in enumerate(sentences, 1):
            issues = analyze_sentence(sentence)
            if issues:
                with st.expander(f"Sentence {i}: {len(issues)} issue(s) found", expanded=True):
                    st.markdown(f"**Text:** {sentence}")
                    for issue_type, suggestion in issues:
                        st.warning(f"{issue_type}: {suggestion}")
        return
    
    # Extract and analyze
    with st.spinner("Analyzing sentences..."):
        try:
            text = extract_text(uploaded_file)
            sentences = [s.strip() + '.' for s in re.split(r'[.!?]', text) if s.strip()]
            
            st.success(f"✓ Found {len(sentences)} sentences")
            
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            
            total_issues = sum(len(analyze_sentence(s)) for s in sentences)
            sentences_with_issues = sum(1 for s in sentences if analyze_sentence(s))
            
            col1.metric("Total Sentences", len(sentences))
            col2.metric("Sentences with Issues", sentences_with_issues)
            col3.metric("Total Issues", total_issues)
            col4.metric("Clean Sentences", len(sentences) - sentences_with_issues)
            
            # Filter options
            st.markdown("---")
            filter_option = st.selectbox(
                "Filter sentences:",
                ["All Sentences", "Only Sentences with Issues", "Clean Sentences"]
            )
            
            # Display sentences
            st.markdown("### 📝 Sentence Analysis")
            
            for i, sentence in enumerate(sentences, 1):
                issues = analyze_sentence(sentence)
                
                # Apply filter
                if filter_option == "Only Sentences with Issues" and not issues:
                    continue
                if filter_option == "Clean Sentences" and issues:
                    continue
                
                # Display sentence
                if issues:
                    with st.expander(f"Sentence {i}: {len(issues)} issue(s) ⚠️", expanded=False):
                        st.markdown(f"**Original:** {sentence}")
                        st.markdown("**Issues Found:**")
                        for issue_type, suggestion in issues:
                            st.warning(f"{issue_type}: {suggestion}")
                else:
                    with st.expander(f"Sentence {i}: ✅ No issues", expanded=False):
                        st.markdown(f"**Text:** {sentence}")
                        st.success("This sentence looks good!")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
