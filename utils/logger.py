"""
Centralized logging configuration with structured logging support.
"""
import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

from app.config import settings


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors"""
        if sys.stdout.isatty():  # Only use colors in terminal
            levelname = record.levelname
            if levelname in self.COLORS:
                record.levelname = (
                    f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
                )
        return super().format(record)


def setup_logger(
    name: str,
    level: Optional[str] = None,
    log_file: Optional[Path] = None
) -> logging.Logger:
    """
    Setup a logger with console and optional file handlers.
    
    Args:
        name: Logger name (usually __name__)
        level: Logging level (defaults to settings.log_level)
        log_file: Optional file path for logging
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Set level
    log_level = level or settings.log_level.value
    logger.setLevel(log_level)
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_formatter = ColoredFormatter(settings.log_format)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    file_path = log_file or settings.log_file
    if file_path:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(file_path, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(settings.log_format)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger with the given name.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return setup_logger(name)


# Create default application logger
app_logger = get_logger("ai_research_intelligence")


__all__ = ["setup_logger", "get_logger", "app_logger"]
