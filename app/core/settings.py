import json
from pathlib import Path
from app.utils.paths import get_data_dir

class SettingsManager:
    def __init__(self):
        self.settings_file = get_data_dir() / "settings.json"
        self.settings = self._load()
        
    def _load(self):
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
        
    def _save(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f)
            
    def get(self, key, default=None):
        return self.settings.get(key, default)
        
    def set(self, key, value):
        self.settings[key] = value
        self._save()

