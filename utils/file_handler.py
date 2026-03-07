"""
Industry-grade file handling with robust error handling, validation,
and support for multiple file formats.
"""
import io
from pathlib import Path
from typing import Union, BinaryIO, Optional
import mimetypes

from PyPDF2 import PdfReader
from docx import Document

from app.config import settings
from utils.logger import get_logger
from utils.exceptions import (
    UnsupportedFileTypeError,
    FileSizeExceededError,
    FileCorruptedError,
    FileProcessingError,
)

logger = get_logger(__name__)


class FileHandler:
    """
    Robust file handler with validation, error handling, and multiple format support.
    """
    
    def __init__(self, max_size_mb: Optional[int] = None):
        """
        Initialize file handler.
        
        Args:
            max_size_mb: Maximum file size in MB (defaults to settings)
        """
        self.max_size_mb = max_size_mb or settings.max_file_size_mb
        self.max_size_bytes = self.max_size_mb * 1024 * 1024
        self.supported_extensions = settings.supported_file_types
        
    def extract_text(self, uploaded_file: Union[BinaryIO, str, Path]) -> str:
        """
        Extract text from uploaded file with comprehensive error handling.
        
        Args:
            uploaded_file: File object (Streamlit uploader) or file path
            
        Returns:
            Extracted text content
            
        Raises:
            UnsupportedFileTypeError: If file type is not supported
            FileSizeExceededError: If file size exceeds maximum
            FileCorruptedError: If file is corrupted or unreadable
            FileProcessingError: For other processing errors
        """
        try:
            # Get filename and validate
            filename = self._get_filename(uploaded_file)
            logger.info(f"Processing file: {filename}")
            
            # Validate file type
            self._validate_file_type(filename)
            
            # Validate file size
            self._validate_file_size(uploaded_file)
            
            # Extract text based on file type
            file_ext = Path(filename).suffix.lower()
            
            if file_ext == ".pdf":
                text = self._extract_pdf(uploaded_file)
            elif file_ext == ".docx":
                text = self._extract_docx(uploaded_file)
            elif file_ext == ".txt":
                text = self._extract_txt(uploaded_file)
            else:
                raise UnsupportedFileTypeError(
                    f"Unsupported file type: {file_ext}",
                    details={"filename": filename, "extension": file_ext}
                )
            
            # Validate extracted text
            if not text or len(text.strip()) == 0:
                raise FileProcessingError(
                    "No text content extracted from file",
                    details={"filename": filename}
                )
            
            logger.info(f"Successfully extracted {len(text)} characters from {filename}")
            return text.strip()
            
        except (UnsupportedFileTypeError, FileSizeExceededError, FileCorruptedError):
            raise
        except Exception as e:
            logger.error(f"Unexpected error processing file: {e}", exc_info=True)
            raise FileProcessingError(
                f"Failed to process file: {str(e)}",
                details={"error_type": type(e).__name__}
            )
    
    def _get_filename(self, file: Union[BinaryIO, str, Path]) -> str:
        """Get filename from file object or path"""
        if isinstance(file, (str, Path)):
            return str(file)
        elif hasattr(file, 'name'):
            return file.name
        else:
            raise FileProcessingError("Cannot determine filename from file object")
    
    def _validate_file_type(self, filename: str) -> None:
        """Validate file type is supported"""
        file_ext = Path(filename).suffix.lower()
        if file_ext not in self.supported_extensions:
            raise UnsupportedFileTypeError(
                f"File type '{file_ext}' is not supported",
                details={
                    "filename": filename,
                    "supported_types": self.supported_extensions
                }
            )
    
    def _validate_file_size(self, file: Union[BinaryIO, str, Path]) -> None:
        """Validate file size doesn't exceed maximum"""
        try:
            if isinstance(file, (str, Path)):
                file_size = Path(file).stat().st_size
            elif hasattr(file, 'size'):
                file_size = file.size
            elif hasattr(file, 'getvalue'):
                file_size = len(file.getvalue())
            else:
                # Try to get size by reading
                current_pos = file.tell() if hasattr(file, 'tell') else 0
                file.seek(0, 2)  # Seek to end
                file_size = file.tell()
                file.seek(current_pos)  # Restore position
            
            if file_size > self.max_size_bytes:
                raise FileSizeExceededError(
                    f"File size ({file_size / 1024 / 1024:.2f} MB) exceeds maximum allowed ({self.max_size_mb} MB)",
                    details={
                        "file_size_mb": file_size / 1024 / 1024,
                        "max_size_mb": self.max_size_mb
                    }
                )
        except FileSizeExceededError:
            raise
        except Exception as e:
            logger.warning(f"Could not validate file size: {e}")
    
    def _extract_pdf(self, file: BinaryIO) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PdfReader(file)
            
            if len(pdf_reader.pages) == 0:
                raise FileCorruptedError("PDF file contains no pages")
            
            text_parts = []
            for page_num, page in enumerate(pdf_reader.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
                except Exception as e:
                    logger.warning(f"Failed to extract text from page {page_num}: {e}")
            
            if not text_parts:
                raise FileCorruptedError("Could not extract any text from PDF")
            
            return "\n".join(text_parts)
            
        except FileCorruptedError:
            raise
        except Exception as e:
            logger.error(f"PDF extraction error: {e}", exc_info=True)
            raise FileCorruptedError(
                f"Failed to read PDF file: {str(e)}",
                details={"error_type": type(e).__name__}
            )
    
    def _extract_docx(self, file: BinaryIO) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file)
            
            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
            
            if not paragraphs:
                raise FileCorruptedError("DOCX file contains no readable text")
            
            return "\n".join(paragraphs)
            
        except FileCorruptedError:
            raise
        except Exception as e:
            logger.error(f"DOCX extraction error: {e}", exc_info=True)
            raise FileCorruptedError(
                f"Failed to read DOCX file: {str(e)}",
                details={"error_type": type(e).__name__}
            )
    
    def _extract_txt(self, file: BinaryIO) -> str:
        """Extract text from TXT file"""
        try:
            # Try UTF-8 first
            try:
                if hasattr(file, 'getvalue'):
                    content = file.getvalue().decode("utf-8")
                else:
                    content = file.read().decode("utf-8")
                    if hasattr(file, 'seek'):
                        file.seek(0)  # Reset for potential re-reading
            except UnicodeDecodeError:
                # Fallback to latin-1
                logger.warning("UTF-8 decoding failed, trying latin-1")
                if hasattr(file, 'getvalue'):
                    content = file.getvalue().decode("latin-1")
                else:
                    if hasattr(file, 'seek'):
                        file.seek(0)
                    content = file.read().decode("latin-1")
            
            if not content.strip():
                raise FileCorruptedError("TXT file is empty")
            
            return content
            
        except FileCorruptedError:
            raise
        except Exception as e:
            logger.error(f"TXT extraction error: {e}", exc_info=True)
            raise FileCorruptedError(
                f"Failed to read TXT file: {str(e)}",
                details={"error_type": type(e).__name__}
            )


# Convenience function for backward compatibility
def extract_text(uploaded_file: Union[BinaryIO, str, Path]) -> str:
    """
    Extract text from uploaded file (convenience function).
    
    Args:
        uploaded_file: File object or path
        
    Returns:
        Extracted text content
    """
    handler = FileHandler()
    return handler.extract_text(uploaded_file)


__all__ = ["FileHandler", "extract_text"]