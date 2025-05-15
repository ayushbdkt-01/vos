# user_management.py
import hashlib
import logger

class UserManager:
    def __init__(self, logger=None):  # Make logger optional
        self.users = {
            "admin": self._hash_password("admin123"),
            "user": self._hash_password("password123")
        }
        self.current_user = None
        self.logger = logger

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username, password):
        if username in self.users:
            if self.users[username] == self._hash_password(password):
                self.current_user = username
                if self.logger:
                    self.logger.log(f"User logged in: {username}")
                return True
        if self.logger:
            self.logger.log(f"Failed login attempt for: {username}")
        return False

    def create_user(self, username, password):
        if username not in self.users:
            self.users[username] = self._hash_password(password)
            if self.logger:
                self.logger.log(f"User created: {username}")
            return True
        return False

    def change_password(self, username, old_password, new_password):
        if self.login(username, old_password):
            self.users[username] = self._hash_password(new_password)
            if self.logger:
                self.logger.log(f"Password changed for: {username}")
            return True
        return False

# Default instance without logger for backward compatibility
user_manager = UserManager()