from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class DashboardView(QWidget):
    def __init__(self, app_context):
        super().__init__()
        self.app_context = app_context
        layout = QVBoxLayout(self)
        
        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        status_lbl = QLabel("Automatic Conversion is ON")
        layout.addWidget(status_lbl)
        
        layout.addStretch()

