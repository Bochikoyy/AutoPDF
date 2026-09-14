from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QStackedWidget
from PySide6.QtCore import Qt

from app.ui.dashboard import DashboardView
from app.ui.history import HistoryView
from app.ui.folders import FoldersView
from app.ui.settings import SettingsView
from app.ui.about import AboutView

class MainWindow(QMainWindow):
    def __init__(self, app_context):
        super().__init__()
        self.app_context = app_context
        self.setWindowTitle("AutoPDF")
        self.resize(900, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.addItems(["Dashboard", "History", "Folders", "Settings", "About"])
        self.sidebar.currentRowChanged.connect(self.display_view)
        
        # Style sidebar (basic styling)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #2b2b2b;
                color: white;
                border: none;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 15px 20px;
            }
            QListWidget::item:selected {
                background-color: #3b3b3b;
                border-left: 4px solid #4a90e2;
            }
        """)
        
        # Content Area
        self.stack = QStackedWidget()
        
        self.dashboard_view = DashboardView(app_context)
        self.history_view = HistoryView(app_context)
        self.folders_view = FoldersView(app_context)
        self.settings_view = SettingsView(app_context)
        self.about_view = AboutView()
        
        self.stack.addWidget(self.dashboard_view)
        self.stack.addWidget(self.history_view)
        self.stack.addWidget(self.folders_view)
        self.stack.addWidget(self.settings_view)
        self.stack.addWidget(self.about_view)
        
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.stack)
        
        # Set initial view
        self.sidebar.setCurrentRow(0)
        
        # Setup Tray
        from app.tray.system_tray import TrayThread
        import os
        
        # create a dummy icon file if none exists
        icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "icons", "icon.png")
        
        self.tray_thread = TrayThread(icon_path)
        self.tray_thread.show_window_signal.connect(self.show_normal)
        self.tray_thread.quit_signal.connect(self.quit_app)
        self.tray_thread.start()
        
    def display_view(self, index):
        self.stack.setCurrentIndex(index)
        
    def show_normal(self):
        self.showNormal()
        self.activateWindow()

    def quit_app(self):
        from PySide6.QtWidgets import QApplication
        QApplication.quit()
        
    def closeEvent(self, event):
        # We want to minimize to tray, not close the app
        event.ignore()
        self.hide()
