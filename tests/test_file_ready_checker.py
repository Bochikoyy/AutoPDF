import pytest
from pathlib import Path
from unittest.mock import patch

def test_wait_until_file_ready(tmp_path):
    file = tmp_path / "download.docx"
    file.write_text("dummy")
    
    with patch('app.core.file_ready_checker.STABILITY_CHECK_INTERVAL', 0.01), \
         patch('app.core.file_ready_checker.STABILITY_CHECK_COUNT', 2), \
         patch('app.core.file_ready_checker.MAX_WAIT_TIME', 1.0):
        
        from app.core.file_ready_checker import wait_until_file_ready
        
        assert wait_until_file_ready(file) is True

