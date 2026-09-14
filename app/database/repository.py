from datetime import datetime
from typing import List, Optional
from app.database.database import DatabaseConnection
from app.database.models import ConversionRecord
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class ConversionRepository:
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection

    def insert(self, record: ConversionRecord) -> int:
        query = '''
            INSERT INTO conversions (
                original_path, output_path, original_name, original_extension,
                original_size, status, error_message, detected_at, started_at, completed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (
                record.original_path,
                record.output_path,
                record.original_name,
                record.original_extension,
                record.original_size,
                record.status,
                record.error_message,
                record.detected_at.isoformat() if record.detected_at else None,
                record.started_at.isoformat() if record.started_at else None,
                record.completed_at.isoformat() if record.completed_at else None
            ))
            conn.commit()
            return cursor.lastrowid

    def update_status(self, record_id: int, status: str, output_path: str = None, 
                      error_message: str = None, started_at: datetime = None, 
                      completed_at: datetime = None):
        updates = ["status = ?"]
        params = [status]

        if output_path is not None:
            updates.append("output_path = ?")
            params.append(output_path)
        if error_message is not None:
            updates.append("error_message = ?")
            params.append(error_message)
        if started_at is not None:
            updates.append("started_at = ?")
            params.append(started_at.isoformat())
        if completed_at is not None:
            updates.append("completed_at = ?")
            params.append(completed_at.isoformat())

        params.append(record_id)
        
        query = f"UPDATE conversions SET {', '.join(updates)} WHERE id = ?"
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def get_recent(self, limit: int = 50) -> List[ConversionRecord]:
        query = "SELECT * FROM conversions ORDER BY detected_at DESC LIMIT ?"
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            
            records = []
            for row in rows:
                records.append(self._row_to_record(row))
            return records
            
    def _row_to_record(self, row) -> ConversionRecord:
        def parse_dt(dt_str):
            if dt_str:
                return datetime.fromisoformat(dt_str)
            return None
            
        return ConversionRecord(
            id=row['id'],
            original_path=row['original_path'],
            output_path=row['output_path'],
            original_name=row['original_name'],
            original_extension=row['original_extension'],
            original_size=row['original_size'],
            status=row['status'],
            error_message=row['error_message'],
            detected_at=parse_dt(row['detected_at']),
            started_at=parse_dt(row['started_at']),
            completed_at=parse_dt(row['completed_at'])
        )

