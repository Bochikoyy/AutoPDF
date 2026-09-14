import pytest
from pathlib import Path
from app.core.duplicate_handler import get_unique_output_path

def test_get_unique_output_path(tmp_path):
    original = tmp_path / "report.docx"
    
    # First conversion
    out1 = get_unique_output_path(original, tmp_path)
    assert out1.name == "report.pdf"
    
    # Simulate first PDF existing
    out1.write_text("dummy")
    
    # Second conversion
    out2 = get_unique_output_path(original, tmp_path)
    assert out2.name == "report (1).pdf"
    
    # Simulate second PDF existing
    out2.write_text("dummy")
    
    # Third conversion
    out3 = get_unique_output_path(original, tmp_path)
    assert out3.name == "report (2).pdf"

