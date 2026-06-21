# 🧠 AI Research Intelligence System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An industry-grade AI system for comprehensive research paper analysis, featuring multi-engine plagiarism detection, quality assessment, sentence-level analysis, and automated report generation. Built with modern NLP technologies including Rabin-Karp, TF-IDF, and Transformer models.

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone <repository-url>
cd AI_Research_Intelligence_System

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLP models
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# 5. Run the application
streamlit run app/main.py

# 6. Open browser to http://localhost:8501
```

That's it! The app will start immediately.

## 🌟 Features

### Core Capabilities
- **Multi-Engine Plagiarism Detection**
  - 🔍 Exact matching using Rabin-Karp rolling hash algorithm
  - 📊 Lexical similarity via TF-IDF cosine similarity
  - 🧠 Semantic understanding with Sentence-BERT transformer models
  - ✅ Universal truth filtering for common knowledge
  - ⚖️ Hybrid weighted scoring model (α, β, γ, δ)

- **Research Quality Analysis**
  - 📝 Academic tone assessment and formality scoring
  - 📚 Citation validation and completeness analysis
  - 🏗️ Document structure evaluation (sections, flow, coherence)
  - 📖 Readability scoring (Flesch-Kincaid, Gunning Fog)
  - 🎯 Multi-dimensional quality metrics

- **Sentence-Level Analysis** (Grammarly-style)
  - 🔍 Individual sentence feedback
  - ⚠️ Passive voice detection
  - 👤 First-person usage warnings
  - 📏 Sentence length analysis
  - 📝 Informal language identification
  - ✅ Real-time suggestions for improvement

- **Intelligent Guidance System**
  - 💡 Contextual improvement suggestions
  - 🎓 Academic writing recommendations
  - 📚 Citation formatting guidance
  - 🏗️ Structural enhancement advice
  - 🛣️ Personalized improvement roadmaps

- **Professional Report Generation**
  - 📄 PDF reports with professional layouts
  - 📝 Editable DOCX reports
  - 📊 Visual analytics and interactive charts
  - 📈 Executive summaries and metrics
  - 💾 Downloadable in multiple formats

### 🔌 API Integrations (6 APIs)

**Always Active (No Keys Required):**
- ✅ **arXiv API** - Search 2M+ research papers
- ✅ **Wikipedia API** - Common knowledge validation
- ✅ **LanguageTool API** - Grammar & style checking

**Optional (Enhanced Features):**
- 🔗 **CrossRef API** - DOI validation & citations



**Note:** All APIs are FREE! No paid services required.

## 🏗️ Architecture & Program Flow

### Technology Stack
- **UI Framework**: Streamlit with multi-page navigation
- **NLP Processing**: spaCy (3.8+), NLTK (3.9+)
- **ML Models**: Sentence-BERT, Scikit-learn (1.8+)
- **Document Processing**: PyPDF2 (3.0+), python-docx (1.2+)
- **Report Generation**: ReportLab (4.0+) for PDF, python-docx for DOCX
- **Visualization**: Plotly (6.6+) for interactive charts
- **Configuration**: Pydantic Settings for type-safe configuration
- **API Integration**: httpx, requests with retry logic

### Program Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Interface (Streamlit)                    │
│                        app/main.py                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ├─► Dashboard (app/dashboard.py)
                         │   └─► Document Upload & Full Analysis
                         │       ├─► Text Extraction (utils/file_handler.py)
                         │       ├─► Multi-Engine Plagiarism Detection
                         │       │   ├─► Rabin-Karp (plagiarism_engine/rabin_karp.py)
                         │       │   ├─► TF-IDF (plagiarism_engine/tfidf_engine.py)
                         │       │   ├─► Semantic (plagiarism_engine/semantic_engine.py)
                         │       │   └─► Universal Truth Filter (plagiarism_engine/universal_truth_filter.py)
                         │       ├─► Quality Analysis
                         │       │   ├─► Tone Checker (quality_analyzer/tone_checker.py)
                         │       │   ├─► Citation Checker (quality_analyzer/citation_checker.py)
                         │       │   ├─► Structure Analyzer (quality_analyzer/structure_analyzer.py)
                         │       │   ├─► Readability (quality_analyzer/readability.py)
                         │       │   └─► Scoring Engine (quality_analyzer/scoring_engine.py)
                         │       ├─► Guidance Generation (guidance_engine/improvement_path.py)
                         │       └─► Visual Analytics (Plotly charts)
                         │
                         ├─► Sentence Analysis (app/pages/sentence_analysis.py)
                         │   └─► Sentence-level feedback (Grammarly-style)
                         │       ├─► Passive voice detection
                         │       ├─► Informal language identification
                         │       ├─► First-person usage warnings
                         │       └─► Sentence length analysis
                         │
                         ├─► Reports (app/pages/reports.py)
                         │   └─► Professional report generation
                         │       ├─► PDF generation (ReportLab)
                         │       ├─► DOCX generation (python-docx)
                         │       └─► Customizable sections
                         │
                         ├─► History (app/pages/history.py)
                         │   └─► Analysis history tracking
                         │
                         └─► Settings (app/pages/settings.py)
                             └─► Configuration management
```

