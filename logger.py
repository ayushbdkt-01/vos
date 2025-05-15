# logger.py
import datetime
import os

class Logger:
    def __init__(self, log_file="system.log"):
        self.log_dir = "logs"
        self.log_file = log_file
        os.makedirs(self.log_dir, exist_ok=True)
        self.full_path = os.path.join(self.log_dir, log_file)
        if not os.path.exists(self.full_path):
            open(self.full_path, 'w').close()

    def log(self, event):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.full_path, 'a') as f:
            f.write(f"[{timestamp}] {event}\n")

# Global logger instance
system_logger = Logger()