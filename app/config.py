"""
Industry-grade configuration management with environment variables,
validation, and type safety using Pydantic.
"""
import os
from pathlib import Path
from typing import Dict, Optional
from enum import Enum

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(str, Enum):
    """Logging levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class AnalysisDepth(str, Enum):
    """Analysis depth levels"""
    QUICK = "Quick"
    STANDARD = "Standard"
    DEEP = "Deep"


class Settings(BaseSettings):
    """Application settings with validation and environment variable support"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Project paths
    project_root: Path = Field(default_factory=lambda: Path(__file__).parent.parent)
    data_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "data")
    reports_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent / "reports" / "generated_reports"
    )
    models_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "models")
    
    # API Keys (Optional)
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    semantic_scholar_api_key: Optional[str] = Field(
        default=None, alias="SEMANTIC_SCHOLAR_API_KEY"
    )
    crossref_api_key: Optional[str] = Field(default=None, alias="CROSSREF_API_KEY")
    
    # API Endpoints
    language_tool_api: str = "https://api.languagetool.org/v2/check"
    semantic_scholar_api: str = "https://api.semanticscholar.org/graph/v1/paper/search"
    crossref_api: str = "https://api.crossref.org/works"
    arxiv_api: str = "http://export.arxiv.org/api/query"
    wikipedia_api: str = "https://en.wikipedia.org/w/api.php"
    
    # Logging
    log_level: LogLevel = Field(default=LogLevel.INFO, alias="LOG_LEVEL")
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: Optional[Path] = Field(default=None)
    
    # Analysis Settings
    default_analysis_depth: AnalysisDepth = Field(
        default=AnalysisDepth.STANDARD, alias="DEFAULT_ANALYSIS_DEPTH"
    )
    enable_api_caching: bool = Field(default=True, alias="ENABLE_API_CACHING")
    max_reference_papers: int = Field(default=10, alias="MAX_REFERENCE_PAPERS", ge=1, le=100)
    cache_ttl_seconds: int = Field(default=3600, ge=60)
    
    # Plagiarism Detection Settings
    rabin_karp_window_size: int = Field(default=5, ge=3, le=15)
    tfidf_ngram_range: tuple[int, int] = Field(default=(1, 3))
    semantic_model_name: str = "all-MiniLM-L6-v2"
    plagiarism_threshold_low: float = Field(default=0.15, ge=0.0, le=1.0)
    plagiarism_threshold_medium: float = Field(default=0.35, ge=0.0, le=1.0)
    plagiarism_threshold_high: float = Field(default=0.60, ge=0.0, le=1.0)
    
    # Section Weights for Hybrid Analysis
    section_weights: Dict[str, float] = Field(
        default={
            "abstract": 0.8,
            "introduction": 1.0,
            "literature_review": 1.2,
            "methodology": 1.0,
            "results": 1.1,
            "discussion": 1.0,
            "conclusion": 0.9,
            "references": 0.5,
            "default": 1.0,
        }
    )
    
    # Hybrid Model Weights (α, β, γ, δ)
    # EMS (Exact Match), LSS (Lexical), SSS (Semantic), API (API-based)
    hybrid_weights: Dict[str, float] = Field(
        default={
            "alpha": 0.3,  # Exact Match Score (Rabin-Karp)
            "beta": 0.2,   # Lexical Similarity Score (TF-IDF)
            "gamma": 0.3,  # Semantic Similarity Score (Transformers)
            "delta": 0.2,  # API-based Score
        }
    )
    
    # Quality Analysis Settings
    min_citation_count: int = Field(default=5, ge=0)
    readability_target_grade: float = Field(default=12.0, ge=1.0, le=20.0)
    tone_formality_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    
    # API Rate Limiting
    api_rate_limit_calls: int = Field(default=100, ge=1)
    api_rate_limit_period: int = Field(default=60, ge=1)  # seconds
    api_timeout_seconds: int = Field(default=30, ge=1)
    api_max_retries: int = Field(default=3, ge=0, le=10)
    
    # File Processing
    max_file_size_mb: int = Field(default=50, ge=1, le=500)
    supported_file_types: list[str] = Field(default=[".pdf", ".docx", ".txt"])
    
    # Performance
    enable_multiprocessing: bool = Field(default=True)
    max_workers: int = Field(default=4, ge=1, le=16)
    chunk_size: int = Field(default=1000, ge=100)
    
    @field_validator("hybrid_weights")
    @classmethod
    def validate_hybrid_weights(cls, v: Dict[str, float]) -> Dict[str, float]:
        """Ensure hybrid weights sum to 1.0"""
        total = sum(v.values())
        if not (0.99 <= total <= 1.01):  # Allow small floating point errors
            raise ValueError(f"Hybrid weights must sum to 1.0, got {total}")
        return v
    
    @field_validator("plagiarism_threshold_medium")
    @classmethod
    def validate_medium_threshold(cls, v: float, info) -> float:
        """Ensure medium threshold is greater than low threshold"""
        if "plagiarism_threshold_low" in info.data and v <= info.data["plagiarism_threshold_low"]:
            raise ValueError("Medium threshold must be greater than low threshold")
        return v
    
    @field_validator("plagiarism_threshold_high")
    @classmethod
    def validate_high_threshold(cls, v: float, info) -> float:
        """Ensure high threshold is greater than medium threshold"""
        if "plagiarism_threshold_medium" in info.data and v <= info.data["plagiarism_threshold_medium"]:
            raise ValueError("High threshold must be greater than medium threshold")
        return v
    
    def ensure_directories(self) -> None:
        """Create necessary directories if they don't exist"""
        for directory in [self.data_dir, self.reports_dir, self.models_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def has_openai_key(self) -> bool:
        """Check if OpenAI API key is configured"""
        return self.openai_api_key is not None and len(self.openai_api_key) > 0
    
    def has_semantic_scholar_key(self) -> bool:
        """Check if Semantic Scholar API key is configured"""
        return self.semantic_scholar_api_key is not None and len(self.semantic_scholar_api_key) > 0
    
    def has_crossref_key(self) -> bool:
        """Check if CrossRef API key is configured"""
        return self.crossref_api_key is not None and len(self.crossref_api_key) > 0
    
    def get_api_status(self) -> Dict[str, bool]:
        """Get status of all API integrations"""
        return {
            "openai": self.has_openai_key(),
            "semantic_scholar": self.has_semantic_scholar_key(),
            "crossref": self.has_crossref_key(),
            "arxiv": True,  # No key required
            "wikipedia": True,  # No key required
            "language_tool": True,  # No key required
        }


# Global settings instance
settings = Settings()

# Ensure directories exist on import
settings.ensure_directories()


# Export commonly used values
__all__ = [
    "settings",
    "Settings",
    "LogLevel",
    "AnalysisDepth",
]
