import logger

system_logger = logger.Logger()

class Process:
    def __init__(self, pid, name, priority=0, state="Ready", parent_pid=None):
        self.pid = pid
        self.name = name
        self.priority = priority
        self.state = state
        self.parent_pid = parent_pid

    def __str__(self):
        return f"PID: {self.pid}, Name: {self.name}, Priority: {self.priority}, State: {self.state}"

class ProcessManager:
    def __init__(self):
        self.process_list = []
        self.ready_queue = []
        self.blocked_queue = []
        self.running_process = None
        self.pid_counter = 1

    def create_process(self, process_name, priority=0, parent_pid=None):
        process = Process(self.pid_counter, process_name, priority, "Ready", parent_pid)
        self.process_list.append(process)
        self.ready_queue.append(process)
        system_logger.log(f"Process created: {process}")
        self.pid_counter += 1
        self.schedule_process()
        return process.pid

    def terminate_process(self, pid):
        for process in self.process_list:
            if process.pid == pid:
                self.process_list.remove(process)
                if process in self.ready_queue:
                    self.ready_queue.remove(process)
                if process in self.blocked_queue:
                    self.blocked_queue.remove(process)
                if self.running_process == process:
                    self.running_process = None
                    system_logger.log(f"Running process terminated: {process}")
                    self.schedule_process()
                else:
                    system_logger.log(f"Process terminated: {process}")
                return
        print(f"Process with PID {pid} not found.")

    def block_process(self, pid):
        for process in self.process_list:
            if process.pid == pid and process.state == "Running":
                process.state = "Blocked"
                self.blocked_queue.append(process)
                self.running_process = None
                system_logger.log(f"Process blocked: {process}")
                self.schedule_process()
                return
        print(f"Process with PID {pid} not running or not found.")

    def unblock_process(self, pid):
        for process in self.blocked_queue:
            if process.pid == pid:
                process.state = "Ready"
                self.blocked_queue.remove(process)
                self.ready_queue.append(process)
                system_logger.log(f"Process unblocked: {process}")
                self.schedule_process()
                return
        print(f"Process with PID {pid} not blocked or not found.")

    def list_processes(self):
        if not self.process_list:
            print("No active processes.")
        else:
            print("Running Process:")
            if self.running_process:
                print(f"  {self.running_process}")
            else:
                print("  None")
                
            print("\nReady Queue:")
            for process in self.ready_queue:
                print(f"  {process}")
                
            print("\nBlocked Queue:")
            for process in self.blocked_queue:
                print(f"  {process}")

    def schedule_process(self):
        if not self.running_process and self.ready_queue:
            # Sort by priority (higher first)
            self.ready_queue.sort(key=lambda p: p.priority, reverse=True)
            self.running_process = self.ready_queue.pop(0)
            self.running_process.state = "Running"
            system_logger.log(f"Process scheduled: {self.running_process}")

process_manager = ProcessManager()