from pathlib import Path
from typing import Tuple
from PIL import Image
from app.converters.base_converter import BaseConverter
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class ImageConverter(BaseConverter):
    def convert(self, input_file: Path, output_file: Path) -> Tuple[bool, str]:
        try:
            image = Image.open(input_file)
            # Convert to RGB if necessary (e.g. RGBA for PNG)
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
                
            image.save(output_file, "PDF", resolution=100.0)
            return True, ""
        except Exception as e:
            logger.error(f"Image conversion failed for {input_file.name}: {e}")
            return False, str(e)

