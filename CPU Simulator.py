#CPU Simulator

class CPU:
    def __init__(self):
        self.register = [0]*32 # 32 registers
        self.pc = 0 #program counter

    def add(self, rd, rs, rt):
        self.register[rd] = self.register[rs] + self.register[rt]
     
    def lw(self, rt, offset, rs, memory):
        address = self.register[rs] + offset
        self.registers[rt] = memory.read(address)
    
    def bne(self, rs, rt, offset):
        if self.register[rs] != self.register[rt]:
            self.pc += offset*4
    def fetch_instruction(self, instructions):
        instruction = instructions[self.pc]
        print("Fetched instruction: {instruction}")
        return instruction
    
    def decode_instruction(instruction):

        parts = instruction.split()
        operation = parts[0]
        operands = parts[1:]
        print(f"Decoded: Operation:{operation}, Operands:{operands}")
        return operation, operands

    def execute(self, instruction, cache, memory):
        operation, operands = instruction
        if operation == "ADD":
            self.add(rd, rs, rt)
            print(f"ADD executed: R{rd} = R{rs} + R{rt} -> {self.register[rd]}")
        elif operation == "LW":
            rt, offset_rs = operands
            offset, rs = parse_offset_rs(offset_rs)
            self.lw(int(rt), int(offset), int(rs), memory)
            print(f"LW executed: R{rt} <- Memory[{self.registers[rs]} + {offset}] -> {self.registers[int(rt)]}")

def read_from_cache(self, address):
    if not self.enabled:
        print(f"Cache disabled. Accessing memory at address {address}.")
        return None
    if address in self.cache:
        print(f"Cache hit for address {address}. Value: {self.cache[address]}")
        return self.cache[address]
    else:
        print(f"Cache miss for address {address}.")
        return None

class Cache:
    def __init__(self, size):
        self.cache: {}
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

def parse_instructions(file_path):
    instructions = []
    with open(file_path, 'r') as file:
        for line in file:
            instructions.append(line.strip())
    return instructions

def initialize_memory(file_path):
    memory = {}
    with open(file_path, 'r') as file:
        for line in file:
            address, value = line.split(':')
            memory[int(address.strip())] = int(value.strip())
    return memory

def simulate(cpu, cache, memory, instructions):
    while cpu.pc < len(instructions):
        instruction = instructions[cpu.pc]
        print(f"Fetching instruction at PC: {cpu.pc*4} -> {instruction}")

        decoded_instruction = decode_instruction(instruction)
        print(f"Decoded instruction: {decoded_instruction}")

        result = cpu.execute(decoded_instruction, cache, memory)
        print(f"Result: {result}")

        if "CACHE" in instruction:
            print(f"Cache Status: Enabled = {cache.enabled}, Entries={len(cache.cache)}")
        
        print(f"PC updated to {cpu.pc*4}")
        cpu.pc += 1
