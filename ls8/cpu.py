"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.properties = [0] * 8
        self.reg = [0] * 8
        self.pc = 0
        self.ir = None
        self.ram = [0] * 256
        self.can_run = False
        

    def load(self, program_file):
        """Load a program into memory."""

        # address = 0
        # self.can_run = True

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        try:
            address = 0
            self.can_run = True
            with open(program_file, 'r') as f:
                allLines = f.readlines()
                for i in range(0, len(allLines)):
                    line = allLines[i].replace('\n','').strip()
                    if '#' in allLines[i]:
                        line = allLines[i].split('#')[0].strip()
                    if len(line) > 0:
                        self.ram[address] = int(line, 2)
                        address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
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
    
    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self,address, value):
        self.ram[address] = value
        return self.ram[address]
        
        

    def run(self):
        """Run the CPU."""

        while self.can_run:
            #get instruction from ram
            ram_read_ins = self.ram_read(self.pc)
            # result = self.ram_write(self.ir, ram_read_ins)
            self.ir = ram_read_ins
            if ram_read_ins == 0b00000001:
                self.can_run = False
                exit()
            format_ram_read_ins = '{0:8b}'.format(ram_read_ins)
            num_op = int(format_ram_read_ins[:2].strip() or '00',2)
            alu_op = int(format_ram_read_ins[2].strip() or '0',2)
            inst_set = int(format_ram_read_ins[3].strip() or '0',2)
            inst_iden = int(format_ram_read_ins[4:].strip() or '0000',2)

            if alu_op == int('1', 2):
                self.alu('MUL', self.ram_read(self.pc+1), self.ram_read(self.pc+2))


                # print(output)
                self.pc += int(num_op) + 1
            else:
                if ram_read_ins == 0b10000010:
                    key = int(self.ram_read(self.pc+1))
                    value = self.ram_read(self.pc+2)
                    self.reg[key] = value
                    self.pc += int(num_op) + 1
                elif ram_read_ins == 0b01000111:
                    key = int(self.ram_read(self.pc+1))
                    print(int(self.reg[key]))
                    self.pc += int(num_op) + 1
                     
            # if inst_set is not int('1', 2):
            #     self.pc += int(num_op)





            #DECODE operation
            
            #EXECUTE op.

