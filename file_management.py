# file_management.py
import os
from cryptography.fernet import Fernet

























class FileManager:
    def __init__(self, base_dir='data', logger=None):
        # Convert to absolute path and normalize
        self.base_dir = os.path.normpath(os.path.abspath(base_dir))
        self.logger = logger
        os.makedirs(self.base_dir, exist_ok=True)
        
        # Debug output - will appear in terminal
        print(f"FILE MANAGER INITIALIZED\n"
              f"Storage directory: {self.base_dir}\n"
              f"Directory exists: {os.path.exists(self.base_dir)}\n"
              f"Write test file...")
              
        # Test file creation during init
        test_file = os.path.join(self.base_dir, "__testfile__.tmp")
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            print("SUCCESS: Test file created/deleted successfully")
        except Exception as e:
            print(f"CRITICAL ERROR: Cannot write to {self.base_dir}\n{str(e)}")

        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def get_full_path(self, path):
        return os.path.join(self.base_dir, path)

    def create_file(self, filename):
        filepath = self.get_full_path(filename)
        try:
            # Double-check directory exists
            os.makedirs(self.base_dir, exist_ok=True)
            
            # Verify we can write
            with open(filepath, 'w') as f:
                f.write("")  # Create empty file
                
            msg = f"File created: {filepath}"
            if self.logger:
                self.logger.log(msg)
            print(msg)  # Terminal confirmation
            return True
        except Exception as e:
            msg = f"Failed to create {filepath}\nError: {str(e)}"
            if self.logger:
                self.logger.log(msg)
            print(msg)
            return False


    def delete_file(self, filename):
        filepath = self.get_full_path(filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            msg = f"File deleted: {filename}"
            if self.logger:
                self.logger.log(msg)
            print(msg)
            return True
        else:
            msg = f"Error: File '{filename}' not found."
            if self.logger:
                self.logger.log(msg)
            print(msg)
            return False

    def read_file(self, filename):
        filepath = self.get_full_path(filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                    # Try to decrypt if encrypted
                    try:
                        content = self.cipher.decrypt(content.encode()).decode()
                    except:
                        pass  # Not encrypted or wrong key
                    msg = f"File read: {filename}"
                    if self.logger:
                        self.logger.log(msg)
                    print(content)
                    return content
            except Exception as e:
                msg = f"Error reading file: {str(e)}"
                if self.logger:
                    self.logger.log(msg)
                print(msg)
                return None
        else:
            msg = f"Error: File '{filename}' not found."
            if self.logger:
                self.logger.log(msg)
            print(msg)
            return None

    def write_file(self, filename, content, encrypt=False):
        filepath = self.get_full_path(filename)
        try:
            data = self.cipher.encrypt(content.encode()) if encrypt else content
            with open(filepath, 'w') as f:
                f.write(data if isinstance(data, str) else data.decode())
            msg = f"File written: {filename} (encrypted: {encrypt})"
            if self.logger:
                self.logger.log(msg)
            print(msg)
            return True
        except Exception as e:
            msg = f"Error writing file: {str(e)}"
            if self.logger:
                self.logger.log(msg)
            print(msg)
            return False

    def create_directory(self, dirname):
        dirpath = self.get_full_path(dirname)
        try:
            os.makedirs(dirpath, exist_ok=True)
            msg = f"Directory created: {dirname}"
            if self.logger:
                self.logger.log(msg)
            print(msg)
            return True
        except Exception as e:
            msg = f"Error creating directory: {str(e)}"
            if self.logger:
                self.logger.log(msg)
            print(msg)
            return False

    def list_directory(self, path="."):
        dirpath = self.get_full_path(path)
        try:
            contents = os.listdir(dirpath)
            msg = f"Directory listed: {path}"
            if self.logger:
                self.logger.log(msg)
            return contents
        except Exception as e:
            msg = f"Error listing directory: {str(e)}"
            if self.logger:
                self.logger.log(msg)
            print(msg)
            return []

# Default instance without logger for backward compatibility
file_manager = FileManager()