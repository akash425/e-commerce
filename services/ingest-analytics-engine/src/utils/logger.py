"""
Simple logging setup.
All modules use the same logger configuration.
"""

import logging
from pathlib import Path
from utils.config import LOGS_DIR

# Create logs directory if it doesn't exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Log file path
LOG_FILE = LOGS_DIR / "ingestion.log"

# Set up file handler
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.INFO)

# Simple log format: timestamp - level - message
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the standard configuration.
    
    Args:
        name: Name of the logger (usually __name__)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger

