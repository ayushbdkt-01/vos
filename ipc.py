import logger

system_logger = logger.Logger()

class IPC:
    def __init__(self):
        self.messages = {}  # {receiver_pid: [(sender_pid, message)]}
        self.shared_memory = {}  # {key: value}

    def send(self, sender_pid, receiver_pid, message):
        if receiver_pid not in self.messages:
            self.messages[receiver_pid] = []
        self.messages[receiver_pid].append((sender_pid, message))
        system_logger.log(f"Message sent from {sender_pid} to {receiver_pid}")

    def receive(self, receiver_pid):
        messages = self.messages.get(receiver_pid, [])
        if messages:
            self.messages[receiver_pid] = []
            system_logger.log(f"Messages retrieved for {receiver_pid}")
        return messages

    def shared_memory_write(self, key, value):
        self.shared_memory[key] = value
        system_logger.log(f"Shared memory updated: {key}")

    def shared_memory_read(self, key):
        return self.shared_memory.get(key)

    def shared_memory_list(self):
        return list(self.shared_memory.keys())