import streamlit as st
import os
from process_management import process_manager
from memory_management import memory_manager
from file_management import FileManager  # Only import the class
from user_management import UserManager
import logger

def initialize_components():
    # Initialize logger first
    system_logger = logger.Logger()
    
    # Initialize FileManager with absolute path and debug info
    file_manager = FileManager(logger=system_logger)
    print(f"DEBUG: File storage location - {file_manager.base_dir}")  # Terminal confirmation
    
    # Initialize other components
    user_manager = UserManager(logger=system_logger)
    
    return system_logger, file_manager, user_manager

system_logger, file_manager, user_manager = initialize_components()

def show_login():
    st.title("Virtual OS Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if user_manager.login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid credentials")

def show_dashboard():
    st.title(f"Virtual OS Dashboard - Welcome {st.session_state.username}")
    
    tabs = st.tabs(["Process Management", "Memory Management", "File Management", "System"])
    
    # Process Management Tab (unchanged)
    with tabs[0]:
        st.header("Process Management")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Create Process")
            proc_name = st.text_input("Process Name", key="proc_name")
            proc_priority = st.selectbox("Priority", [0, 1, 2], 
                                      format_func=lambda x: ["Low", "Normal", "High"][x],
                                      key="proc_priority")
            if st.button("Create Process"):
                pid = process_manager.create_process(proc_name, proc_priority)
                st.success(f"Process created with PID: {pid}")
                
        with col2:
            st.subheader("Process Actions")
            pid = st.number_input("PID", min_value=1, step=1, key="proc_pid")
            action = st.selectbox("Action", ["Terminate", "Block", "Unblock"], key="proc_action")
            if st.button("Execute Action"):
                if action == "Terminate":
                    process_manager.terminate_process(pid)
                    st.success(f"Process {pid} terminated")
                elif action == "Block":
                    process_manager.block_process(pid)
                    st.success(f"Process {pid} blocked")
                elif action == "Unblock":
                    process_manager.unblock_process(pid)
                    st.success(f"Process {pid} unblocked")
    
    # Memory Management Tab (unchanged)
    with tabs[1]:
        st.header("Memory Management")
        size = st.number_input("Memory Size (MB)", min_value=1, max_value=1024, value=128)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Allocate Memory"):
                if memory_manager.allocate_memory(size):
                    st.success(f"Allocated {size}MB")
                else:
                    st.error("Allocation failed")
        
        with col2:
            if st.button("Free Memory"):
                if memory_manager.free_memory(size):
                    st.success(f"Freed {size}MB")
                else:
                    st.error("Free failed")
        
        if st.button("Defragment Memory"):
            memory_manager.defragment()
    
    # File Management Tab (updated with debug info)
    with tabs[2]:
        st.header("File Management")
        
        # Debug information
        with st.expander("ℹ️ Storage Location"):
            st.code(f"Files are stored at:\n{file_manager.base_dir}")
            st.write(f"Directory exists: {os.path.exists(file_manager.base_dir)}")
            if st.button("Refresh Directory Contents"):
                st.rerun()
        
        action = st.selectbox("Select Action", 
            ["Create File", "Delete File", "Read File", "Write File", 
             "Create Directory", "List Directory"], key="file_action")
        
        if action in ["Create File", "Delete File", "Read File", "Write File"]:
            filename = st.text_input("File Name", key="filename")
            
            if action == "Write File":
                content = st.text_area("Content", key="file_content")
                if st.button("Write"):
                    if file_manager.write_file(filename, content):
                        st.success(f"File written to:\n{os.path.join(file_manager.base_dir, filename)}")
                    else:
                        st.error("Operation failed (check terminal for details)")
            
            elif action == "Read File":
                if st.button("Read"):
                    content = file_manager.read_file(filename)
                    if content is not None:
                        st.text_area("File Content", value=content, key="file_output")
            
            elif action in ["Create File", "Delete File"]:
                if st.button(action):
                    if action == "Create File":
                        success = file_manager.create_file(filename)
                        if success:
                            st.success(f"File created at:\n{os.path.join(file_manager.base_dir, filename)}")
                    else:
                        success = file_manager.delete_file(filename)
                    if not success:
                        st.error("Operation failed (check terminal for details)")
        
        elif action == "Create Directory":
            dirname = st.text_input("Directory Name", key="dirname")
            if st.button("Create Directory"):
                if file_manager.create_directory(dirname):
                    st.success(f"Directory created at:\n{os.path.join(file_manager.base_dir, dirname)}")
                else:
                    st.error("Operation failed (check terminal for details)")
        
        elif action == "List Directory":
            dirname = st.text_input("Directory Path", ".", key="list_dir")
            if st.button("List"):
                contents = file_manager.list_directory(dirname)
                if contents is not None:
                    st.write(f"Contents of {os.path.join(file_manager.base_dir, dirname)}:")
                    st.write(contents)
                else:
                    st.error("Failed to list directory")
    
    # System Tab (unchanged)
    with tabs[3]:
        st.header("System Information")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        show_login()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()