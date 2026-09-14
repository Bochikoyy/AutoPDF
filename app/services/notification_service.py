from winotify import Notification
from app.utils.constants import APP_NAME

def show_notification(title: str, msg: str, duration: str = "short"):
    try:
        toast = Notification(
            app_id=APP_NAME,
            title=title,
            msg=msg,
            duration=duration
        )
        toast.show()
    except Exception as e:
        pass # Optional logging

