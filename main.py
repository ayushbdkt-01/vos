import os
from user_management import UserManager

if __name__ == "__main__":
    print("Welcome to the Virtual Operating System!")
    print("Initializing modules...")

    # Initialize user manager
    user_manager = UserManager()
    
    # Authentication
    if not user_manager.login(input("Username: "), input("Password: ")):
        print("Access denied!")
        exit()

    # Importing modules
    import process_management
    import memory_management
    import file_management
    import shell
    import logger

    # Initialize system logger
    system_logger = logger.Logger()

    print("Initialization complete. Starting shell...")
    shell.start_shell()