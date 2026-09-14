"""
Service to detect and execute LibreOffice headless for document conversions.
"""
import subprocess
from pathlib import Path
from typing import Optional, Tuple
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class LibreOfficeService:
    def __init__(self):
        self.soffice_path = self.detect_libreoffice()

    def detect_libreoffice(self) -> Optional[Path]:
        """Detect the path to soffice.exe."""
        common_paths = [
            Path(r"C:\Program Files\LibreOffice\program\soffice.exe"),
            Path(r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"),
        ]

        for p in common_paths:
            if p.exists() and p.is_file():
                logger.info(f"LibreOffice detected at: {p}")
                return p
        
        logger.warning("LibreOffice not detected in standard locations.")
        return None

    def is_available(self) -> bool:
        return self.soffice_path is not None

    def set_libreoffice_path(self, path: str):
        """Allow manual override of the LibreOffice path."""
        p = Path(path)
        if p.exists() and p.is_file():
            self.soffice_path = p
            logger.info(f"LibreOffice path manually set to: {self.soffice_path}")

    def convert_to_pdf(self, input_file: Path, output_dir: Path, timeout: int = 120) -> Tuple[bool, str]:
        """
        Convert an office document to PDF using LibreOffice headless.
        Returns (success_bool, error_message)
        """
        if not self.is_available():
            return False, "LibreOffice is not available or path is not set."

        if not input_file.exists():
            return False, f"Input file does not exist: {input_file}"

        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

        # command: soffice.exe --headless --convert-to pdf --outdir OUTPUT_FOLDER INPUT_FILE
        cmd = [
            str(self.soffice_path),
            "--headless",
            "--convert-to", "pdf",
            "--outdir", str(output_dir),
            str(input_file)
        ]

        try:
            logger.info(f"Executing LibreOffice conversion for {input_file.name}")
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if process.returncode == 0:
                logger.info(f"Conversion successful for {input_file.name}")
                return True, ""
            else:
                logger.error(f"Conversion failed for {input_file.name}. Error: {process.stderr}")
                return False, process.stderr or "Unknown LibreOffice error."
        except subprocess.TimeoutExpired:
            logger.error(f"Conversion timed out for {input_file.name}")
            return False, "Conversion timed out."
        except Exception as e:
            logger.error(f"Exception during conversion for {input_file.name}: {e}")
            return False, str(e)

