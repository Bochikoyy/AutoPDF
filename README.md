# AutoPDF

> **Download it. AutoPDF handles the rest.**

AutoPDF is a Python-based Windows background file-processing utility that monitors filesystem events and automatically converts supported newly downloaded or saved files into PDF documents using asynchronous conversion workers and local conversion engines.

## Features

- **Automatic folder monitoring:** Watches your Downloads folder (and others) for new files.
- **Offline conversion:** 100% local processing. Your files never leave your computer.
- **No uploading required:** Just download a file in your browser, and a PDF appears next to it.
- **Original files preserved:** Safely keeps your original files by default.
- **Intelligent download detection:** Waits for browsers to completely finish downloading before starting conversion.
- **Duplicate handling:** Never silently overwrites existing PDFs.
- **System Tray Integration:** Runs quietly in the background on Windows.

## Supported Formats

- **Documents:** `.doc`, `.docx`, `.odt`, `.rtf`
- **Presentations:** `.ppt`, `.pptx`, `.odp`
- **Spreadsheets:** `.xls`, `.xlsx`, `.ods`
- **Images:** `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`
- **Text:** `.txt`

## Architecture

```text
File Downloaded
      ↓
Folder Watcher
      ↓
File Validation
      ↓
Download Completion Check
      ↓
Conversion Queue
      ↓
Background Worker
      ↓
Converter (LibreOffice / Pillow / FPDF)
      ↓
PDF
      ↓
Database + Notification
```

## Installation

### Prerequisites
- Windows 10 or 11
- Python 3.12+
- **LibreOffice:** Must be installed in a standard location (`C:\Program Files\LibreOffice`) for Office document conversions.

### Setup
1. Clone or download the repository.
2. Create a virtual environment:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
4. Run the application:
   ```cmd
   python main.py
   ```

## Development

Run tests using pytest:
```cmd
pytest tests/
```

## Privacy

AutoPDF is entirely offline. No files, metadata, or telemetry are uploaded to any external servers or APIs.

## Packaging

To package AutoPDF into a single executable for Windows, PyInstaller is recommended (use `build.spec`).