### Mathematical Model

The system uses a hybrid weighted similarity model:

```
P_i = (α × EMS_i) + (β × LSS_i) + (γ × SSS_i) + (δ × API_i)
```

Where:
- **EMS** (Exact Match Score): Rabin-Karp rolling hash with configurable window size
- **LSS** (Lexical Similarity Score): TF-IDF cosine similarity with n-gram analysis
- **SSS** (Semantic Similarity Score): Transformer embeddings (all-MiniLM-L6-v2)
- **API** (API-based Score): External API analysis (Semantic Scholar, CrossRef, arXiv)

Default weights (configurable in app/config.py): α=0.3, β=0.2, γ=0.3, δ=0.2

### Data Flow

1. **Input**: User uploads document (PDF/DOCX/TXT) through Dashboard
2. **Extraction**: Text extracted with metadata preservation
3. **Preprocessing**: Tokenization, normalization, sentence segmentation
4. **Parallel Analysis**:
   - Plagiarism engines run concurrently
   - Quality analyzers evaluate different aspects
   - API integrations fetch reference data
5. **Scoring**: Hybrid model combines all scores with weighted averaging
6. **Guidance**: AI generates personalized improvement suggestions
7. **Visualization**: Interactive charts and metrics displayed
8. **Output**: Results stored in session, exportable as PDF/DOCX reports

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager
- Virtual environment (recommended)

### Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd AI_Research_Intelligence_System
```

2. **Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download NLP models**
```bash
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

5. **Configure environment (optional)**
```bash
cp .env.example .env
# Edit .env with your API keys
```

6. **Run the application**
```bash
streamlit run app/main.py
```

The application will open in your browser at `http://localhost:8501`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# API Keys (Optional)
OPENAI_API_KEY=sk-your-key-here
SEMANTIC_SCHOLAR_API_KEY=your-key-here
CROSSREF_API_KEY=your-key-here

# Logging
LOG_LEVEL=INFO

# Analysis Settings
DEFAULT_ANALYSIS_DEPTH=Standard
ENABLE_API_CACHING=true
MAX_REFERENCE_PAPERS=10

# Plagiarism Thresholds
PLAGIARISM_THRESHOLD_LOW=0.15
PLAGIARISM_THRESHOLD_MEDIUM=0.35
PLAGIARISM_THRESHOLD_HIGH=0.60
```

### Configuration Options

All settings can be configured via environment variables or the `app/config.py` file:

- **File Processing**: Max file size, supported formats
- **Analysis Depth**: Quick, Standard, or Deep analysis
- **Model Selection**: Choose transformer models
- **Thresholds**: Customize plagiarism detection sensitivity
- **Performance**: Multiprocessing, batch sizes, caching

## 🚀 Usage

### Web Interface Navigation

The application features a professional multi-page interface:

#### 1. **Dashboard** (Main Analysis)
   - Upload document (PDF, DOCX, TXT - max 50MB)
   - Automatic text extraction with preprocessing
   - Real-time multi-engine analysis:
     - Plagiarism detection with risk level indicators
     - Quality scoring with interactive gauges
     - Visual analytics with Plotly charts
   - Smart AI recommendations with actionable steps
   - Overall quality score (0-100)

#### 2. **Sentence Analysis** (Grammarly-style)
   - Upload document for sentence-level feedback
   - Individual sentence analysis with:
     - Passive voice warnings
     - Informal language detection
     - First-person usage identification
     - Sentence length recommendations
   - Filter by: All / Issues Only / Clean Sentences
   - Real-time suggestions for each sentence

#### 3. **Reports**
   - Generate professional reports from analyses
   - Choose format: PDF (print-ready) or DOCX (editable)
   - Customizable sections:
     - Executive Summary
     - Quality Metrics
     - Recommendations
   - One-click download with timestamp

#### 4. **History**
   - View past analyses
   - Track improvements over time
   - Access previous results

#### 5. **Settings**
   - Configure analysis parameters
   - Manage API keys (optional)
   - Adjust detection thresholds
   - Customize weights and preferences

### Programmatic Usage

```python
from plagiarism_engine.rabin_karp import RabinKarpPlagiarism
from plagiarism_engine.tfidf_engine import TFIDFSimilarity
from plagiarism_engine.semantic_engine import SemanticSimilarity
from utils.preprocessing import TextPreprocessor

# Initialize engines
rk_engine = RabinKarpPlagiarism(window_size=5)
tfidf_engine = TFIDFSimilarity()
semantic_engine = SemanticSimilarity()

# Preprocess text
preprocessor = TextPreprocessor()
doc_words = preprocessor.preprocess_for_tokens(document_text)
doc_sentences = preprocessor.tokenize_sentences(document_text)

