#CPU Simulator

class CPU:
    def __init__(self):
        self.register = [0]*32 # 32 registers
        self.pc = 0 #program counter

    def add(self, rd, rs, rt):
        self.register[rd] = self.register[rs] + self.register[rt]
    
    def addi(self, rt, rs, immd):
        self.register[rt] = self.register[rs] + immd

    def sub(self, rd, rs, rt):
        self.register[rd] = self.register[rs] - self.register[rt]

    def slt(self, rd, rs, rt):
        self.register[rd] = 1 if self.register[rs] < self.register[rt] else 0

    def bne(self, rs, rt, offset):
        if self.register[rs] != self.register[rt]:
            self.pc += offset * 4

    def j(self, target):
        self.pc = target * 4

    def jal(self, target):
        self.register[7] = self.pc + 4
        self.pc = target * 4

    def lw(self, rt, offset, rs, memory):
        address = self.register[rs] + offset
        self.register[rt] = memory.read(address)

    def sw(self, rt, offset, rs, memory):
        address = self.register[rs] + offset
        memory.write(address, self.register[rt])

    def fetch_instruction(self, instructions):
        instruction = instructions[self.pc // 4]
        print(f"Fetched instruction: {instruction}")
        return instruction
    
    def decode_instruction(self, instruction):
        parts = instruction.split()
        operation = parts[0]
        operands = parts[1:]
        print(f"Decoded: Operation: {operation}, Operands: {operands}")
        return operation, operands

    def execute(self, instruction, cache, memory):
        operation, operands = instruction
        if operation == "ADD":
            rd, rs, rt = map(int, operands)
            self.add(rd, rs, rt)
            print(f"ADD executed: R{rd} = R{rs} + R{rt} -> {self.register[rd]}")
        elif operation == "ADDI":
            rt, rs, immd = operands
            self.addi(int(rt), int(rs), int(immd))
            print(f"ADDI executed: R{rt} = R{rs} + {immd} -> {self.register[int(rt)]}")
        elif operation == "SUB":
            rd, rs, rt = map(int, operands)
            self.sub(rd, rs, rt)
            print(f"SUB executed: R{rd} = R{rs} - R{rt} -> {self.register[rd]}")
        elif operation == "SLT":
            rd, rs, rt = map(int, operands)
            self.slt(rd, rs, rt)
            print(f"SLT executed: R{rd} = (R{rs} < R{rt}) -> {self.register[rd]}")
        elif operation == "BNE":
            rs, rt, offset = map(int, operands)
            self.bne(rs, rt, offset)
            print(f"BNE executed: if R{rs} != R{rt} -> PC = {self.pc}")
        elif operation == "J":
            target = int(operands[0])
            self.j(target)
            print(f"J executed: PC = {self.pc}")
        elif operation == "JAL":
            target = int(operands[0])
            self.jal(target)
            print(f"JAL executed: R7 = {self.register[7]}, PC = {self.pc}")
        elif operation == "LW":
            rt, offset_rs = operands
            offset, rs = map(int, offset_rs.strip('()').split('('))
            self.lw(int(rt), offset, rs, memory)
            print(f"LW executed: R{rt} <- Memory[{self.register[rs]} + {offset}] -> {self.register[int(rt)]}")
        elif operation == "SW":
            rt, offset_rs = operands
            offset, rs = map(int, offset_rs.strip('()').split('('))
            self.sw(int(rt), offset, rs, memory)
            print(f"SW executed: Memory[{self.register[rs]} + {offset}] <- R{rt} -> {memory.read(self.register[rs] + offset)}")
        elif operation == "CACHE":
            code = int(operands[0])
            cache.toggle(code)
            print(f"CACHE executed: Code = {code}, Cache Enabled = {cache.enabled}")
        elif operation == "HALT":
            print("HALT executed: Terminating execution")
            return "HALT"

class Cache:
    def __init__(self, size):
        self.cache = {}
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
    while cpu.pc < len(instructions) * 4:
        instruction = cpu.fetch_instruction(instructions)
        decoded_instruction = cpu.decode_instruction(instruction)
        result = cpu.execute(decoded_instruction, cache, memory)
        if result == "HALT":
            break
        cpu.pc += 4
