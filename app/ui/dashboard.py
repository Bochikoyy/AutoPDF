from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class DashboardView(QWidget):
    def __init__(self, app_context):
        super().__init__()
        self.app_context = app_context
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        
        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)
        
        watcher = self.app_context.get('watcher')
        is_on = True
        if watcher:
            is_on = watcher.event_handler.is_active
            
        self.status_lbl = QLabel(f"Automatic Conversion is {'ON' if is_on else 'OFF'}")
        self.status_lbl.setStyleSheet(f"font-size: 16px; color: {'green' if is_on else 'red'};")
        layout.addWidget(self.status_lbl)
        
        self.toggle_btn = QPushButton("Turn OFF" if is_on else "Turn ON")
        self.toggle_btn.setFixedSize(150, 40)
        self.toggle_btn.clicked.connect(self.toggle_status)
        layout.addWidget(self.toggle_btn)
        
        layout.addStretch()

    def toggle_status(self):
        watcher = self.app_context.get('watcher')
        settings = self.app_context.get('settings')
        if not watcher:
            return
            
        current_status = watcher.event_handler.is_active
        new_status = not current_status
        watcher.set_active(new_status)
        
        if settings:
            settings.set("is_active", new_status)
        
        if new_status:
            self.status_lbl.setText("Automatic Conversion is ON")
            self.status_lbl.setStyleSheet("font-size: 16px; color: green;")
            self.toggle_btn.setText("Turn OFF")
        else:
            self.status_lbl.setText("Automatic Conversion is OFF")
            self.status_lbl.setStyleSheet("font-size: 16px; color: red;")
            self.toggle_btn.setText("Turn ON")


