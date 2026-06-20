import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from guidance_engine.improvement_path import ImprovementPathGenerator
from utils.file_handler import extract_text
from quality_analyzer.scoring_engine import ResearchIntelligenceSystem

# Initialize systems
improvement_generator = ImprovementPathGenerator()
local_system = ResearchIntelligenceSystem()


def apply_custom_css():
    """Apply enhanced professional aesthetic CSS"""
    st.markdown("""
    <style>
    /* Import elegant fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Force light theme and center everything */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #dbeafe 100%) !important;
    }
    
    /* Hide sidebar */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Main container - centered */
    .main {
        max-width: 1400px !important;
        margin: 0 auto !important;
        padding: 2rem !important;
        background: transparent !important;
    }
    
    .block-container {
        max-width: 1400px !important;
        margin: 0 auto !important;
        padding: 2rem 1rem !important;
    }
    
    /* Main background - Enhanced gradient */
    .stApp {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #dbeafe 100%) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* All text - Darker blue for visibility */
    * {
        color: #0c4a6e !important;
    }
    
    /* Headers - Enhanced hierarchy */
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 900 !important;
        font-size: 3.5rem !important;
        color: #075985 !important;
        letter-spacing: -0.03em !important;
        line-height: 1.1 !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 2px 4px rgba(7, 89, 133, 0.1);
    }
    
    h2 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        font-size: 2.25rem !important;
        color: #0c4a6e !important;
        letter-spacing: -0.02em !important;
        margin-top: 2.5rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    h3 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.75rem !important;
        color: #0c4a6e !important;
        letter-spacing: -0.01em !important;
        margin-top: 2rem !important;
    }
    
    /* Paragraph text - Enhanced readability */
    p {
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
        font-size: 1.05rem !important;
        color: #0c4a6e !important;
        line-height: 1.8 !important;
    }
    
    /* Card styling - Enhanced with shadows */
    .css-1r6slb0, .element-container {
        background: white;
        border-radius: 20px;
        padding: 28px;
        box-shadow: 
            0 4px 6px rgba(3, 105, 161, 0.07),
            0 2px 4px rgba(3, 105, 161, 0.06),
            0 0 0 1px rgba(186, 230, 253, 0.5);
        border: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .css-1r6slb0:hover, .element-container:hover {
        box-shadow: 
            0 10px 15px rgba(3, 105, 161, 0.1),
            0 4px 6px rgba(3, 105, 161, 0.08),
            0 0 0 1px rgba(186, 230, 253, 0.8);
        transform: translateY(-2px);
    }
    
    /* Buttons - Enhanced gradient and effects */
    .stButton>button {
        background: linear-gradient(135deg, #0369a1 0%, #0284c7 50%, #0ea5e9 100%);
        color: white !important;
        border: none;
        border-radius: 14px;
        padding: 18px 36px;
        font-size: 17px;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.02em;
        box-shadow: 
            0 4px 12px rgba(3, 105, 161, 0.25),
            0 2px 4px rgba(3, 105, 161, 0.15);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 50%, #075985 100%);
        transform: translateY(-3px);
        box-shadow: 
            0 8px 20px rgba(3, 105, 161, 0.35),
            0 4px 8px rgba(3, 105, 161, 0.2);
    }
    
    .stButton>button:active {
        transform: translateY(-1px);
    }
    
    /* File uploader - Enhanced design */
    .stFileUploader {
        background: white;
        border-radius: 20px;
        padding: 40px;
        border: 3px dashed #7dd3fc;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(3, 105, 161, 0.08);
    }
    
    .stFileUploader:hover {
        border-color: #38bdf8;
        background: #f0f9ff;
        box-shadow: 0 4px 12px rgba(3, 105, 161, 0.12);
        transform: scale(1.01);
    }
    
    /* Metrics - Enhanced cards */
    .stMetric {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(3, 105, 161, 0.1);
        border: 1px solid #bae6fd;
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        box-shadow: 0 6px 16px rgba(3, 105, 161, 0.15);
        transform: translateY(-4px);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #075985 !important;
        text-shadow: 0 2px 4px rgba(7, 89, 133, 0.1);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        color: #0c4a6e !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    
    /* Hide metric delta arrows */
    [data-testid="stMetricDelta"] {
        display: none !important;
    }
    
    /* Success/Warning/Error boxes - Enhanced */
    .stSuccess {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%) !important;
        border-left: 5px solid #22c55e !important;
        border-radius: 14px;
        padding: 20px;
        color: #166534 !important;
        box-shadow: 0 2px 8px rgba(34, 197, 94, 0.15);
        font-weight: 500;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%) !important;
        border-left: 5px solid #f59e0b !important;
        border-radius: 14px;
        padding: 20px;
        color: #92400e !important;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.15);
        font-weight: 500;
    }
    
    .stError {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%) !important;
        border-left: 5px solid #ef4444 !important;
        border-radius: 14px;
        padding: 20px;
        color: #991b1b !important;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.15);
        font-weight: 500;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%) !important;
        border-left: 5px solid #3b82f6 !important;
        border-radius: 14px;
        padding: 20px;
        color: #1e40af !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
        font-weight: 500;
    }
    
    /* Progress bar - Enhanced gradient */
    .stProgress > div > div {
        background: linear-gradient(90deg, #0369a1 0%, #0284c7 50%, #0ea5e9 100%);
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(3, 105, 161, 0.3);
    }
    
    /* Expander - Enhanced */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        color: #0369a1 !important;
        border-radius: 14px;
        font-weight: 700;
        border: 2px solid #bae6fd;
        padding: 16px 20px;
        transition: all 0.3s ease;
        font-size: 1.1rem;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        border-color: #7dd3fc;
        box-shadow: 0 4px 12px rgba(3, 105, 161, 0.15);
    }
    
    /* Code blocks - Enhanced */
    code {
        font-family: 'JetBrains Mono', monospace !important;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%) !important;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.9rem;
        color: #0369a1 !important;
        border: 1px solid #bae6fd;
        font-weight: 500;
    }
    
    /* Columns - Better spacing */
    .stColumns {
        gap: 1.5rem;
    }
    
    /* Enhanced animations */
    @keyframes fadeInUp {
        from { 
            opacity: 0; 
            transform: translateY(30px);
        }
        to { 
            opacity: 1; 
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.8;
        }
    }
    
    .element-container {
        animation: fadeInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Enhanced scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #e0f2fe;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #7dd3fc 0%, #38bdf8 100%);
        border-radius: 10px;
        border: 2px solid #e0f2fe;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #0ea5e9 100%);
    }
    
    /* Plotly charts - Enhanced */
    .stPlotlyChart {
        background: white;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(3, 105, 161, 0.08);
        border: 1px solid #bae6fd;
    }
    
    /* Download button - Enhanced */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white !important;
        border: none;
        border-radius: 14px;
        padding: 16px 32px;
        font-size: 16px;
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
        transition: all 0.3s ease;
    }
    
    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.35);
    }
    </style>
    """, unsafe_allow_html=True)


