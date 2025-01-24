#CPU Simulator

class CPU:
    def __init__(self):
    self.register = [0]*32 # 32 registers
    self.pc = 0 #program counter

    def execute(self, instruction):
        pass

class Cache:
    def __init__(self, size):
        self.cache {}
        self.size = size
        self.enabled = False

    def toggle(self, code):
        if code == 0:
            self.enabled = False
        elif code == 1:
            self.enabled = True
        elif code == 2:
            self.cache.clear()

class MemoryBus:
    def __init__(self):
        self.memory = {}

    def read(self, address):
        return self.memory.get(address, 0)
    
    def write(self, address, value):
        self.memory[address] = value
