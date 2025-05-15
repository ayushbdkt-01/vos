# shell.py - Windows-compatible version
import sys
from process_management import process_manager
from memory_management import memory_manager
from file_management import file_manager
from ipc import IPC
import logger

# Windows-friendly input handling
try:
    if sys.platform == 'win32':
        from pyreadline3 import Readline
        readline = Readline()
        try:
            readline.parse_and_bind("tab: complete")
            COMMAND_LIST = [
                'create_process', 'terminate_process', 'list_processes',
                'block_process', 'unblock_process',
                'allocate_memory', 'free_memory', 'defragment',
                'create_file', 'delete_file', 'read_file', 'write_file',
                'create_dir', 'list_dir', 'exit', 'help'
            ]
            readline.set_completer(lambda text, state: [cmd for cmd in COMMAND_LIST if cmd.startswith(text)][state])
        except:
            pass
    else:
        import readline
except ImportError:
    readline = None
    print("Note: Advanced input features disabled")

system_logger = logger.Logger()

def start_shell():
    print("Virtual OS Shell Started. Type 'exit' to quit or 'help' for commands.")
    
    while True:
        try:
            command = input("$ ")
            if readline:
                readline.add_history(command)

            if not command.strip():
                continue

            if command == "exit":
                system_logger.log("Shell session ended")
                print("Exiting Virtual OS Shell.")
                break

            elif command == "help":
                print("\nAvailable commands:")
                print("Process Management:")
                print("  create_process <name> [priority] - Create new process")
                print("  terminate_process <pid> - Terminate process")
                print("  list_processes - Show all processes")
                print("  block_process <pid> - Block a running process")
                print("  unblock_process <pid> - Unblock a process\n")
                print("Memory Management:")
                print("  allocate_memory <size> - Allocate memory (MB)")
                print("  free_memory <size> - Free memory (MB)")
                print("  defragment - Show memory fragmentation\n")
                print("File Management:")
                print("  create_file <name> - Create new file")
                print("  delete_file <name> - Delete file")
                print("  read_file <name> - Read file contents")
                print("  write_file <name> <content> - Write to file")
                print("  create_dir <name> - Create directory")
                print("  list_dir [path] - List directory contents\n")
                print("System:")
                print("  exit - Quit the shell")
                print("  help - Show this help\n")

            # Process Management
            elif command.startswith("create_process"):
                parts = command.split()
                if len(parts) < 2:
                    print("Usage: create_process <name> [priority]")
                else:
                    name = parts[1]
                    priority = int(parts[2]) if len(parts) > 2 else 0
                    pid = process_manager.create_process(name, priority)
                    print(f"Process '{name}' created with PID {pid}")

            elif command.startswith("terminate_process"):
                parts = command.split()
                if len(parts) != 2:
                    print("Usage: terminate_process <pid>")
                else:
                    process_manager.terminate_process(int(parts[1]))

            elif command == "list_processes":
                process_manager.list_processes()

            elif command.startswith("block_process"):
                parts = command.split()
                if len(parts) != 2:
                    print("Usage: block_process <pid>")
                else:
                    process_manager.block_process(int(parts[1]))

            elif command.startswith("unblock_process"):
                parts = command.split()
                if len(parts) != 2:
                    print("Usage: unblock_process <pid>")
                else:
                    process_manager.unblock_process(int(parts[1]))

            # Memory Management
            elif command.startswith("allocate_memory"):
                parts = command.split()
                if len(parts) != 2:
                    print("Usage: allocate_memory <size>")
                else:
                    size = int(parts[1])
                    if memory_manager.allocate_memory(size):
                        print(f"Allocated {size}MB memory.")
                    else:
                        print("Memory allocation failed.")

            elif command.startswith("free_memory"):
                parts = command.split()
                if len(parts) != 2:
                    print("Usage: free_memory <size>")
                else:
                    size = int(parts[1])
                    if memory_manager.free_memory(size):
                        print(f"Freed {size}MB memory.")
                    else:
                        print("Memory free failed.")

            elif command == "defragment":
                memory_manager.defragment()

            # File Management
            elif command.startswith("create_file"):
                parts = command.split(" ", 1)
                if len(parts) < 2:
                    print("Usage: create_file <filename>")
                else:
                    filename = parts[1]
                    if file_manager.create_file(filename):
                        print(f"File '{filename}' created successfully.")
                    else:
                        print(f"Failed to create file '{filename}'.")

            elif command.startswith("delete_file"):
                parts = command.split(" ", 1)
                if len(parts) < 2:
                    print("Usage: delete_file <filename>")
                else:
                    filename = parts[1]
                    if file_manager.delete_file(filename):
                        print(f"File '{filename}' deleted.")
                    else:
                        print(f"File '{filename}' not found.")

            elif command.startswith("read_file"):
                parts = command.split(" ", 1)
                if len(parts) < 2:
                    print("Usage: read_file <filename>")
                else:
                    filename = parts[1]
                    content = file_manager.read_file(filename)
                    if content is not None:
                        print("File content:\n" + content)

            elif command.startswith("write_file"):
                parts = command.split(" ", 2)
                if len(parts) < 3:
                    print("Usage: write_file <filename> <content>")
                else:
                    filename = parts[1]
                    content = parts[2]
                    if file_manager.write_file(filename, content):
                        print(f"Written to file '{filename}'.")
                    else:
                        print(f"Failed to write to file '{filename}'.")

            elif command.startswith("create_dir"):
                parts = command.split(" ", 1)
                if len(parts) < 2:
                    print("Usage: create_dir <dirname>")
                else:
                    dirname = parts[1]
                    if file_manager.create_directory(dirname):
                        print(f"Directory '{dirname}' created.")
                    else:
                        print(f"Failed to create directory '{dirname}'.")

            elif command.startswith("list_dir"):
                parts = command.split(" ", 1)
                path = parts[1] if len(parts) > 1 else "."
                contents = file_manager.list_directory(path)
                print(f"Contents of '{path}':")
                for item in contents:
                    print(" -", item)

            else:
                print(f"Command not recognized: {command}. Type 'help' for available commands.")

        except Exception as e:
            print(f"Error: {str(e)}")
            system_logger.log(f"Command failed: {command} - Error: {str(e)}")

if __name__ == "__main__":
    start_shell()
