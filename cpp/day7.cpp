#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <functional>

// Try to reach target using nums and allowed operations
bool poss_sums(long long target, const std::vector<long long>& nums, const std::vector<std::function<long long(long long, long long)>>& ops, int i = 0, long long curr = 0) {
    if (i == (int)nums.size()) return curr == target;
    if (curr > target) return false;
    for (const auto& op : ops) {
        if (poss_sums(target, nums, ops, i + 1, op(curr, nums[i]))) return true;
    }
    return false;
}

// Parse input: each line is 'target: n1 n2 n3 ...'
std::vector<std::pair<long long, std::vector<long long>>> parse_input(const std::string& filename) {
    std::ifstream infile(filename);
    std::vector<std::pair<long long, std::vector<long long>>> lines;
    std::string line;
    while (std::getline(infile, line)) {
        if (line.empty()) continue;
        size_t colon = line.find(':');
        // Check if colon exists in the line
        if (colon == std::string::npos) {
            // Skip lines without a colon and print a warning
            std::cerr << "Warning: Skipping malformed line (no colon): '" << line << "'\n";
            continue;
        }
        std::string target_str = line.substr(0, colon);
        // Check if the target part is not empty
        if (target_str.empty()) {
            std::cerr << "Warning: Skipping malformed line (empty target): '" << line << "'\n";
            continue;
        }
        long long target;
        try {
            // Use stoll to handle large numbers
            target = std::stoll(target_str);
        } catch (const std::exception& e) {
            // Skip lines where the target is not a valid integer
            std::cerr << "Warning: Skipping malformed line (invalid target): '" << line << "'\n";
            continue;
        }
        std::vector<long long> nums;
        std::istringstream iss(line.substr(colon + 1));
        long long x;
        while (iss >> x) nums.push_back(x);
        lines.emplace_back(target, nums);
    }
    return lines;
}

long long part1(const std::vector<std::pair<long long, std::vector<long long>>>& lines) {
    std::vector<std::function<long long(long long, long long)>> ops = {
        [](long long a, long long b) { return a + b; },
        [](long long a, long long b) { return a * b; }
    };
    long long sum = 0;
    for (const auto& [target, nums] : lines) {
        if (poss_sums(target, nums, ops)) sum += target;
    }
    return sum;
}

long long part2(const std::vector<std::pair<long long, std::vector<long long>>>& lines) {
    std::vector<std::function<long long(long long, long long)>> ops = {
        [](long long a, long long b) { return a + b; },
        [](long long a, long long b) { return a * b; },
        [](long long a, long long b) {
            std::string sa = std::to_string(a), sb = std::to_string(b);
            return std::stoll(sa + sb);
        }
    };
    long long sum = 0;
    for (const auto& [target, nums] : lines) {
        if (poss_sums(target, nums, ops)) sum += target;
    }
    return sum;
}

int main(int argc, char* argv[]) {
    std::string filename = argc > 1 ? argv[1] : "../data/day7.txt";
    auto lines = parse_input(filename);
    std::cout << "part1=" << part1(lines) << std::endl;
    std::cout << "part2=" << part2(lines) << std::endl;
    return 0;
} 