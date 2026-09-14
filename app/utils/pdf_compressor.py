import fitz  # PyMuPDF
from pathlib import Path
from typing import Tuple
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

def compress_pdf(file_path: Path) -> Tuple[bool, str]:
    """
    Compresses a PDF file in-place using PyMuPDF.
    Returns (success, error_message).
    """
    temp_path = file_path.with_suffix('.temp.pdf')
    try:
        if not file_path.exists():
            return False, "File does not exist"
            
        doc = fitz.open(str(file_path))
        
        # Save to a temporary file with maximum compression settings
        # garbage=4: removes unused objects and duplicate streams
        # deflate=True: compresses data streams
        # clean=True: sanitizes content streams
        doc.save(
            str(temp_path),
            garbage=4,
            deflate=True,
            clean=True
        )
        doc.close()
        
        # Replace original file with compressed file
        temp_path.replace(file_path)
        
        logger.info(f"Successfully compressed {file_path.name}")
        return True, ""
        
    except Exception as e:
        logger.error(f"Failed to compress {file_path.name}: {e}")
        # Clean up temp file if it exists
        if temp_path.exists():
            try:
                temp_path.unlink()
            except Exception:
                pass
        return False, str(e)
