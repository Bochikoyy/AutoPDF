"""
Handles generation of unique output filenames to prevent overwriting.
"""
from pathlib import Path

def get_unique_output_path(original_path: Path, output_dir: Path) -> Path:
    """
    Generate a unique output path for the PDF to avoid overwrites.
    Example: report.pdf -> report (1).pdf
    """
    base_name = original_path.stem
    target_path = output_dir / f"{base_name}.pdf"
    
    counter = 1
    while target_path.exists():
        target_path = output_dir / f"{base_name} ({counter}).pdf"
        counter += 1
        
    return target_path

