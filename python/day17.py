import sys
from pathlib import Path

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
        
    def reset_state(self, a_value):
        self.a = a_value
        self.b = 0
        self.c = 0
        self.instruction_ptr = 0
        self.output = []
        self.states.clear()
        self.loop = False
    
    def validate_program(self):
        if self.program_data[-2:] != [3, 0]:
            raise ValueError("Program must end with JNZ 0")
        
        adv_count = 0
        for i in range(0, len(self.program_data) - 2, 2):
            if self.program_data[i] == 0:  # ADV instruction
                adv_count += 1
                if self.program_data[i + 1] != 3:
                    raise ValueError("ADV instruction must have operand 3")
        
        if adv_count != 1:
            raise ValueError("Program must have exactly one ADV instruction")
    
    def simulate_until_output(self):
        while self.instruction_ptr < len(self.program_data) - 1:
            opcode, operand = self.program_data[self.instruction_ptr : self.instruction_ptr + 2]
            
            if opcode == 5:  # out
                val = self._combo(operand) % 8
                self.instruction_ptr += 2
                return val
            else:
                self.run_command(opcode, operand)
            
            if self.loop:
                return None
        
        return None
    
    def find_self_replicating_value(self):
        """
        Find the lowest positive initial value for register A that causes the program
        to output a copy of itself.
        
        The algorithm works by:
        1. Building the value for register A bit by bit (3 bits at a time)
        2. For each candidate value, simulating the program until it produces output
        3. If the output matches the expected value, recursing to find the next bits
        4. Continuing until we find a value that produces the entire program as output
        """
        self.validate_program()
        
        def find_value(target, current_value):
            if not target:
                return current_value
            
            for bit_value in range(8):
                candidate = (current_value << 3) | bit_value
                
                self.reset_state(candidate)
                output = self.simulate_until_output()
                
                if output == target[-1]:
                    result = find_value(target[:-1], candidate)
                    if result is not None:
                        return result
            
            return None
        
        return find_value(self.program_data, 0)
    
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
        while self.instruction_ptr < len(self.program_data):
            opcode, operand = self.program_data[self.instruction_ptr : self.instruction_ptr + 2]
            self.run_command(opcode, operand)
        return ",".join(self.output)

def part1():
    computer = Computer(*parse())
    output = computer.run()
    return output

def part2():
    computer = Computer(*parse())
    return computer.find_self_replicating_value()

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

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))
