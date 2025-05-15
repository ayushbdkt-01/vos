import logger

system_logger = logger.Logger()

class Page:
    def __init__(self, page_id, size):
        self.page_id = page_id
        self.size = size
        self.allocated = False
        self.data = None
        self.last_accessed = 0  # For LRU

    def __str__(self):
        status = "Allocated" if self.allocated else "Free"
        return f"Page ID: {self.page_id}, Size: {self.size}MB, Status: {status}"

class MemoryManager:
    def __init__(self, total_memory=1024, page_size=128):
        self.total_memory = total_memory
        self.page_size = page_size
        self.pages = [Page(i, page_size) for i in range(total_memory // page_size)]
        self.disk = {}  # Simulate disk storage
        self.page_table = {}  # Virtual to physical mapping
        self.lru_cache = []
        self.access_counter = 0

    def allocate_memory(self, size):
        pages_needed = (size + self.page_size - 1) // self.page_size
        free_pages = [page for page in self.pages if not page.allocated]

        if len(free_pages) >= pages_needed:
            for i in range(pages_needed):
                free_pages[i].allocated = True
                free_pages[i].last_accessed = self.access_counter
                self.access_counter += 1
                self.lru_cache.append(free_pages[i].page_id)
            system_logger.log(f"Allocated {size}MB using {pages_needed} pages")
            return True
        else:
            print("Memory allocation failed. Not enough free pages available.")
            return False

    def free_memory(self, size):
        pages_to_free = (size + self.page_size - 1) // self.page_size
        allocated_pages = [page for page in self.pages if page.allocated]

        if len(allocated_pages) >= pages_to_free:
            for i in range(pages_to_free):
                allocated_pages[i].allocated = False
                if allocated_pages[i].page_id in self.lru_cache:
                    self.lru_cache.remove(allocated_pages[i].page_id)
            system_logger.log(f"Freed {size}MB using {pages_to_free} pages")
            return True
        else:
            print("Error: Cannot free more memory than allocated.")
            return False

    def handle_page_fault(self, page_id):
        if page_id in self.disk:
            # Find a page to replace using LRU
            if len(self.lru_cache) >= len(self.pages):
                oldest = self.lru_cache.pop(0)
                oldest_page = next(p for p in self.pages if p.page_id == oldest)
                self.disk[oldest] = oldest_page.data  # Swap out
                oldest_page.data = self.disk[page_id]  # Swap in
                oldest_page.last_accessed = self.access_counter
                self.access_counter += 1
                self.lru_cache.append(page_id)
                system_logger.log(f"Page fault handled for page {page_id}")
                return True
        return False

    def defragment(self):
        free_pages = [p for p in self.pages if not p.allocated]
        contiguous_free = 0
        max_contiguous = 0
        current_block = 0
        
        for page in self.pages:
            if not page.allocated:
                current_block += 1
                contiguous_free += self.page_size
            else:
                max_contiguous = max(max_contiguous, current_block)
                current_block = 0
                
        max_contiguous = max(max_contiguous, current_block)
        print(f"Contiguous free memory: {contiguous_free}MB")
        print(f"Largest contiguous block: {max_contiguous * self.page_size}MB")
        system_logger.log("Memory defragmentation analysis completed")

    def display_memory(self):
        print("Memory Status:")
        for page in self.pages:
            print(page)

memory_manager = MemoryManager()