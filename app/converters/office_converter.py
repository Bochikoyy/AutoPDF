"""
Office document converter using Microsoft Office COM.
"""
from pathlib import Path
from typing import Tuple
from app.converters.base_converter import BaseConverter
from app.services.msoffice_service import MsOfficeService
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class OfficeConverter(BaseConverter):
    def __init__(self, msoffice_service: MsOfficeService):
        self.office_service = msoffice_service

    def convert(self, input_file: Path, output_file: Path) -> Tuple[bool, str]:
        if not self.office_service.is_available():
            return False, "Microsoft Office integration is not available."
            
        success, error = self.office_service.convert_to_pdf(input_file, output_file)
        
        if success:
            if output_file.exists():
                return True, ""
            else:
                return False, f"Expected output file {output_file} not found after conversion."
                
        return False, error

