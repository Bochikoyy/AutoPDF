import sys
import winreg
from pathlib import Path
from app.utils.constants import APP_NAME

def get_executable_path() -> str:
    if getattr(sys, 'frozen', False):
        return sys.executable
    else:
        return f'"{sys.executable}" "{Path(__file__).resolve().parent.parent.parent / "main.py"}"'

def set_startup_registry(enable: bool):
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, 
            r"Software\Microsoft\Windows\CurrentVersion\Run", 
            0, 
            winreg.KEY_SET_VALUE | winreg.KEY_READ
        )
        
        if enable:
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, get_executable_path())
        else:
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass
                
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Failed to set startup registry: {e}")

