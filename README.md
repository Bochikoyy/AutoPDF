<h1 align="center">AutoPDF</h1>

<p align="center">
  Download it. Save it. AutoPDF turns it into a PDF automatically.
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" />
  <img alt="Platform" src="https://img.shields.io/badge/platform-Windows-0078D4?logo=windows&logoColor=white" />
  <img alt="Desktop UI" src="https://img.shields.io/badge/UI-PySide6-41CD52?logo=qt&logoColor=white" />
  <img alt="Offline" src="https://img.shields.io/badge/conversion-local%20%26%20offline-16A34A" />
  <img alt="License" src="https://img.shields.io/badge/license-MIT-7C3AED" />
</p>

## About

**AutoPDF** is a Windows desktop utility that watches your default Downloads folder and automatically converts newly created supported files into PDF documents.

Keep AutoPDF running, download or save a supported file into `C:\Users\<YourName>\Downloads`, and the application handles the rest. It waits until the file has finished downloading, places the conversion in a background queue, creates the PDF beside the original file, compresses the result, records the attempt locally, and displays a Windows notification.

The original file is preserved. If a PDF with the same name already exists, AutoPDF creates a numbered copy instead of overwriting it.

## How it works

```text
New file created or moved into Downloads
                    ↓
          Extension validation
                    ↓
        File stability and lock check
                    ↓
            Conversion queue
                    ↓
          Background worker thread
                    ↓
   Office COM / Pillow / FPDF converter
                    ↓
          In-place PDF compression
                    ↓
   SQLite record + Windows notification
```

## Current features

### Automatic conversion

- Watches the current Windows user's default Downloads folder
- Detects files created directly in the folder or moved into it
- Ignores PDFs, unsupported formats, and temporary browser-download files
- Waits for the file size to remain unchanged before processing
- Processes conversions in a background worker so the UI remains available
- Can pause or resume automatic detection from the Dashboard

### Safe output handling

- Preserves the source file
- Writes the PDF into the same folder as the source
- Avoids overwriting existing PDFs
- Uses numbered names such as `report (1).pdf` and `report (2).pdf`
- Attempts to compress every successfully created PDF with PyMuPDF
- Keeps the created PDF even if the compression step fails

### Desktop experience

- PySide6 desktop dashboard
- Automatic conversion ON/OFF control
- Minimize-to-system-tray behavior when the window is closed
- Tray menu actions for reopening or exiting AutoPDF
- Windows toast notifications for successful and failed conversions
- Local rotating log files for troubleshooting
- Local SQLite records for conversion status and output paths

## Supported formats

| Category | Extensions | Conversion engine | Additional requirement |
| --- | --- | --- | --- |
| Documents | `.doc`, `.docx`, `.odt`, `.rtf` | Microsoft Word COM automation | Microsoft Word |
| Presentations | `.ppt`, `.pptx`, `.odp` | Microsoft PowerPoint COM automation | Microsoft PowerPoint |
| Spreadsheets | `.xls`, `.xlsx`, `.ods` | Microsoft Excel COM automation | Microsoft Excel |
| Images | `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`, `.jfif` | Pillow | None beyond Python dependencies |
| Text | `.txt` | FPDF2 | None beyond Python dependencies |

> OpenDocument files (`.odt`, `.odp`, and `.ods`) are accepted by AutoPDF, but successful conversion depends on whether the installed Microsoft Office application can open that specific file correctly.

### Files intentionally ignored

AutoPDF does not reconvert existing PDFs. It also ignores the following temporary extensions while browsers and download managers are still writing files:

- `.crdownload`
- `.part`
- `.tmp`
- `.download`

## Step-by-step installation

### Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer; Python 3.12 is recommended
- Git, or a downloaded ZIP of this repository
- Microsoft Office only if you want to convert Word, PowerPoint, or Excel-compatible files

No Microsoft Office installation is required for image and plain-text conversion.

### 1. Clone the repository

Open **Command Prompt** or **PowerShell**, then run:

```powershell
git clone https://github.com/Bochikoyy/AutoPDF.git
cd AutoPDF
```

If you downloaded the project as a ZIP, extract it first and open a terminal inside the extracted `AutoPDF` folder.

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

In Command Prompt:

```bat
.venv\Scripts\activate.bat
```

In PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, run this once in the same window and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 4. Install the dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Start AutoPDF

```powershell
python main.py
```

The AutoPDF window should open with the **Dashboard** selected. The message **Automatic Conversion is ON** confirms that the Downloads watcher is active.

Keep this terminal open while running from source. AutoPDF stops when the process is terminated or when **Exit AutoPDF** is selected from the system-tray menu.

## Step-by-step usage guide

### 1. Start AutoPDF before downloading the file

Run `python main.py` and confirm that the Dashboard says **Automatic Conversion is ON**.

AutoPDF only reacts to new filesystem events. Files that were already inside Downloads before AutoPDF started are not automatically scanned or converted.

### 2. Download or save a supported file

Save the file directly into your default Downloads folder:

```text
C:\Users\<YourName>\Downloads
```

The current watcher is not recursive, so files created inside a Downloads subfolder are not detected automatically.

### 3. Let the download finish

You do not need to open or drag the file into AutoPDF. The application checks the file once per second and waits for three consecutive unchanged size checks. It also verifies that the file can be opened before adding it to the queue.

The readiness check can wait for up to five minutes before timing out.

### 4. Wait for conversion

AutoPDF chooses the converter from the file extension:

