"""
Logging configuration for AutoPDF.
"""
import logging
from logging.handlers import RotatingFileHandler

from app.utils.paths import get_logs_dir

def setup_logger(name: str = "AutoPDF") -> logging.Logger:
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times if logger is requested again
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    log_file = get_logs_dir() / "autopdf.log"

    # Format
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File Handler
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

