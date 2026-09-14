"""
Base interface for converters.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple

class BaseConverter(ABC):
    @abstractmethod
    def convert(self, input_file: Path, output_file: Path) -> Tuple[bool, str]:
        """
        Convert the input_file to PDF and save it as output_file.
        Returns (success, error_message).
        """
        pass

