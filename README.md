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
Converter (Microsoft Office COM / Pillow / FPDF)
      ↓
PDF
      ↓
Database + Notification
```

## Installation

### Prerequisites
- Windows 10 or 11
- Python 3.12+
- **Microsoft Office:** Word, PowerPoint, and Excel must be installed for Office document conversions.

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

## Step-by-Step Usage Guide

### 1. Starting AutoPDF
1. Open File Explorer and navigate to the `dist` folder.
2. Double-click **`AutoPDF.exe`**.
3. The app will launch silently. Check the bottom right of your screen (in the System Tray near the clock) for the AutoPDF icon. This confirms it is running in the background.

### 2. Converting a File
1. Open your browser or apps like Microsoft Teams.
2. Download a supported file (like a `.pptx` or `.docx`) into your standard **Downloads** folder.
3. Don't click anything—just wait a few seconds! 
4. AutoPDF automatically detects the file, waits for it to finish downloading, and commands Microsoft Office in the background to convert it.
5. A **Windows Notification** will appear when the conversion is successful.
6. Check your Downloads folder. You will find your original file untouched, with the new `.pdf` version right next to it!

### 3. Running Automatically on Startup
If you want AutoPDF to run automatically every time you turn on your computer:
1. Press `Windows Key + R` to open the Run dialog.
2. Type `shell:startup` and press Enter. This opens the Windows Startup folder.
3. Right-click your `AutoPDF.exe` file, choose **Create Shortcut**, and drag that shortcut into the Startup folder.

## Development

Run tests using pytest:
```cmd
pytest tests/
```

## Privacy

AutoPDF is entirely offline. No files, metadata, or telemetry are uploaded to any external servers or APIs. All conversions happen entirely on your own local hardware.


