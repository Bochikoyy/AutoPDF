from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class AboutView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        title = QLabel("About AutoPDF")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        desc = QLabel("AutoPDF automatically converts your downloaded files to PDF.")
        layout.addWidget(desc)
        
        layout.addStretch()

