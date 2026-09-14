import pystray
from PIL import Image
from PySide6.QtCore import QObject, Signal, QThread

class TrayThread(QThread):
    show_window_signal = Signal()
    quit_signal = Signal()

    def __init__(self, icon_path):
        super().__init__()
        self.icon_path = icon_path
        self.tray = None

    def run(self):
        # Create a simple icon if missing
        try:
            image = Image.open(self.icon_path)
        except:
            image = Image.new('RGB', (64, 64), color = (73, 109, 137))
            
        menu = pystray.Menu(
            pystray.MenuItem("Open AutoPDF", self.on_open),
            pystray.MenuItem("Exit AutoPDF", self.on_exit)
        )
        
        self.tray = pystray.Icon("AutoPDF", image, "AutoPDF", menu)
        self.tray.run()

    def on_open(self, icon, item):
        self.show_window_signal.emit()

    def on_exit(self, icon, item):
        self.tray.stop()
        self.quit_signal.emit()

    def stop(self):
        if self.tray:
            self.tray.stop()

