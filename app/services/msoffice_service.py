"""
Service to execute Microsoft Office COM automation for document conversions.
"""
import pythoncom
import win32com.client
from pathlib import Path
from typing import Tuple
from app.utils.logger import setup_logger
from app.utils.constants import SUPPORTED_DOCUMENTS, SUPPORTED_PRESENTATIONS, SUPPORTED_SPREADSHEETS

logger = setup_logger(__name__)

class MsOfficeService:
    def __init__(self):
        self.available = True

    def is_available(self) -> bool:
        return self.available

    def convert_to_pdf(self, input_file: Path, output_file: Path, timeout: int = 120) -> Tuple[bool, str]:
        """
        Convert an office document to PDF using Microsoft Office COM.
        """
        if not input_file.exists():
            return False, f"Input file does not exist: {input_file}"

        ext = input_file.suffix.lower()
        
        # COM must be initialized in the thread that uses it
        pythoncom.CoInitialize()
        
        try:
            if ext in SUPPORTED_DOCUMENTS:
                return self._convert_word(input_file, output_file)
            elif ext in SUPPORTED_PRESENTATIONS:
                return self._convert_powerpoint(input_file, output_file)
            elif ext in SUPPORTED_SPREADSHEETS:
                return self._convert_excel(input_file, output_file)
            else:
                return False, f"Unsupported file extension for MS Office: {ext}"
        finally:
            pythoncom.CoUninitialize()

    def _convert_word(self, in_file: Path, out_file: Path) -> Tuple[bool, str]:
        word = None
        doc = None
        try:
            word = win32com.client.DispatchEx("Word.Application")
            word.Visible = False
            # wdExportFormatPDF = 17
            doc = word.Documents.Open(str(in_file.resolve()), ReadOnly=True)
            doc.SaveAs(str(out_file.resolve()), FileFormat=17)
            return True, ""
        except Exception as e:
            logger.error(f"Word COM error: {e}")
            return False, str(e)
        finally:
            if doc:
                try:
                    doc.Close(SaveChanges=False)
                except Exception:
                    pass
            if word:
                try:
                    word.Quit()
                except Exception:
                    pass

    def _convert_powerpoint(self, in_file: Path, out_file: Path) -> Tuple[bool, str]:
        powerpoint = None
        presentation = None
        try:
            powerpoint = win32com.client.DispatchEx("Powerpoint.Application")
            # ppSaveAsPDF = 32
            presentation = powerpoint.Presentations.Open(str(in_file.resolve()), ReadOnly=True, WithWindow=False)
            presentation.SaveAs(str(out_file.resolve()), 32)
            return True, ""
        except Exception as e:
            logger.error(f"PowerPoint COM error: {e}")
            return False, str(e)
        finally:
            if presentation:
                try:
                    presentation.Close()
                except Exception:
                    pass
            if powerpoint:
                try:
                    powerpoint.Quit()
                except Exception:
                    pass

    def _convert_excel(self, in_file: Path, out_file: Path) -> Tuple[bool, str]:
        excel = None
        wb = None
        try:
            excel = win32com.client.DispatchEx("Excel.Application")
            excel.Visible = False
            excel.DisplayAlerts = False
            # xlTypePDF = 0
            wb = excel.Workbooks.Open(str(in_file.resolve()), ReadOnly=True)
            wb.ExportAsFixedFormat(0, str(out_file.resolve()))
            return True, ""
        except Exception as e:
            logger.error(f"Excel COM error: {e}")
            return False, str(e)
        finally:
            if wb:
                try:
                    wb.Close(SaveChanges=False)
                except Exception:
                    pass
            if excel:
                try:
                    excel.Quit()
                except Exception:
                    pass

