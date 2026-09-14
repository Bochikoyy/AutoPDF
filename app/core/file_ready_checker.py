"""
Checks if a file has completely finished downloading.
"""
import time
from pathlib import Path
from app.utils.constants import STABILITY_CHECK_INTERVAL, STABILITY_CHECK_COUNT, MAX_WAIT_TIME
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

def wait_until_file_ready(file_path: Path) -> bool:
    """
    Wait until the file size stabilizes and the file can be opened.
    Returns True if the file is ready, False if it timed out or disappeared.
    """
    logger.info(f"Checking stability for {file_path.name}")
    start_time = time.time()
    consecutive_unchanged = 0
    last_size = -1
    
    while time.time() - start_time < MAX_WAIT_TIME:
        if not file_path.exists():
            logger.warning(f"File disappeared while checking stability: {file_path.name}")
            return False
            
        try:
            current_size = file_path.stat().st_size
            
            if current_size == last_size and current_size > 0:
                consecutive_unchanged += 1
            else:
                consecutive_unchanged = 0
                last_size = current_size
                
            if consecutive_unchanged >= STABILITY_CHECK_COUNT:
                # Try to open the file to ensure it's not locked
                try:
                    with open(file_path, 'rb') as f:
                        pass
                    logger.info(f"File {file_path.name} is stable and ready.")
                    return True
                except PermissionError:
                    # File is locked, keep waiting
                    consecutive_unchanged = 0
                    
        except Exception as e:
            logger.warning(f"Error checking file stability for {file_path.name}: {e}")
            
        time.sleep(STABILITY_CHECK_INTERVAL)
        
    logger.error(f"Timeout waiting for file to stabilize: {file_path.name}")
    return False

