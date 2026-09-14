from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class FoldersView(QWidget):
    def __init__(self, app_context):
        super().__init__()
        self.app_context = app_context
        layout = QVBoxLayout(self)
        
        title = QLabel("Monitored Folders")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        layout.addStretch()

