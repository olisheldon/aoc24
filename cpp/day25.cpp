#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>

const char EMPTY = '.';
const char FILLED = '#';
const int FULL = 6;

using Row = std::vector<int>;
using Grid = std::vector<std::string>;

// Helper function: checks if key and lock do not overlap (sum in each column < FULL)
bool no_overlap(const Row& key, const Row& lock) {
    for (size_t i = 0; i < key.size(); ++i) {
        if (key[i] + lock[i] >= FULL) return false;
    }
    return true;
}

// Parses the input file into keys and locks
void parse(const std::string& filename, std::vector<Row>& keys, std::vector<Row>& locks) {
    std::ifstream infile(filename);
    if (!infile) {
        std::cerr << "Could not open file: " << filename << std::endl;
        exit(1);
    }
    std::string content((std::istreambuf_iterator<char>(infile)), std::istreambuf_iterator<char>());
    std::vector<std::string> grids;
    size_t pos = 0, prev = 0;
    // Split by double newline
    while ((pos = content.find("\n\n", prev)) != std::string::npos) {
        grids.push_back(content.substr(prev, pos - prev));
        prev = pos + 2;
    }
    grids.push_back(content.substr(prev));

    for (const auto& grid_str : grids) {
        std::istringstream ss(grid_str);
        std::vector<std::string> grid;
        std::string line;
        while (std::getline(ss, line)) {
            if (!line.empty() && line.back() == '\r') line.pop_back(); // Handle Windows line endings
            if (!line.empty()) grid.push_back(line);
        }
        if (grid.empty()) continue;
        Row rows(grid[0].size(), -1);
        for (const auto& row : grid) {
            for (size_t i = 0; i < row.size(); ++i) {
                if (row[i] == FILLED) rows[i] += 1;
            }
        }
        // If first row is all FILLED, it's a key; else, a lock
        bool is_key = std::all_of(grid[0].begin(), grid[0].end(), [](char c){ return c == FILLED; });
        if (is_key) keys.push_back(rows);
        else locks.push_back(rows);
    }
}

// Part 1 counts valid key-lock pairs
int part1(const std::string& filename) {
    std::vector<Row> keys, locks;
    parse(filename, keys, locks);
    int res = 0;
    for (const auto& lock : locks) {
        for (const auto& key : keys) {
            if (no_overlap(key, lock)) ++res;
        }
    }
    return res;
}

// Part 2 has no problem
std::string part2(const std::string&) {
    return "None";
}

int main(int argc, char* argv[]) {
    std::string filename;
    if (argc > 1) filename = argv[1];
    else filename = "../data/day25.txt";

    std::cout << "part1=" << part1(filename) << std::endl;
    std::cout << "part2=" << part2(filename) << std::endl;
    return 0;
} 