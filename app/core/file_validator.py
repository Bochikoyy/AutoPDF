"""
Validates files to see if they are supported and not temporary.
"""
from pathlib import Path
from app.utils.constants import ALL_SUPPORTED_EXTENSIONS, KNOWN_TEMP_EXTENSIONS
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

def is_valid_file(file_path: Path) -> bool:
    """Check if the file is supported and not a temporary file."""
    if not file_path.is_file():
        return False
        
    ext = file_path.suffix.lower()
    
    if ext in KNOWN_TEMP_EXTENSIONS:
        return False
        
    if ext == ".pdf":
        return False

    if ext in ALL_SUPPORTED_EXTENSIONS:
        return True
        
    return False

def get_converter_type(file_path: Path) -> str:
    """Returns 'office', 'image', 'text', or None"""
    from app.utils.constants import SUPPORTED_OFFICE, SUPPORTED_IMAGES, SUPPORTED_TEXT
    ext = file_path.suffix.lower()
    if ext in SUPPORTED_OFFICE:
        return 'office'
    elif ext in SUPPORTED_IMAGES:
        return 'image'
    elif ext in SUPPORTED_TEXT:
        return 'text'
    return None

