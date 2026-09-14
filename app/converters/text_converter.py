from pathlib import Path
from typing import Tuple
from fpdf import FPDF
from app.converters.base_converter import BaseConverter
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class TextConverter(BaseConverter):
    def convert(self, input_file: Path, output_file: Path) -> Tuple[bool, str]:
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=11)
            
            with open(input_file, 'r', encoding='utf-8') as f:
                for line in f:
                    # Replace characters that can't be rendered by standard font if needed
                    text = line.strip('\n').encode('latin-1', 'replace').decode('latin-1')
                    pdf.multi_cell(0, 5, txt=text)
                    
            pdf.output(str(output_file))
            return True, ""
        except Exception as e:
            logger.error(f"Text conversion failed for {input_file.name}: {e}")
            return False, str(e)

