#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <regex>

// Part 1: Sum all x*y for every 'mul(x,y)' in the input
int part1(const std::string& input) {
    std::regex mul_pattern(R"(mul\((\d+),(\d+)\))");
    std::sregex_iterator it(input.begin(), input.end(), mul_pattern);
    std::sregex_iterator end;
    int sum = 0;
    for (; it != end; ++it) {
        int x = std::stoi((*it)[1]);
        int y = std::stoi((*it)[2]);
        sum += x * y;
    }
    return sum;
}

// Part 2: Only sum x*y when in 'do' mode, toggled by 'do()' and 'don't()'
int part2(const std::string& input) {
    std::regex pattern(R"(mul\((\d+),(\d+)\)|do\(\)|don't\(\))");
    std::sregex_iterator it(input.begin(), input.end(), pattern);
    std::sregex_iterator end;
    int sum = 0;
    bool do_mode = true;
    for (; it != end; ++it) {
        if ((*it)[0] == "do()") {
            do_mode = true;
        } else if ((*it)[0] == "don't()") {
            do_mode = false;
        } else if (do_mode && (*it)[1].matched && (*it)[2].matched) {
            int x = std::stoi((*it)[1]);
            int y = std::stoi((*it)[2]);
            sum += x * y;
        }
    }
    return sum;
}

// Read the entire file as a string
std::string read_input(const std::string& filename) {
    std::ifstream infile(filename);
    std::ostringstream ss;
    ss << infile.rdbuf();
    return ss.str();
}

int main(int argc, char* argv[]) {
    std::string filename = argc > 1 ? argv[1] : "../data/day3.txt";
    std::string input = read_input(filename);
    std::cout << "part1=" << part1(input) << std::endl;
    std::cout << "part2=" << part2(input) << std::endl;
    return 0;
} 