import pytest
from pathlib import Path
from app.core.file_validator import is_valid_file, get_converter_type

def test_is_valid_file_supported(tmp_path):
    file = tmp_path / "document.docx"
    file.write_text("dummy")
    assert is_valid_file(file) is True

def test_is_valid_file_pdf(tmp_path):
    file = tmp_path / "document.pdf"
    file.write_text("dummy")
    assert is_valid_file(file) is False

def test_is_valid_file_temp(tmp_path):
    file = tmp_path / "document.docx.crdownload"
    file.write_text("dummy")
    assert is_valid_file(file) is False

def test_is_valid_file_unsupported(tmp_path):
    file = tmp_path / "program.exe"
    file.write_text("dummy")
    assert is_valid_file(file) is False

def test_get_converter_type():
    assert get_converter_type(Path("test.docx")) == "office"
    assert get_converter_type(Path("test.pptx")) == "office"
    assert get_converter_type(Path("test.png")) == "image"
    assert get_converter_type(Path("test.txt")) == "text"
    assert get_converter_type(Path("test.exe")) is None

