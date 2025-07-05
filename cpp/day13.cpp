#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <limits>
#include <cmath>

// Use long long for all fields to prevent overflow in part 2
struct Machine {
    long long a_dx, a_dy, b_dx, b_dy, x, y;
};

// Parse input as described
std::vector<Machine> parse_input(const std::string& filename) {
    std::ifstream infile(filename);
    std::string content((std::istreambuf_iterator<char>(infile)), std::istreambuf_iterator<char>());
    std::vector<Machine> machines;
    std::istringstream ss(content);
    std::string block;
    while (std::getline(ss, block, '\n')) {
        if (block.empty()) continue;
        std::vector<std::string> lines;
        lines.push_back(block);
        for (int i = 0; i < 2; ++i) {
            std::string line;
            if (!std::getline(ss, line)) break;
            if (!line.empty()) lines.push_back(line);
        }
        if (lines.size() != 3) continue;
        auto parse_line = [](const std::string& s, long long& dx, long long& dy) {
            size_t x_pos = s.find("X+");
            size_t y_pos = s.find(", Y+");
            dx = std::stoll(s.substr(x_pos + 2, y_pos - (x_pos + 2)));
            dy = std::stoll(s.substr(y_pos + 4));
        };
        long long a_dx, a_dy, b_dx, b_dy, x, y;
        parse_line(lines[0], a_dx, a_dy);
        parse_line(lines[1], b_dx, b_dy);
        size_t x_pos = lines[2].find("X=");
        size_t y_pos = lines[2].find(", Y=");
        x = std::stoll(lines[2].substr(x_pos + 2, y_pos - (x_pos + 2)));
        y = std::stoll(lines[2].substr(y_pos + 4));
        machines.push_back({a_dx, a_dy, b_dx, b_dy, x, y});
    }
    return machines;
}

// Brute force for part1 (small numbers, int is fine)
std::pair<int, bool> find_min_tokens(long long a_dx, long long a_dy, long long b_dx, long long b_dy, long long prize_x, long long prize_y) {
    int min_tokens = std::numeric_limits<int>::max();
    bool is_possible = false;
    for (int a_presses = 0; a_presses <= 100; ++a_presses) {
        for (int b_presses = 0; b_presses <= 100; ++b_presses) {
            long long final_x = a_presses * a_dx + b_presses * b_dx;
            long long final_y = a_presses * a_dy + b_presses * b_dy;
            if (final_x == prize_x && final_y == prize_y) {
                int tokens = a_presses * 3 + b_presses * 1;
                if (tokens < min_tokens) min_tokens = tokens;
                is_possible = true;
            }
        }
    }
    return {min_tokens, is_possible};
}

// Solve linear equation for part2 (all long long)
std::pair<long long, long long>* solve_linear_equation(long long a_dx, long long a_dy, long long b_dx, long long b_dy, long long prize_x, long long prize_y) {
    long long det = a_dx * b_dy - a_dy * b_dx;
    if (det == 0) return nullptr;
    long long x_num = prize_x * b_dy - prize_y * b_dx;
    long long y_num = a_dx * prize_y - a_dy * prize_x;
    if (x_num % det != 0 || y_num % det != 0) return nullptr;
    long long x = x_num / det;
    long long y = y_num / det;
    if (x < 0 || y < 0) return nullptr;
    return new std::pair<long long, long long>(x, y);
}

int part1(const std::vector<Machine>& machines) {
    int total_tokens = 0;
    for (const auto& m : machines) {
        auto [min_tokens, is_possible] = find_min_tokens(m.a_dx, m.a_dy, m.b_dx, m.b_dy, m.x, m.y);
        if (is_possible) total_tokens += min_tokens;
    }
    return total_tokens;
}

long long part2(const std::vector<Machine>& machines) {
    long long total_tokens = 0;
    for (const auto& m : machines) {
        long long px = m.x + 10000000000000LL;
        long long py = m.y + 10000000000000LL;
        auto sol = solve_linear_equation(m.a_dx, m.a_dy, m.b_dx, m.b_dy, px, py);
        if (sol) {
            long long a_presses = sol->first, b_presses = sol->second;
            total_tokens += a_presses * 3 + b_presses * 1;
            delete sol;
        }
    }
    return total_tokens;
}

int main(int argc, char* argv[]) {
    std::string filename = argc > 1 ? argv[1] : "../data/day13.txt";
    auto machines = parse_input(filename);
    std::cout << "part1=" << part1(machines) << std::endl;
    std::cout << "part2=" << part2(machines) << std::endl;
    return 0;
} 