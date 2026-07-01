from datetime import datetime

class Logger:
    def __init__(self, callback):
        self.callback = callback

    def log(self, level, msg):
        time = datetime.now().strftime("%H:%M:%S")
        self.callback(f"[{time}] [{level}] {msg}")