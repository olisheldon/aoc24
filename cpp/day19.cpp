#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>

// Parse the input file and return towels and target towels
void parse(const std::string& filename, std::vector<std::string>& towels, std::vector<std::string>& target_towels) {
    std::ifstream infile(filename);
    std::string line, towels_str, targets_str;
    bool reading_towels = true;
    while (std::getline(infile, line)) {
        if (line.empty()) {
            reading_towels = false;
            continue;
        }
        if (reading_towels) {
            towels_str += line;
        } else {
            if (!line.empty()) targets_str += line + '\n';
        }
    }
    // Parse towels
    std::istringstream towel_stream(towels_str);
    std::string towel;
    while (std::getline(towel_stream, towel, ',')) {
        if (!towel.empty() && towel[0] == ' ') towel = towel.substr(1);
        if (!towel.empty()) towels.push_back(towel);
    }
    // Parse target towels
    std::istringstream target_stream(targets_str);
    std::string target;
    while (std::getline(target_stream, target)) {
        if (!target.empty()) target_towels.push_back(target);
    }
}

// Part 1: For each target towel, check if it can be constructed from towels
int part1(const std::vector<std::string>& towels, const std::vector<std::string>& target_towels) {
    int total = 0;
    for (const auto& target : target_towels) {
        std::vector<bool> res(target.size() + 1, false);
        res[target.size()] = true;
        for (int i = (int)target.size() - 1; i >= 0; --i) {
            for (const auto& towel : towels) {
                if (i + towel.size() <= target.size() && target.substr(i, towel.size()) == towel) {
                    res[i] = std::max(res[i], res[i + towel.size()]);
                }
            }
        }
        total += res[0];
    }
    return total;
}

// Part 2: For each target towel, count the number of ways it can be constructed from towels
long long part2(const std::vector<std::string>& towels, const std::vector<std::string>& target_towels) {
    // Use long long to prevent overflow for large counts
    long long total = 0;
    for (const auto& target : target_towels) {
        std::vector<long long> res(target.size() + 1, 0);
        res[target.size()] = 1;
        for (int i = (int)target.size() - 1; i >= 0; --i) {
            for (const auto& towel : towels) {
                if (i + towel.size() <= target.size() && target.substr(i, towel.size()) == towel) {
                    res[i] += res[i + towel.size()];
                }
            }
        }
        total += res[0];
    }
    return total;
}

int main(int argc, char* argv[]) {
    std::string filename;
    if (argc > 1) {
        filename = argv[1];
    } else {
        filename = "../data/day19.txt";
    }
    std::vector<std::string> towels, target_towels;
    parse(filename, towels, target_towels);
    std::cout << "part1=" << part1(towels, target_towels) << std::endl;
    std::cout << "part2=" << part2(towels, target_towels) << std::endl;
    return 0;
} 