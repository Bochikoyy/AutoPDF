import sqlite3
from pathlib import Path
from app.utils.paths import get_data_dir
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class DatabaseConnection:
    def __init__(self):
        self.db_path = get_data_dir() / "autopdf.db"
        self._init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS conversions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        original_path TEXT NOT NULL,
                        output_path TEXT,
                        original_name TEXT,
                        original_extension TEXT,
                        original_size INTEGER,
                        status TEXT NOT NULL,
                        error_message TEXT,
                        detected_at DATETIME,
                        started_at DATETIME,
                        completed_at DATETIME
                    )
                ''')
                conn.commit()
                logger.info("Database initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")