- Word, PowerPoint, and Excel-compatible files use Microsoft Office in the background
- Images use Pillow
- Plain-text files use FPDF2

Conversions are processed one at a time by the current background worker.

### 5. Find the PDF

The new PDF appears beside the original file in Downloads:

```text
Downloads/
├── class-presentation.pptx
└── class-presentation.pdf
```

If `class-presentation.pdf` already exists, AutoPDF creates:

```text
class-presentation (1).pdf
```

### 6. Check the result notification

Windows displays either:

- **Conversion Complete** when the PDF is created successfully
- **Conversion Failed** when the selected converter cannot finish the file

The original file remains untouched in both cases.

### 7. Keep AutoPDF in the system tray

Clicking the window's close button hides the dashboard instead of stopping the application. AutoPDF continues watching Downloads from the system tray.

Use the tray icon menu to:

- Select **Open AutoPDF** to show the dashboard again
- Select **Exit AutoPDF** to stop the application completely

### 8. Pause or resume automatic conversion

Open the Dashboard and select:

- **Turn OFF** to ignore new files temporarily
- **Turn ON** to resume watching for new files

Files created while detection is turned off are not processed later automatically.

## Optional: run AutoPDF when Windows starts

The repository contains startup-registry code, but the current interface does not expose or call it. For the present build, startup must be configured manually.

After creating a working executable:

1. Press `Windows + R`.
2. Enter `shell:startup` and press Enter.
3. Create a shortcut to `AutoPDF.exe`.
4. Move the shortcut into the Startup folder.
5. Restart Windows and verify that the AutoPDF tray icon appears.

## Optional: build a Windows executable

No prebuilt `AutoPDF.exe` or `dist` folder is currently committed to this repository. The supplied `build.spec` is intended for PyInstaller, but it references an `assets` directory that is not currently included in the repository.

Before packaging, either add the expected `assets` directory or remove its entry from `build.spec`. Then install PyInstaller and build:

```powershell
python -m pip install pyinstaller
pyinstaller build.spec
```

When the specification and assets are valid, the executable is generated under `dist/AutoPDF.exe`.

## Current interface status

| View | Current behavior |
| --- | --- |
| Dashboard | Functional ON/OFF control for automatic detection |
| History | Screen exists, but records are not displayed yet |
| Folders | Screen exists, but custom folders cannot be managed yet |
| Settings | Screen exists as a placeholder |
| About | Displays a short AutoPDF description |

The conversion engine already stores history in SQLite and the watcher already exposes folder-management methods, but those capabilities are not yet connected to the corresponding interface pages.

## Privacy

AutoPDF performs its conversion pipeline locally. The current source code contains no upload flow, cloud conversion API, analytics service, or telemetry integration.

Local runtime data is stored in:

| Path | Purpose |
| --- | --- |
| `data/autopdf.db` | SQLite conversion records |
| `logs/autopdf.log` | Rotating application and conversion logs |

When running a packaged executable, these folders are created beside the executable. When running from source, they are created in the repository root.

## Tech stack

| Area | Technology |
| --- | --- |
| Language | Python |
| Desktop UI | PySide6 / Qt |
| Folder monitoring | Watchdog |
| Windows integration | pywin32, winotify, pystray |
| Office conversion | Microsoft Office COM automation |
| Image conversion | Pillow |
| Text-to-PDF conversion | FPDF2 |
| PDF compression | PyMuPDF |
| Local persistence | SQLite |
| Testing | pytest |
| Windows packaging | PyInstaller specification |

## Project structure

| Path | Purpose |
| --- | --- |
| `main.py` | Starts the database, converters, worker, watcher, UI, and shutdown flow |
| `app/core/` | Validation, readiness checking, duplicate naming, queueing, watching, and worker logic |
| `app/converters/` | Office, image, and text converter implementations |
| `app/services/` | Microsoft Office automation, notifications, startup support, and inactive LibreOffice support code |
| `app/database/` | SQLite connection, conversion model, and repository |
| `app/tray/` | System-tray thread and menu actions |
| `app/ui/` | Dashboard, History, Folders, Settings, About, and main window |
| `app/utils/` | Constants, paths, logging, and PDF compression |
| `tests/` | Validator, readiness, and duplicate-name regression tests |
| `build.spec` | PyInstaller build configuration |

## Development

### Run the tests

Activate the virtual environment, then run:

```powershell
python -m pytest tests -v
```

The current suite checks:

- Supported, PDF, temporary, and unsupported-file validation
- Converter selection by extension
- File-readiness detection
- Duplicate-safe PDF output naming

### Runtime behavior worth knowing

- Monitoring is limited to the default Downloads folder and does not include subfolders.
- Only new create and move events are handled; there is no startup scan of existing files.
- Office conversion currently uses Microsoft Office COM. `LibreOfficeService` exists in the codebase but is not connected to the application startup or worker.
- The text converter uses Helvetica with Latin-1 replacement, so unsupported Unicode characters may be replaced in generated PDFs.
- Conversion records are written to SQLite, but the current History view does not render them.

## Roadmap

- Connect conversion records to the History view
- Add monitored-folder management to the Folders view
- Expose startup, output, and converter preferences in Settings
- Connect LibreOffice as an optional Office-conversion fallback
- Add startup scanning for supported files already present in watched folders
- Support recursive monitoring as an opt-in setting
- Add a packaged release with a real application icon and installer

## License

AutoPDF is released under the [MIT License](LICENSE).

Copyright © 2026 Chrisnel Caipang.
