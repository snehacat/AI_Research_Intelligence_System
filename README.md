# 🧠 AI Research Intelligence System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An industry-grade AI system for comprehensive research paper analysis, featuring plagiarism detection, quality assessment, and academic guidance generation.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
streamlit run app/main.py

# 3. Open browser to http://localhost:8501
```

That's it! The app will start immediately.

## 🌟 Features

### Core Capabilities
- **Multi-Engine Plagiarism Detection**
  - Exact matching using Rabin-Karp algorithm
  - Lexical similarity via TF-IDF analysis
  - Semantic understanding with transformer models
  - Universal truth filtering for common knowledge

- **Research Quality Analysis**
  - Academic tone assessment
  - Citation validation and analysis
  - Document structure evaluation
  - Readability scoring

- **Intelligent Guidance System**
  - Contextual improvement suggestions
  - Academic writing recommendations
  - Citation formatting guidance
  - Structural enhancement advice

- **Comprehensive Reporting**
  - Detailed plagiarism breakdowns
  - Visual analytics and charts
  - Section-wise analysis
  - Exportable reports (PDF/HTML)

### 🔌 API Integrations (6 APIs)

**Always Active (No Keys Required):**
- ✅ **arXiv API** - Search 2M+ research papers
- ✅ **Wikipedia API** - Common knowledge validation
- ✅ **LanguageTool API** - Grammar & style checking

**Optional (Enhanced Features):**
- 🔗 **CrossRef API** - DOI validation & citations

**📖 Quick Start:** See [QUICK_START_APIS.md](QUICK_START_APIS.md)  
**📚 Full Guide:** See [API_INTEGRATION_GUIDE.md](API_INTEGRATION_GUIDE.md)  
**🏗️ Architecture:** See [API_ARCHITECTURE.md](API_ARCHITECTURE.md)

**Note:** All APIs are FREE! No paid services required.

## 🏗️ Architecture

### Technology Stack
- **UI Framework**: Streamlit
- **NLP Processing**: spaCy, NLTK
- **ML Models**: Sentence Transformers, Scikit-learn
- **Document Processing**: PyPDF2, python-docx
- **Visualization**: Plotly
- **Configuration**: Pydantic Settings

### Mathematical Model

The system uses a hybrid weighted similarity model:

```
P_i = (α × EMS_i) + (β × LSS_i) + (γ × SSS_i) + (δ × API_i)
```

Where:
- **EMS** (Exact Match Score): Rabin-Karp rolling hash
- **LSS** (Lexical Similarity Score): TF-IDF cosine similarity
- **SSS** (Semantic Similarity Score): Transformer embeddings
- **API** (API-based Score): External API analysis

Default weights: α=0.3, β=0.2, γ=0.3, δ=0.2

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

### Web Interface

1. **Upload Document**
   - Supported formats: PDF, DOCX, TXT
   - Maximum size: 50MB (configurable)

2. **Select Analysis Mode**
   - Local Analysis: Uses local ML models
   - API-Based Analysis: Leverages external APIs
   - Hybrid Mode: Combines both approaches

3. **Configure Options**
   - Analysis depth
   - Reference corpus
   - Detection sensitivity

4. **Review Results**
   - Plagiarism score and breakdown
   - Quality metrics
   - Improvement suggestions
   - Visual analytics

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
│   ├── main.py                   # Entry point
│   ├── dashboard.py              # Local analysis UI
│   ├── api_dashboard.py          # API-based analysis UI
│   └── config.py                 # Configuration management
│
├── plagiarism_engine/            # Plagiarism detection
│   ├── rabin_karp.py            # Exact matching
│   ├── tfidf_engine.py          # Lexical similarity
│   ├── semantic_engine.py       # Semantic analysis
│   └── universal_truth_filter.py # Common knowledge filter
│
├── quality_analyzer/             # Quality assessment
│   ├── tone_checker.py          # Academic tone analysis
│   ├── citation_checker.py      # Citation validation
│   ├── structure_analyzer.py    # Document structure
│   ├── readability.py           # Readability metrics
│   └── scoring_engine.py        # Unified scoring
│
├── guidance_engine/              # Guidance generation
│   ├── plagiarism_guidance.py   # Plagiarism suggestions
│   ├── tone_guidance.py         # Tone improvements
│   ├── citation_guidance.py     # Citation fixes
│   ├── structure_guidance.py    # Structure enhancements
│   └── improvement_path.py      # Action plans
│
├── api_integrations/             # External APIs
│   ├── openai_client.py         # OpenAI integration
│   ├── semantic_scholar_client.py
│   ├── crossref_client.py
│   ├── arxiv_client.py
│   ├── wikipedia_client.py
│   └── language_tool_client.py
│
├── utils/                        # Utilities
│   ├── preprocessing.py         # Text preprocessing
│   ├── file_handler.py          # File I/O
│   ├── logger.py                # Logging
│   ├── exceptions.py            # Custom exceptions
│   └── similarity_utils.py      # Similarity helpers
│
├── data/                         # Data files
│   ├── common_knowledge.json    # Universal truths
│   ├── academic_replacement_words.json
│   └── reference_corpus/        # Reference documents
│
├── tests/                        # Test suite
│   ├── test_plagiarism_engine/
│   ├── test_quality_analyzer/
│   └── test_utils/
│
├── reports/                      # Generated reports
│   └── generated_reports/
│
├── requirements.txt              # Dependencies
├── pyproject.toml               # Project configuration
├── .env.example                 # Environment template
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
