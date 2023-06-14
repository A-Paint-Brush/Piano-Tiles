import time


class timer:
    def __init__(self):
        self.initialized = False
        self.start_time = 0

    def is_initialized(self):
        return self.initialized

    def reset(self):
        if not self.initialized:
            self.initialized = True
        self.start_time = time.time()

    def get_time(self):
        return time.time() - self.start_time
