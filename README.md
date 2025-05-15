# 🖥️ Virtual Operating System (VOS)

The **Virtual Operating System (VOS)** is a Python-based simulation of core operating system functionalities. It includes **process management**, **memory allocation**, **file operations**, and **user authentication** through both a **Command-Line Shell** and a **Streamlit GUI Dashboard**.

---

## 📌 Project Overview

This project is intended to help Computer Science students and enthusiasts understand the internal workings of an OS by simulating:

- 👥 Multi-user login system  
- 🧠 Process creation, blocking/unblocking, and scheduling (by priority)  
- 💾 Virtual memory management with paging and defragmentation  
- 📁 File management (create, read, write, delete, directory ops)  
- 🖥️ Command-line shell interface (like a terminal)  
- 🌐 GUI interface via Streamlit for a visual experience  

> ⚠️ This is a simulated OS; it does **not interact** with actual system-level processes or memory.

---

## 📂 Project Structure

```
virtual_operating_system/
├── app.py                # Streamlit-based GUI app
├── main.py               # CLI shell-based OS controller
├── shell.py              # Terminal-like command handler
├── process_management.py # Process scheduling logic
├── memory_management.py  # Paging and memory management
├── file_management.py    # File & directory system
├── user_management.py    # Login and user handling
├── logger.py             # Logs system activities
├── ipc.py                # Inter-process communication (planned)
├── data/                 # All created files and folders stored here
├── logs/                 # Log files for auditing
└── README.md             # Project documentation
```

---

## ⚙️ Required Dependencies

Install these before running the project:

```bash
pip install streamlit cryptography pyreadline3
```

> `pyreadline3` is required only on **Windows** to enable shell autocompletion and history.

---

## 🚀 Setup & Installation

1. **Clone the Repository:**

```bash
git clone https://github.com/your-username/virtual-operating-system.git
cd virtual-operating-system
```

2. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

(Or install manually using the dependencies listed above)

---

## 👤 Default Users

| Username | Password     | Description      |
|----------|--------------|------------------|
| admin    | admin123     | Administrator    |
| user     | password123  | Regular user     |

---

## 🖥️ How to Use

### 🔧 Option 1: Command-Line Shell

```bash
python main.py
```

🔑 Login using username and password.  
Then use commands like:

```bash
create_process Calculator 2
allocate_memory 128
create_file notes.txt
write_file notes.txt Hello_World
read_file notes.txt
```

### 🌐 Option 2: GUI via Streamlit

```bash
streamlit run app.py
```

🔐 Log in via the browser interface  
🧠 Interact with OS components via the tabbed dashboard:
- Process Management
- Memory Management
- File Management
- System Controls

---

## 💻 Supported Shell Commands

| Category           | Command Example                        | Description                             |
|-------------------|-----------------------------------------|-----------------------------------------|
| Process Mgmt       | `create_process Editor 1`               | Create a process with priority          |
|                   | `terminate_process 1`                   | Terminate process with PID 1            |
|                   | `list_processes`                        | Show all processes                      |
|                   | `block_process 1`                       | Block process with PID 1                |
|                   | `unblock_process 1`                     | Unblock process with PID 1              |
| Memory Mgmt        | `allocate_memory 256`                  | Allocate 256MB memory                   |
|                   | `free_memory 128`                       | Free 128MB memory                       |
|                   | `defragment`                            | Show memory fragmentation               |
| File Mgmt          | `create_file report.txt`               | Create a new file                       |
|                   | `write_file report.txt Hello`           | Write content to file                   |
|                   | `read_file report.txt`                  | Read file content                       |
|                   | `delete_file report.txt`                | Delete a file                           |
|                   | `create_dir projects`                   | Create a new directory                  |
|                   | `list_dir` or `list_dir projects`       | List contents of directory              |
| System             | `help`                                 | Show all commands                       |
|                   | `exit`                                  | Exit the shell                          |

---

## 📌 Features Implemented

- ✅ User login system with hashed passwords  
- ✅ Process management with priority scheduling  
- ✅ Virtual memory with page allocation & LRU  
- ✅ File and directory operations with optional encryption  
- ✅ Logging of all operations (stored in `/logs`)  
- ✅ GUI Dashboard via Streamlit  
- ✅ Command-based CLI interface  

---

## 🚧 Future Improvements

- 🔁 Inter-process communication (IPC) between processes  
- 🔐 Toggle encryption from UI  
- 📊 Real-time visualization of memory and process queues  
- 💾 Persistent user and process data via database  

---

## 🙋‍♂️ Author

**Ayush**  
B.Tech Computer Science | India 🇮🇳  
Currently exploring Operating Systems, Backend Development, and Machine Learning.

---

## 📄 License

This project is licensed under the **MIT License**. Feel free to use and modify for educational purposes.

---

## 📬 Feedback / Contributions

Have ideas, suggestions, or want to contribute? Open an issue or submit a pull request on GitHub.
