

from CPU_Simulator import CPU, Cache, MemoryBus, simulate

def main():
    instructions = [
        "ADD 1 2 3",       # R1 = R2 + R3
        "ADDI 4 1 10",     # R4 = R1 + 10
        "SUB 5 4 3",       # R5 = R4 - R3
        "SLT 6 2 3",       # R6 = (R2 < R3) ? 1 : 0
        "BNE 2 3 2",       # if R2 != R3, PC = PC + 4 + 2*4
        "J 8",             # PC = 8 * 4
        "JAL 12",          # R7 = PC + 4, PC = 12 * 4
        "LW 9 4(2)",       # R9 = MEM[R2 + 4]
        "SW 10 8(3)",      # MEM[R3 + 8] = R10
        "CACHE 1",         # Enable cache
        "CACHE 2",         # Flush cache
        "HALT"             # Terminate execution
    ]

    memory_content = {
        0: 5,
        4: 10,
        8: 15,
        12: 20
    }

    cpu = CPU()
    cache = Cache(size=4)
    memory = MemoryBus()
    memory.memory = memory_content

    simulate(cpu, cache, memory, instructions)

if __name__ == "__main__":
    main()