# Run analysis
rk_result = rk_engine.calculate_similarity(doc_words, reference_words_list)
tfidf_result = tfidf_engine.calculate_similarity(document_text, reference_texts)
semantic_result = semantic_engine.calculate_similarity(doc_sentences, ref_sentences)

# Combine scores
final_score = (
    0.3 * rk_result.similarity_score +
    0.2 * tfidf_result.similarity_score +
    0.3 * semantic_result.similarity_score
)
```

## 📊 Project Structure

```
AI_Research_Intelligence_System/
│
├── app/                          # Application layer
│   ├── main.py                   # Entry point with multi-page navigation
│   ├── dashboard.py              # Main analysis dashboard with visual analytics
│   ├── config.py                 # Pydantic-based configuration management
│   └── pages/                    # Multi-page application modules
│       ├── sentence_analysis.py  # Sentence-level feedback (Grammarly-style)
│       ├── reports.py            # PDF/DOCX report generation
│       ├── history.py            # Analysis history tracking
│       └── settings.py           # User preferences and configuration
│
├── plagiarism_engine/            # Multi-engine plagiarism detection
│   ├── rabin_karp.py            # Exact matching with rolling hash
│   ├── tfidf_engine.py          # Lexical similarity with TF-IDF
│   ├── semantic_engine.py       # Semantic analysis with Transformers
│   └── universal_truth_filter.py # Common knowledge filtering
│
├── quality_analyzer/             # Multi-dimensional quality assessment
│   ├── tone_checker.py          # Academic tone and formality analysis
│   ├── citation_checker.py      # Citation validation and completeness
│   ├── structure_analyzer.py    # Document structure and coherence
│   ├── readability.py           # Readability metrics (Flesch-Kincaid, etc.)
│   ├── scoring_engine.py        # Unified scoring system
│   └── api_based_scoring_engine.py # API-enhanced scoring
│
├── guidance_engine/              # AI-powered guidance generation
│   ├── plagiarism_guidance.py   # Plagiarism-specific suggestions
│   ├── tone_guidance.py         # Tone improvement recommendations
│   ├── citation_guidance.py     # Citation formatting guidance
│   ├── structure_guidance.py    # Structure enhancement advice
│   └── improvement_path.py      # Personalized improvement roadmaps
│
├── api_integrations/             # External API clients with retry logic
│   ├── openai_client.py         # OpenAI GPT integration (optional)
│   ├── semantic_scholar_client.py # Academic paper search
│   ├── crossref_client.py       # DOI validation and metadata
│   ├── arxiv_client.py          # arXiv paper search
│   ├── wikipedia_client.py      # Common knowledge validation
│   └── language_tool_client.py  # Grammar and style checking
│
├── utils/                        # Utility modules
│   ├── preprocessing.py         # Text preprocessing and tokenization
│   ├── file_handler.py          # Document I/O (PDF, DOCX, TXT)
│   ├── logger.py                # Structured logging
│   ├── exceptions.py            # Custom exception classes
│   └── similarity_utils.py      # Similarity calculation helpers
│
├── data/                         # Data files and knowledge bases
│   ├── common_knowledge.json    # Universal truths database
│   ├── academic_replacement_words.json # Academic vocabulary
│   └── reference_corpus/        # Reference documents (optional)
│
├── tests/                        # Test suite
│   ├── test_plagiarism_engine/  # Plagiarism detection tests
│   │   └── test_rabin_karp.py
│   ├── test_quality_analyzer/   # Quality analysis tests
│   └── test_utils/              # Utility tests
│       └── test_preprocessing.py
│
├── reports/                      # Generated reports directory
│   └── generated_reports/       # Saved PDF/DOCX reports
│
├── models/                       # Cached ML models
│
├── .github/                      # GitHub configuration
│   └── workflows/
│       └── ci.yml               # CI/CD pipeline configuration
│
├── .streamlit/                   # Streamlit configuration
│   └── config.toml              # App theme and settings
│
├── requirements.txt              # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore patterns
└── README.md                    # This file
```

## 🧪 Testing

Run the test suite:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_plagiarism_engine/test_rabin_karp.py
```

## 🔧 Development

### Code Quality

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy .
```

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

## 📈 Performance

- **Processing Speed**: ~1000 words/second
- **Memory Usage**: ~500MB for standard analysis
- **Supported File Size**: Up to 50MB
- **Concurrent Processing**: Multi-threaded analysis
- **Caching**: Intelligent embedding caching

## 🛡️ Security

- API keys stored in environment variables
- Input validation and sanitization
- File size and type restrictions
- Rate limiting for API calls
- Secure error handling

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Sentence Transformers for semantic models
- spaCy for NLP processing
- Streamlit for the web framework
- The open-source community

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the documentation
- Review the setup guide

## 🗺️ Roadmap

- [ ] Multi-language support
- [ ] Real-time collaboration
- [ ] Advanced citation network analysis
- [ ] Integration with reference managers
- [ ] Mobile application
- [ ] Cloud deployment options

---

**Built with ❤️ for the academic community**
