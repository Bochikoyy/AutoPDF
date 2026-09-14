"""
Filesystem watchdog to monitor directories for new files.
"""
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from app.core.file_validator import is_valid_file
from app.core.file_ready_checker import wait_until_file_ready
from app.core.queue_manager import ConversionQueue, ConversionTask
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

from datetime import datetime
from app.database.models import ConversionRecord
from app.database.repository import ConversionRepository
from app.utils.constants import STATUS_WAITING

class AutoPDFEventHandler(FileSystemEventHandler):
    def __init__(self, queue_manager: ConversionQueue, repository: ConversionRepository):
        super().__init__()
        self.queue_manager = queue_manager
        self.repository = repository
        
    def process_file(self, file_path: Path):
        """Validates the file, waits for readiness, and adds to queue."""
        if not is_valid_file(file_path):
            return
            
        def _wait_and_queue():
            if wait_until_file_ready(file_path):
                # For now, output dir is the same as input dir
                record = ConversionRecord(
                    id=None,
                    original_path=str(file_path.resolve()),
                    output_path=None,
                    original_name=file_path.name,
                    original_extension=file_path.suffix,
                    original_size=file_path.stat().st_size,
                    status=STATUS_WAITING,
                    error_message=None,
                    detected_at=datetime.now(),
                    started_at=None,
                    completed_at=None
                )
                record_id = self.repository.insert(record)
                
                task = ConversionTask(
                    input_file=file_path,
                    output_dir=file_path.parent,
                    record_id=record_id
                )
                self.queue_manager.add_task(task)
                
        # Launch wait process in a daemon thread so it doesn't block the watcher
        t = threading.Thread(target=_wait_and_queue, daemon=True)
        t.start()

    def on_created(self, event):
        if event.is_directory:
            return
        logger.info(f"File created: {event.src_path}")
        self.process_file(Path(event.src_path))
        
    def on_moved(self, event):
        if event.is_directory:
            return
        logger.info(f"File moved to: {event.dest_path}")
        self.process_file(Path(event.dest_path))

class FolderWatcher:
    def __init__(self, queue_manager: ConversionQueue, repository: ConversionRepository):
        self.observer = Observer()
        self.event_handler = AutoPDFEventHandler(queue_manager, repository)
        self.watches = {} # path_str: watch
        
    def add_folder(self, folder_path: Path):
        if not folder_path.exists():
            logger.warning(f"Cannot watch {folder_path} as it does not exist.")
            return
            
        path_str = str(folder_path.resolve())
        if path_str in self.watches:
            return
            
        watch = self.observer.schedule(self.event_handler, path_str, recursive=False)
        self.watches[path_str] = watch
        logger.info(f"Started monitoring folder: {path_str}")
        
    def remove_folder(self, folder_path: Path):
        path_str = str(folder_path.resolve())
        if path_str in self.watches:
            self.observer.unschedule(self.watches[path_str])
            del self.watches[path_str]
            logger.info(f"Stopped monitoring folder: {path_str}")

    def start(self):
        self.observer.start()
        logger.info("Folder Watcher started.")
        
    def stop(self):
        self.observer.stop()
        self.observer.join()
        logger.info("Folder Watcher stopped.")
