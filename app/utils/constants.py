"""
Constants for AutoPDF.
"""

APP_NAME = "AutoPDF"
APP_VERSION = "1.0.0"

SUPPORTED_DOCUMENTS = {".doc", ".docx", ".odt", ".rtf"}
SUPPORTED_PRESENTATIONS = {".ppt", ".pptx", ".odp"}
SUPPORTED_SPREADSHEETS = {".xls", ".xlsx", ".ods"}
SUPPORTED_OFFICE = SUPPORTED_DOCUMENTS | SUPPORTED_PRESENTATIONS | SUPPORTED_SPREADSHEETS

SUPPORTED_IMAGES = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
SUPPORTED_TEXT = {".txt"}

ALL_SUPPORTED_EXTENSIONS = SUPPORTED_OFFICE | SUPPORTED_IMAGES | SUPPORTED_TEXT

KNOWN_TEMP_EXTENSIONS = {".crdownload", ".part", ".tmp", ".download"}

# Conversion Statuses
STATUS_WAITING = "WAITING"
STATUS_PROCESSING = "PROCESSING"
STATUS_SUCCESS = "SUCCESS"
STATUS_FAILED = "FAILED"
STATUS_SKIPPED = "SKIPPED"

# File Stability settings
STABILITY_CHECK_INTERVAL = 1.0  # seconds
STABILITY_CHECK_COUNT = 3       # Number of consecutive unchanged sizes required
MAX_WAIT_TIME = 300             # seconds

