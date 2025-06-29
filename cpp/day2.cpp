#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cmath>

// Check if a sequence is 'safe' as per the problem definition
bool safe(const std::vector<int>& report) {
    bool inc = true, dec = true;
    for (size_t i = 1; i < report.size(); ++i) {
        if (report[i-1] >= report[i]) inc = false;
        if (report[i-1] <= report[i]) dec = false;
        int diff = std::abs(report[i] - report[i-1]);
        if (diff < 1 || diff > 3) return false;
    }
    return inc || dec;
}

// Part 1: Count how many reports are 'safe'
int part1(const std::vector<std::vector<int>>& reports) {
    int count = 0;
    for (const auto& report : reports) {
        if (safe(report)) ++count;
    }
    return count;
}

// Part 2: For each report, check if removing any one element makes it 'safe'
int part2(const std::vector<std::vector<int>>& reports) {
    int count = 0;
    for (const auto& report : reports) {
        bool found = false;
        for (size_t i = 0; i < report.size(); ++i) {
            std::vector<int> mod_report;
            for (size_t j = 0; j < report.size(); ++j) {
                if (j != i) mod_report.push_back(report[j]);
            }
            if (safe(mod_report)) {
                found = true;
                break;
            }
        }
        if (found) ++count;
    }
    return count;
}

// Parse input: each line is a sequence of integers
std::vector<std::vector<int>> parse_input(const std::string& filename) {
    std::ifstream infile(filename);
    std::vector<std::vector<int>> reports;
    std::string line;
    while (std::getline(infile, line)) {
        if (line.empty()) continue;
        std::istringstream iss(line);
        std::vector<int> report;
        int x;
        while (iss >> x) report.push_back(x);
        reports.push_back(report);
    }
    return reports;
}

int main(int argc, char* argv[]) {
    std::string filename = argc > 1 ? argv[1] : "../data/day2.txt";
    auto reports = parse_input(filename);
    std::cout << "part1=" << part1(reports) << std::endl;
    std::cout << "part2=" << part2(reports) << std::endl;
    return 0;
} 