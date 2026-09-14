import sys
import time
from app.utils.logger import setup_logger
from app.utils.paths import get_default_downloads_dir
from app.services.msoffice_service import MsOfficeService
from app.converters.office_converter import OfficeConverter
from app.core.queue_manager import ConversionQueue
from app.core.worker import ConversionWorker
from app.core.watcher import FolderWatcher
from app.core.settings import SettingsManager

from app.database.database import DatabaseConnection
from app.database.repository import ConversionRepository

logger = setup_logger()

def main():
    logger.info("Starting AutoPDF Engine MVP")
    
    settings = SettingsManager()
    
    db_conn = DatabaseConnection()
    repository = ConversionRepository(db_conn)
    
    office_service = MsOfficeService()
    office_converter = OfficeConverter(office_service)
    
    queue_manager = ConversionQueue()
    
    worker = ConversionWorker(queue_manager, office_converter, repository)
    worker.start()
    
    watcher = FolderWatcher(queue_manager, repository)
    downloads_dir = get_default_downloads_dir()
    
    if downloads_dir.exists():
        watcher.add_folder(downloads_dir)
    else:
        logger.error(f"Downloads folder not found at: {downloads_dir}")
        
    # Load initial state from settings
    is_active = settings.get("is_active", True)
    watcher.set_active(is_active)
    
    watcher.start()
    
    # Start PyQt Application
    from PySide6.QtWidgets import QApplication
    from app.ui.main_window import MainWindow
    
    qapp = QApplication(sys.argv)
    
    # Simple app context to pass around
    app_context = {
        'db': repository,
        'queue': queue_manager,
        'watcher': watcher,
        'worker': worker,
        'office_service': office_service,
        'settings': settings
    }
    
    window = MainWindow(app_context)
    window.show()
    
    try:
        sys.exit(qapp.exec())
    finally:
        logger.info("Shutting down...")
        watcher.stop()
        worker.stop()
        worker.join(timeout=2.0)
        logger.info("AutoPDF shutdown complete.")

if __name__ == "__main__":
    main()
