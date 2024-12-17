import sys

class Computer:
    
    def __init__(self, registers, program_data, a=0):
        self.a = a or registers[0]
        self.b = registers[1]
        self.c = registers[2]
        self.program_data = program_data
        
        self.instruction_ptr = 0
        self.output = []
        self.log = []
        self.states = set()
        self.loop = False
    
        self.opcode_to_op  = [
            self._adv,
            self._bxl,
            self._bst,
            self._jnz,
            self._bxc,
            self._out,
            self._bdv,
            self._cdv,
            ]
        
    def detect_loop(self):
        state = (self.a, self.b, self.c, self.instruction_ptr)
        if state in self.states:
            self.loop = True
            return
        self.states.add(state)
        
    def run_command(self, opcode, operand):
        self.detect_loop()
        self.opcode_to_op[opcode](operand)
        
    def _combo(self, val):
        assert val in range(8)
        if val in range(4):
            return val
        elif val == 4:
            return self.a
        elif val == 5:
            return self.b
        elif val == 6:
            return self.c
        else:
            raise RuntimeError("Invalid program!")
    
    def _literal(self, val):
        return val
    
    def _adv(self, operand):
        self.instruction_ptr += 2
        self.a = int(self.a / (2**self._combo(operand)))
    
    def _bxl(self, operand):
        self.instruction_ptr += 2
        self.b = self.b ^ self._literal(operand)
    
    def _bst(self, operand):
        self.instruction_ptr += 2
        self.b = self._combo(operand) % 8
    
    def _jnz(self, operand):
        if self.a == 0:
            self.instruction_ptr += 2
            return
        self.instruction_ptr = self._literal(operand)
    
    def _bxc(self, operand):
        self.instruction_ptr += 2
        self.b = self.b ^ self.c
    
    def _out(self, operand):
        self.instruction_ptr += 2
        self.output.append(str(self._combo(operand) % 8))
    
    def _bdv(self, operand):
        self.instruction_ptr += 2
        self.b = int(self.a / (2**self._combo(operand)))
    
    def _cdv(self, operand):
        self.instruction_ptr += 2
        self.c = int(self.a / (2**self._combo(operand)))
        
    def run(self):
        while self.instruction_ptr < len(self.program_data) - 1:
            opcode, operand = self.program_data[self.instruction_ptr : self.instruction_ptr + 2]
            self.run_command(opcode, operand)
            if self.loop:
                return ""
        return ",".join(self.output)
    
def part1():
    computer = Computer(*parse())
    output = computer.run()
    return output

def part2():
    register_init, program_data = parse()
    s = ",".join(map(str, program_data))
    a = 0
    computer = Computer(register_init, program_data, a)
    while computer.run() != s:
        print(a)
        a += 1
        computer = Computer(register_init, program_data, a)
    return a

def parse():
    with open(filename) as f:
        inp = f.read()

    register_init = []
    registers, program = inp.split("\n\n")
    for register in registers.split("\n"):
        register_init.append(int(register.split(": ")[1]))
    program_data = list(map(int, program.split(": ")[1].split(",")))
    
    return register_init, program_data

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day17.txt"

    print(part1())
    print(part2())
