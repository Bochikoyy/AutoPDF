"""
Background worker thread for processing the conversion queue.
"""
import threading
from app.core.queue_manager import ConversionQueue, ConversionTask
from app.core.file_validator import get_converter_type
from app.core.duplicate_handler import get_unique_output_path
from app.converters.office_converter import OfficeConverter
from datetime import datetime
from app.database.repository import ConversionRepository
from app.services.notification_service import show_notification
from app.utils.constants import STATUS_PROCESSING, STATUS_SUCCESS, STATUS_FAILED
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class ConversionWorker(threading.Thread):
    def __init__(self, queue_manager: ConversionQueue, office_converter: OfficeConverter, repository: ConversionRepository):
        super().__init__()
        self.queue_manager = queue_manager
        self.office_converter = office_converter
        self.repository = repository
        self.daemon = True
        self.running = True

    def run(self):
        logger.info("Conversion Worker started.")
        while self.running:
            try:
                # Block until a task is available
                task = self.queue_manager.q.get(timeout=1.0)
                if not self.running:
                    self.queue_manager.q.put(task) # Put it back
                    break
                    
                self.process_task(task)
                self.queue_manager.task_done(task)
            except Exception as e:
                # queue.Empty exception is handled implicitly by timeout
                if type(e).__name__ != 'Empty':
                    logger.error(f"Error in worker thread: {e}")

    def process_task(self, task: ConversionTask):
        logger.info(f"Processing task: {task.input_file.name}")
        
        if task.record_id:
            self.repository.update_status(
                record_id=task.record_id,
                status=STATUS_PROCESSING,
                started_at=datetime.now()
            )
            
        converter_type = get_converter_type(task.input_file)
        
        output_file = get_unique_output_path(task.input_file, task.output_dir)
        
        success = False
        error_msg = ""
        
        if converter_type == 'office':
            success, error_msg = self.office_converter.convert(task.input_file, output_file)
        elif converter_type == 'image':
            from app.converters.image_converter import ImageConverter
            success, error_msg = ImageConverter().convert(task.input_file, output_file)
        elif converter_type == 'text':
            from app.converters.text_converter import TextConverter
            success, error_msg = TextConverter().convert(task.input_file, output_file)
        else:
            logger.error(f"Unsupported converter type for {task.input_file.name}")
            success = False
            error_msg = "Unsupported file type"

        if success:
            logger.info(f"Successfully converted {task.input_file.name} to {output_file.name}")
            show_notification("Conversion Complete", f"Successfully converted {task.input_file.name} to PDF.")
            if task.record_id:
                self.repository.update_status(
                    record_id=task.record_id,
                    status=STATUS_SUCCESS,
                    output_path=str(output_file.resolve()),
                    completed_at=datetime.now()
                )
        else:
            logger.error(f"Failed to convert {task.input_file.name}: {error_msg}")
            show_notification("Conversion Failed", f"Failed to convert {task.input_file.name}.")
            if task.record_id:
                self.repository.update_status(
                    record_id=task.record_id,
                    status=STATUS_FAILED,
                    error_message=error_msg,
                    completed_at=datetime.now()
                )

    def stop(self):
        self.running = False