def create_score_gauge(score, title):
    """Create elegant blue gauge chart with visible numbers"""
    fig = go.Figure(go.Indicator(
        mode="gauge",  # Only gauge, no number mode
        value=score,
        domain={'x': [0.05, 0.95], 'y': [0.25, 0.75]},  # Centered gauge
        title={
            'text': f"<b style='font-size:18px'>{title}</b><br><br><span style='font-size:56px; font-weight:800; color:#075985'>{score:.1f}</span>", 
            'font': {'size': 14, 'color': '#0c4a6e', 'family': 'Inter'},
            'align': 'center'
        },
        gauge={
            'axis': {
                'range': [None, 100], 
                'tickwidth': 1, 
                'tickcolor': "#93c5fd", 
                'tickfont': {'size': 10, 'color': '#0c4a6e'}
            },
            'bar': {'color': "#075985", 'thickness': 0.3},
            'bgcolor': "#f0f9ff",
            'borderwidth': 2,
            'bordercolor': "#93c5fd",
            'steps': [
                {'range': [0, 40], 'color': '#dbeafe'},
                {'range': [40, 70], 'color': '#bfdbfe'},
                {'range': [70, 100], 'color': '#93c5fd'}
            ],
            'threshold': {
                'line': {'color': "#0284c7", 'width': 2},
                'thickness': 0.35,
                'value': 85
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={'color': "#0c4a6e", 'family': "Inter"},
        height=300,
        margin=dict(l=10, r=10, t=100, b=10)
    )
    
    return fig


def create_comparison_chart(scores_dict):
    """Create elegant blue bar chart"""
    categories = list(scores_dict.keys())
    values = list(scores_dict.values())
    
    # Create blue gradient based on values
    colors = ['rgba(7, 89, 133, ' + str(0.6 + (v/250)) + ')' for v in values]
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker=dict(
                color=colors,
                line=dict(color='#075985', width=2)
            ),
            text=[f'{v:.0f}' for v in values],
            textposition='outside',
            textfont=dict(size=18, color='#0c4a6e', family='Inter', weight=700),
            hovertemplate='<b>%{x}</b><br>Score: %{y:.1f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': "Performance Metrics",
            'font': {'size': 22, 'color': '#075985', 'family': 'Inter', 'weight': 700}
        },
        xaxis_title="",
        yaxis_title="Score",
        yaxis=dict(
            range=[0, 105],
            gridcolor='#dbeafe',
            tickfont=dict(color='#0c4a6e', family='Inter', size=12)
        ),
        xaxis=dict(
            tickfont=dict(color='#0c4a6e', family='Inter', weight=600, size=13)
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter", size=14, color="#0c4a6e"),
        height=400,
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig


def create_risk_indicator(risk_level, score):
    """Create elegant blue risk indicator"""
    risk_configs = {
        "MINIMAL": {"color": "#075985", "bg": "#f0f9ff", "icon": "✓", "border": "#7dd3fc"},
        "LOW": {"color": "#0c4a6e", "bg": "#e0f2fe", "icon": "○", "border": "#38bdf8"},
        "MEDIUM": {"color": "#075985", "bg": "#bae6fd", "icon": "△", "border": "#0284c7"},
        "HIGH": {"color": "#0c4a6e", "bg": "#93c5fd", "icon": "⬤", "border": "#0369a1"}
    }
    
    config = risk_configs.get(risk_level, risk_configs["LOW"])
    
    return f"""
    <div style="
        background: {config['bg']};
        border: 2px solid {config['border']};
        border-radius: 16px;
        padding: 32px;
        margin: 24px 0;
        box-shadow: 0 2px 4px rgba(7, 89, 133, 0.15);
    ">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <p style="
                    font-size: 14px;
                    font-weight: 700;
                    color: #0c4a6e;
                    margin: 0;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                ">Plagiarism Risk Level</p>
                <h2 style="
                    font-size: 36px;
                    font-weight: 800;
                    color: {config['color']};
                    margin: 8px 0;
                    letter-spacing: -0.02em;
                ">{config['icon']} {risk_level}</h2>
                <p style="
                    font-size: 18px;
                    font-weight: 600;
                    color: #0c4a6e;
                    margin: 0;
                ">{score:.1%} Similarity Detected</p>
            </div>
            <div style="
                font-size: 72px;
                color: {config['color']};
                opacity: 0.2;
            ">{config['icon']}</div>
        </div>
    </div>
    """


def run_dashboard():
    """Main dashboard with professional aesthetic design"""
    
    # Apply custom styling
    apply_custom_css()
    
    # Technology info - simple inline format
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: white; border-radius: 16px; margin-bottom: 32px; box-shadow: 0 2px 4px rgba(7, 89, 133, 0.12); border: 1px solid #93c5fd;">
        <p style="font-size: 16px; color: #0c4a6e; margin: 0;">
            � Rabin-Karp  •  📊 TF-IDF  •  🧠 Transformers  •  🎯 Sentence-BERT  •  💬 NLP  •  ⚡ Real-time
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # File Upload Section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        uploaded_file = st.file_uploader(
            "Upload your research document",
            type=["pdf", "docx", "txt"],
            help="Supported formats: PDF, DOCX, TXT (max 50MB)"
        )
    
    if not uploaded_file:
        # Show features
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        features = [
            ("🔍", "Multi-Engine Detection", "Rabin-Karp, TF-IDF, and Transformer-based analysis"),
            ("📊", "Quality Metrics", "Comprehensive tone, citation, and structure evaluation"),
            ("💡", "Smart Recommendations", "AI-powered suggestions for improvement")
        ]
        
        for col, (icon, title, desc) in zip([col1, col2, col3], features):
            with col:
                st.markdown(f"""
                <div style="
                    background: white;
                    padding: 32px 24px;
                    border-radius: 16px;
                    text-align: center;
                    height: 220px;
                    border: 1px solid #93c5fd;
                    box-shadow: 0 2px 4px rgba(7, 89, 133, 0.12);
                ">
                    <div style="font-size: 48px; margin-bottom: 16px; opacity: 0.8;">{icon}</div>
                    <h3 style="font-size: 18px; font-weight: 700; color: #075985; margin-bottom: 8px;">{title}</h3>
                    <p style="font-size: 14px; color: #0c4a6e; line-height: 1.6; font-weight: 500;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
        
        return
    
    # File uploaded
    st.success(f"✓ {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
    
    # Extract text
    with st.spinner("Extracting text..."):
        try:
            document_text = extract_text(uploaded_file)
            word_count = len(document_text.split())
            st.info(f"📄 {word_count:,} words extracted")
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return
    
    # Analysis button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_button = st.button("Analyze Document", use_container_width=True)
    
    if analyze_button:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Running analysis...")
        progress_bar.progress(33)
        
        results = local_system.analyze_text(document_text)
        progress_bar.progress(66)
        
        plagiarism_data = results.get("plagiarism_analysis", {})
        quality_data = results.get("quality_analysis", {})
        final_scores = results.get("final_scores", {})
        
        improvement_plan = improvement_generator.generate_plan(
            plagiarism_data=plagiarism_data,
            tone_data=quality_data.get("tone", {}),
            citation_data=quality_data.get("citations", {}),
            structure_data=quality_data.get("structure", {}),
            readability_data=quality_data.get("readability", {}),
            final_score=final_scores.get("overall_score", 0)
        )
        
        progress_bar.progress(100)
        status_text.text("✓ Analysis complete")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Overall Score
        overall_score = final_scores.get("overall_score", 0)
        st.markdown(f"""
        <div style="
            background: white;
            padding: 48px;
            border-radius: 20px;
            text-align: center;
            border: 2px solid #60a5fa;
            box-shadow: 0 4px 6px rgba(7, 89, 133, 0.15);
            margin: 32px 0;
        ">
            <p style="
                font-size: 14px;
                font-weight: 700;
                color: #0c4a6e;
                margin: 0;
                text-transform: uppercase;
                letter-spacing: 0.1em;
            ">Overall Quality Score</p>
            <h1 style="
                font-size: 96px;
                font-weight: 800;
                color: #075985;
                margin: 16px 0;
                letter-spacing: -0.03em;
            ">{overall_score:.0f}</h1>
            <p style="font-size: 16px; color: #0c4a6e; margin: 0; font-weight: 600;">out of 100</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Risk Indicator
        plag_score = plagiarism_data.get("overall_plagiarism_score", 0)
        risk_level = plagiarism_data.get("risk_level", "UNKNOWN")
        st.markdown(create_risk_indicator(risk_level, plag_score), unsafe_allow_html=True)
        
        # Metrics
        st.markdown("### Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        metrics = [
            ("Originality", final_scores.get('originality_score', 0)),
            ("Tone Quality", final_scores.get('tone_score', 0)),
            ("Citations", final_scores.get('citation_score', 0)),
            ("Overall", overall_score)
        ]
        
        for col, (label, value) in zip([col1, col2, col3, col4], metrics):
            with col:
                st.metric(label, f"{value:.0f}")
        
        # Gauge Charts
        st.markdown("### Detailed Analysis")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig1 = create_score_gauge(final_scores.get('originality_score', 0), "Originality")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = create_score_gauge(final_scores.get('tone_score', 0), "Tone")
            st.plotly_chart(fig2, use_container_width=True)
        
        with col3:
            fig3 = create_score_gauge(final_scores.get('citation_score', 0), "Citations")
            st.plotly_chart(fig3, use_container_width=True)
        
        # Comparison Chart
        scores_for_chart = {
            "Originality": final_scores.get('originality_score', 0),
            "Tone": final_scores.get('tone_score', 0),
            "Citations": final_scores.get('citation_score', 0),
            "Overall": overall_score
        }
        fig_comparison = create_comparison_chart(scores_for_chart)
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Smart Recommendations - User-friendly format
        st.markdown("### 💡 Smart Recommendations")
        st.markdown("<p style='font-size: 16px; color: #0c4a6e; margin-bottom: 24px;'>AI-powered, actionable guidance to improve your document</p>", unsafe_allow_html=True)
        
        # Create user-friendly recommendations based on scores
        recommendations = []
        
        # Originality recommendations
        originality_score = final_scores.get('originality_score', 0)
        if originality_score < 70:
            recommendations.append({
                'type': 'error',
                'icon': '🚨',
                'title': 'Plagiarism Risk Detected',
                'message': f'Your document shows {100-originality_score:.0f}% similarity with existing sources.',
                'actions': [
                    'Review highlighted sections for potential plagiarism',
                    'Paraphrase similar content in your own words',
                    'Add proper citations for all referenced material',
                    'Use quotation marks for direct quotes'
                ]
            })
        elif originality_score < 85:
            recommendations.append({
                'type': 'warning',
                'icon': '⚠️',
                'title': 'Improve Originality',
                'message': f'Score: {originality_score:.0f}/100. Some sections need more original expression.',
                'actions': [
                    'Rephrase common phrases in unique ways',
                    'Add your own analysis and insights',
                    'Reduce reliance on source material'
                ]
            })
        else:
            recommendations.append({
                'type': 'success',
                'icon': '✅',
                'title': 'Excellent Originality!',
                'message': f'Score: {originality_score:.0f}/100. Your work is highly original.',
                'actions': [
                    'Maintain this level of originality',
                    'Continue with unique insights'
                ]
            })
        
        # Tone recommendations
        tone_score = final_scores.get('tone_score', 0)
        if tone_score < 70:
            recommendations.append({
                'type': 'error',
                'icon': '📝',
                'title': 'Academic Tone Needs Work',
                'message': f'Score: {tone_score:.0f}/100. Writing style needs improvement.',
                'actions': [
                    'Use more formal academic language',
                    'Replace informal words with academic alternatives',
                    'Remove contractions (don\'t → do not)',
                    'Maintain consistent professional tone'
                ]
            })
        elif tone_score < 85:
            recommendations.append({
                'type': 'warning',
                'icon': '📝',
                'title': 'Enhance Academic Tone',
                'message': f'Score: {tone_score:.0f}/100. Good, but can be better.',
                'actions': [
                    'Strengthen academic vocabulary',
                    'Maintain formal tone consistently'
                ]
            })
        
        # Citation recommendations
        citation_score = final_scores.get('citation_score', 0)
        if citation_score < 70:
            recommendations.append({
                'type': 'error',
                'icon': '📚',
                'title': 'Citations Required',
                'message': f'Score: {citation_score:.0f}/100. Many statements lack sources.',
                'actions': [
                    'Add citations for factual claims',
                    'Ensure all data and statistics are cited',
                    'Follow APA/MLA format consistently',
                    'Include a complete reference list'
                ]
            })
        
        # Structure recommendations
        structure_score = final_scores.get('structure_score', 0)
        if structure_score < 80:
            recommendations.append({
                'type': 'warning',
                'icon': '🏗️',
                'title': 'Improve Structure',
                'message': f'Score: {structure_score:.0f}/100. Organization needs enhancement.',
                'actions': [
                    'Add clear section headings',
                    'Improve paragraph transitions',
                    'Ensure logical flow of ideas',
                    'Balance section lengths'
                ]
            })
        
        # Display recommendations in a user-friendly way
        for rec in recommendations:
            if rec['type'] == 'error':
                with st.container():
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
                        border-left: 5px solid #ef4444;
                        border-radius: 14px;
                        padding: 24px;
                        margin: 16px 0;
                        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.15);
                    ">
                        <div style="display: flex; align-items: center; margin-bottom: 12px;">
                            <span style="font-size: 32px; margin-right: 12px;">{rec['icon']}</span>
                            <h4 style="margin: 0; color: #991b1b; font-size: 20px; font-weight: 700;">{rec['title']}</h4>
                        </div>
                        <p style="color: #991b1b; font-size: 16px; margin: 8px 0 16px 0; font-weight: 500;">{rec['message']}</p>
                        <div style="background: white; padding: 16px; border-radius: 8px;">
                            <p style="color: #991b1b; font-weight: 700; margin: 0 0 12px 0; font-size: 14px;">ACTION STEPS:</p>
                            {''.join([f'<p style="color: #991b1b; margin: 8px 0; font-size: 15px;">• {action}</p>' for action in rec['actions']])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            elif rec['type'] == 'warning':
                with st.container():
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
                        border-left: 5px solid #f59e0b;
                        border-radius: 14px;
                        padding: 24px;
                        margin: 16px 0;
                        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.15);
                    ">
                        <div style="display: flex; align-items: center; margin-bottom: 12px;">
                            <span style="font-size: 32px; margin-right: 12px;">{rec['icon']}</span>
                            <h4 style="margin: 0; color: #92400e; font-size: 20px; font-weight: 700;">{rec['title']}</h4>
                        </div>
                        <p style="color: #92400e; font-size: 16px; margin: 8px 0 16px 0; font-weight: 500;">{rec['message']}</p>
                        <div style="background: white; padding: 16px; border-radius: 8px;">
                            <p style="color: #92400e; font-weight: 700; margin: 0 0 12px 0; font-size: 14px;">ACTION STEPS:</p>
                            {''.join([f'<p style="color: #92400e; margin: 8px 0; font-size: 15px;">• {action}</p>' for action in rec['actions']])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            else:  # success
                with st.container():
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
                        border-left: 5px solid #22c55e;
                        border-radius: 14px;
                        padding: 24px;
                        margin: 16px 0;
                        box-shadow: 0 2px 8px rgba(34, 197, 94, 0.15);
                    ">
                        <div style="display: flex; align-items: center; margin-bottom: 12px;">
                            <span style="font-size: 32px; margin-right: 12px;">{rec['icon']}</span>
                            <h4 style="margin: 0; color: #166534; font-size: 20px; font-weight: 700;">{rec['title']}</h4>
                        </div>
                        <p style="color: #166534; font-size: 16px; margin: 8px 0 16px 0; font-weight: 500;">{rec['message']}</p>
                        <div style="background: white; padding: 16px; border-radius: 8px;">
                            <p style="color: #166534; font-weight: 700; margin: 0 0 12px 0; font-size: 14px;">KEEP IT UP:</p>
                            {''.join([f'<p style="color: #166534; margin: 8px 0; font-size: 15px;">• {action}</p>' for action in rec['actions']])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Detailed Data
        with st.expander("View Detailed Analysis"):
            st.json(results)
        
        # Download
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.download_button(
                label="Download Report",
                data=str(results),
                file_name=f"report_{uploaded_file.name}.txt",
                mime="text/plain",
                use_container_width=True
            )


if __name__ == "__main__":
    run_dashboard()   
