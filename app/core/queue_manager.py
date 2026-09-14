"""
Manages the conversion queue.
"""
import queue
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ConversionTask:
    input_file: Path
    output_dir: Path
    record_id: int = None
    # Future attributes like settings for this specific folder

class ConversionQueue:
    def __init__(self):
        self.q = queue.Queue()
        self.currently_processing = set()

    def add_task(self, task: ConversionTask):
        # Avoid duplicate tasks for the same file
        file_path_str = str(task.input_file.resolve())
        if file_path_str not in self.currently_processing:
            self.currently_processing.add(file_path_str)
            self.q.put(task)

    def get_task(self) -> ConversionTask:
        return self.q.get()

    def task_done(self, task: ConversionTask):
        file_path_str = str(task.input_file.resolve())
        if file_path_str in self.currently_processing:
            self.currently_processing.remove(file_path_str)
        self.q.task_done()
        
    def empty(self):
        return self.q.empty()
