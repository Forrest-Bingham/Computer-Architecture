"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #pass
        #8 registers
        self.reg = [0] * 8
        #255 storage for ram
        self.ram = [0] * 256
        self.pc = 0

    def ram_read(self, MAR):

        return self.ram[MAR]
    
    def ram_write(self, MDR, MAR):

        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [0] * 256
        # [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
            
        # ]

        with open(sys.argv[1]) as f:
            for line in f:
                string_val = line.split("#")[0].strip()
                if string_val == '':
                    continue
                v = int(string_val, 2)
        #print(v)
                self.ram[address] = v
                address += 1

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] * self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        #pass
        # Look up bits for HLT, LDI, PRN, set running = true
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        running = True

        #while running!:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8 <-- Save Reg_a in R0
        #     0b00000000, # reg_a
        #     0b00001000, # The value 8 == reg_b
        #     0b01000111, # PRN R0
        #     0b00000000, # reg_a
        #     0b00000001, # HLT
        # ]

        while running == True:
            instruction = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)

            if instruction == HLT:
                print("***** HALT COMMAND INITIATED ******")
                running = False
                self.pc += 1
                sys.exit()

            elif instruction == LDI:
                print("******** LDI COMMAND INITIATED *******")
                print(self.reg, "--- self.reg")
                print(reg_a, "--- reg_a")
                print(reg_b, "--- reg_b")
                print(self.reg[reg_a], "--- Before")
                #Set reg_a = to reg_b
                self.reg[reg_a] = reg_b
                print(self.reg[reg_a], "--- After")
                self.pc += 3

                print(self.reg, "--- self.reg")

            elif instruction == PRN:
                print("******* PRINT COMMAND INITIATED *********")
                print(self.pc, "--- self.pc")
                print(self.reg, "--- self.reg")
                print(reg_a, "--- reg_a")
                print(self.reg[reg_a])
                self.pc += 2

            elif instruction == MUL:
                print("******** MULTIPLY COMMAND INITIATED ********")
                print(self.reg, " --- self.reg")
                print(self.reg[reg_a], " -- reg_a")
                print(self.reg[reg_b], " -- reg_b")
                mul = self.reg[reg_a] * self.reg[reg_b]
                print(mul)
                self.pc += 3

            else: 
                print(f'unknown instruction {instruction} at address {pc}')
                running = False
                sys.exit()
		        