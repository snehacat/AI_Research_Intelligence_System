"""
Custom exceptions for the AI Research Intelligence System.
Provides clear error messages and proper exception hierarchy.
"""
from typing import Optional, Any


class AIResearchException(Exception):
    """Base exception for all custom exceptions in the system"""
    
    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"{self.message} ({details_str})"
        return self.message


# File Processing Exceptions
class FileProcessingError(AIResearchException):
    """Raised when file processing fails"""
    pass


class UnsupportedFileTypeError(FileProcessingError):
    """Raised when file type is not supported"""
    pass


class FileSizeExceededError(FileProcessingError):
    """Raised when file size exceeds maximum allowed"""
    pass


class FileCorruptedError(FileProcessingError):
    """Raised when file is corrupted or unreadable"""
    pass


# API Exceptions
class APIError(AIResearchException):
    """Base exception for API-related errors"""
    pass


class APIKeyMissingError(APIError):
    """Raised when required API key is missing"""
    pass


class APIRateLimitError(APIError):
    """Raised when API rate limit is exceeded"""
    pass


class APITimeoutError(APIError):
    """Raised when API request times out"""
    pass


class APIResponseError(APIError):
    """Raised when API returns an error response"""
    pass


# Analysis Exceptions
class AnalysisError(AIResearchException):
    """Base exception for analysis-related errors"""
    pass


class InsufficientDataError(AnalysisError):
    """Raised when insufficient data for analysis"""
    pass


class ModelLoadError(AnalysisError):
    """Raised when ML model fails to load"""
    pass


class InvalidInputError(AnalysisError):
    """Raised when input data is invalid"""
    pass


# Plagiarism Detection Exceptions
class PlagiarismDetectionError(AnalysisError):
    """Raised when plagiarism detection fails"""
    pass


class ReferenceCorpusError(PlagiarismDetectionError):
    """Raised when reference corpus is invalid or missing"""
    pass


# Quality Analysis Exceptions
class QualityAnalysisError(AnalysisError):
    """Raised when quality analysis fails"""
    pass


class CitationAnalysisError(QualityAnalysisError):
    """Raised when citation analysis fails"""
    pass


class ToneAnalysisError(QualityAnalysisError):
    """Raised when tone analysis fails"""
    pass


class StructureAnalysisError(QualityAnalysisError):
    """Raised when structure analysis fails"""
    pass


# Configuration Exceptions
class ConfigurationError(AIResearchException):
    """Raised when configuration is invalid"""
    pass


class ValidationError(AIResearchException):
    """Raised when data validation fails"""
    pass


# Report Generation Exceptions
class ReportGenerationError(AIResearchException):
    """Raised when report generation fails"""
    pass


__all__ = [
    "AIResearchException",
    "FileProcessingError",
    "UnsupportedFileTypeError",
    "FileSizeExceededError",
    "FileCorruptedError",
    "APIError",
    "APIKeyMissingError",
    "APIRateLimitError",
    "APITimeoutError",
    "APIResponseError",
    "AnalysisError",
    "InsufficientDataError",
    "ModelLoadError",
    "InvalidInputError",
    "PlagiarismDetectionError",
    "ReferenceCorpusError",
    "QualityAnalysisError",
    "CitationAnalysisError",
    "ToneAnalysisError",
    "StructureAnalysisError",
    "ConfigurationError",
    "ValidationError",
    "ReportGenerationError",
]
