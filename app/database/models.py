from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ConversionRecord:
    id: Optional[int]
    original_path: str
    output_path: Optional[str]
    original_name: str
    original_extension: str
    original_size: int
    status: str
    error_message: Optional[str]
    detected_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

