#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <set>
#include <tuple>
#include <algorithm>
#include <functional>

// Computer class simulates the custom instruction set
class Computer {
private:
    // State variables
    long long a, b, c;
    std::vector<int> program_data;
    int instruction_ptr;
    std::vector<std::string> output;
    std::set<std::tuple<long long, long long, long long, int>> states;
    bool loop;

    // Helper methods
    void detect_loop() {
        auto state = std::make_tuple(a, b, c, instruction_ptr);
        if (states.count(state)) {
            loop = true;
            return;
        }
        states.insert(state);
    }

    long long combo(int val) {
        if (val >= 0 && val < 4) return val;
        else if (val == 4) return a;
        else if (val == 5) return b;
        else if (val == 6) return c;
        else throw std::runtime_error("Invalid program!");
    }

    int literal(int val) { return val; }

    // Instruction implementations
    void adv(int operand) {
        instruction_ptr += 2;
        a = a / (1LL << combo(operand));
    }

    void bxl(int operand) {
        instruction_ptr += 2;
        b = b ^ literal(operand);
    }

    void bst(int operand) {
        instruction_ptr += 2;
        b = combo(operand) % 8;
    }

    void jnz(int operand) {
        if (a == 0) {
            instruction_ptr += 2;
            return;
        }
        instruction_ptr = literal(operand);
    }

    void bxc(int operand) {
        instruction_ptr += 2;
        b = b ^ c;
    }

    void out(int operand) {
        instruction_ptr += 2;
        output.push_back(std::to_string(combo(operand) % 8));
    }

    void bdv(int operand) {
        instruction_ptr += 2;
        b = a / (1LL << combo(operand));
    }

    void cdv(int operand) {
        instruction_ptr += 2;
        c = a / (1LL << combo(operand));
    }

    void run_command(int opcode, int operand) {
        detect_loop();
        switch (opcode) {
            case 0: adv(operand); break;
            case 1: bxl(operand); break;
            case 2: bst(operand); break;
            case 3: jnz(operand); break;
            case 4: bxc(operand); break;
            case 5: out(operand); break;
            case 6: bdv(operand); break;
            case 7: cdv(operand); break;
            default: throw std::runtime_error("Invalid opcode");
        }
    }

public:
    // Constructor
    Computer(const std::vector<int>& registers, const std::vector<int>& program, long long a_init = 0) {
        a = a_init ? a_init : registers[0];
        b = registers[1];
        c = registers[2];
        program_data = program;
        instruction_ptr = 0;
        output.clear();
        states.clear();
        loop = false;
    }

    // Public interface methods
    void reset_state(long long a_value) {
        a = a_value;
        b = 0;
        c = 0;
        instruction_ptr = 0;
        output.clear();
        states.clear();
        loop = false;
    }

    void validate_program() {
        if (program_data.size() < 2 || program_data[program_data.size() - 2] != 3 || program_data[program_data.size() - 1] != 0) {
            throw std::runtime_error("Program must end with JNZ 0");
        }
        int adv_count = 0;
        for (size_t i = 0; i + 1 < program_data.size() - 2; i += 2) {
            if (program_data[i] == 0) {
                adv_count++;
                if (program_data[i + 1] != 3) throw std::runtime_error("ADV instruction must have operand 3");
            }
        }
        if (adv_count != 1) throw std::runtime_error("Program must have exactly one ADV instruction");
    }

    int simulate_until_output() {
        while (instruction_ptr < (int)program_data.size() - 1) {
            int opcode = program_data[instruction_ptr];
            int operand = program_data[instruction_ptr + 1];
            if (opcode == 5) { // out
                int val = combo(operand) % 8;
                instruction_ptr += 2;
                return val;
            } else {
                run_command(opcode, operand);
            }
            if (loop) return -1;
        }
        return -1;
    }

    long long find_self_replicating_value() {
        validate_program();
        std::function<long long(const std::vector<int>&, long long)> find_value = [&](const std::vector<int>& target, long long current_value) -> long long {
            if (target.empty()) return current_value;
            for (int bit_value = 0; bit_value < 8; ++bit_value) {
                long long candidate = (current_value << 3) | bit_value;
                reset_state(candidate);
                int output = simulate_until_output();
                if (output == target.back()) {
                    std::vector<int> next_target(target.begin(), target.end() - 1);
                    long long result = find_value(next_target, candidate);
                    if (result != -1) return result;
                }
            }
            return -1;
        };
        return find_value(program_data, 0);
    }

    std::string run() {
        while (instruction_ptr < (int)program_data.size()) {
            int opcode = program_data[instruction_ptr];
            int operand = program_data[instruction_ptr + 1];
            run_command(opcode, operand);
        }
        std::string result;
        for (size_t i = 0; i < output.size(); ++i) {
            if (i > 0) result += ",";
            result += output[i];
        }
        return result;
    }
};

// Parse the input file and return registers and program data
void parse(const std::string& filename, std::vector<int>& registers, std::vector<int>& program_data) {
    std::ifstream infile(filename);
    std::string line, registers_str, program_str;
    bool reading_registers = true;
    while (std::getline(infile, line)) {
        if (line.empty()) {
            reading_registers = false;
            continue;
        }
        if (reading_registers) {
            registers_str += line + '\n';
        } else {
            program_str += line;
        }
    }
    // Parse registers
    std::istringstream reg_stream(registers_str);
    while (std::getline(reg_stream, line)) {
        if (!line.empty()) {
            size_t pos = line.find(": ");
            registers.push_back(std::stoi(line.substr(pos + 2)));
        }
    }
    // Parse program data
    size_t pos = program_str.find(": ");
    std::string nums = program_str.substr(pos + 2);
    std::istringstream num_stream(nums);
    std::string num;
    while (std::getline(num_stream, num, ',')) {
        if (!num.empty()) program_data.push_back(std::stoi(num));
    }
}

// Part 1: Run the program and output the result
std::string part1(const std::vector<int>& registers, const std::vector<int>& program_data) {
    Computer computer(registers, program_data);
    return computer.run();
}

// Part 2: Find the lowest initial value for register A that causes the program to output a copy of itself
long long part2(const std::vector<int>& registers, const std::vector<int>& program_data) {
    Computer computer(registers, program_data);
    return computer.find_self_replicating_value();
}

int main(int argc, char* argv[]) {
    std::string filename;
    if (argc > 1) {
        filename = argv[1];
    } else {
        filename = "../data/day17.txt";
    }
    std::vector<int> registers, program_data;
    parse(filename, registers, program_data);
    std::cout << "part1=" << part1(registers, program_data) << std::endl;
    std::cout << "part2=" << part2(registers, program_data) << std::endl;
    return 0;
} 