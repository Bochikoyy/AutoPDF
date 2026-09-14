"""
Path handling for AutoPDF.
"""
import sys
from pathlib import Path

def get_base_dir() -> Path:
    """Get the base directory of the application, accommodating for PyInstaller."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent.parent

def get_logs_dir() -> Path:
    """Get the logs directory."""
    path = get_base_dir() / "logs"
    path.mkdir(exist_ok=True, parents=True)
    return path

def get_data_dir() -> Path:
    """Get the data directory for the database."""
    path = get_base_dir() / "data"
    path.mkdir(exist_ok=True, parents=True)
    return path

def get_default_downloads_dir() -> Path:
    """Get the user's default Downloads directory."""
    return Path.home() / "Downloads"

