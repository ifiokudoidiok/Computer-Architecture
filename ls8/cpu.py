"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101 
POP = 0b01000110 
CALL = 0b01010000
RET  = 0b00010001
ADD = 0b10100000

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
        self.branchtable = {
            ADD: self.add,
            LDI: self.ldi,
            PRN: self.prn,
            HLT: self.hlt,
            MUL: self.mul,
            PUSH: self.push,
            POP: self.pop,
            CALL: self.call,
            RET: self.ret
        }
        

    def load(self, program_file):
        """Load a program into memory."""

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
        print(op)
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
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

    def prn(self):
        key = int(self.ram_read(self.pc+1))
        print(int(self.reg[key]))

    def hlt(self):
        self.can_run = False
        exit()

    def add(self):
        self.alu('ADD', self.ram_read(self.pc+1), self.ram_read(self.pc+2))

    def mul(self):
        self.alu('MUL', self.ram_read(self.pc+1), self.ram_read(self.pc+2))
    
    def ldi(self):
        key = int(self.ram_read(self.pc+1))
        value = self.ram_read(self.pc+2)
        self.reg[key] = value
    
    def push(self):
        register = int(self.ram_read(self.pc+1))
        value = self.reg[register]
        self.reg[7] -=1
        self.ram_write(self.reg[7], value)
        

    def pop(self):
        register = int(self.ram_read(self.pc+1))
        self.reg[register] = self.ram[self.reg[7]]
        self.reg[7] +=1

    def call(self):
        register = int(self.ram_read(self.pc+1))
        value = self.pc + 2
        self.pc = self.reg[register]
        self.reg[7] -=1
        self.ram_write(self.reg[7], value)

    def ret(self):
        self.pc = self.ram[self.reg[7]]
        self.reg[7] +=1
        pass
   

    def run(self):
        """Run the CPU."""

        while self.can_run:
            #get instruction from ram
            ram_read_ins = self.ram_read(self.pc)
            # result = self.ram_write(self.ir, ram_read_ins)
            self.ir = ram_read_ins
            # if ram_read_ins == 0b00000001:
            #     self.can_run = False
            #     exit()
            format_ram_read_ins = '{0:8b}'.format(ram_read_ins)
            num_op = int(format_ram_read_ins[:2].strip() or '00',2)
            alu_op = int(format_ram_read_ins[2].strip() or '0',2)
            inst_set = int(format_ram_read_ins[3].strip() or '0',2)
            inst_iden = int(format_ram_read_ins[4:].strip() or '0000',2)

            self.branchtable[self.ir]()
            if inst_set == 0:
                self.pc += num_op + 1

            # if alu_op == int('1', 2):
            #     self.alu('MUL', self.ram_read(self.pc+1), self.ram_read(self.pc+2))
            #     # print(output)
            #     self.pc += int(num_op) + 1
            # else:
            #     if ram_read_ins == 0b10000010:
            #         key = int(self.ram_read(self.pc+1))
            #         value = self.ram_read(self.pc+2)
            #         self.reg[key] = value
            #         self.pc += int(num_op) + 1
            #     elif ram_read_ins == 0b01000111:
            #         key = int(self.ram_read(self.pc+1))
            #         print(int(self.reg[key]))
            #         self.pc += int(num_op) + 1
            
                     
            # if inst_set is not int('1', 2):
            #     self.pc += int(num_op)





            #DECODE operation
            
            #EXECUTE op.

