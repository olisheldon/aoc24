#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <map>
#include <set>
#include <algorithm>

// Read the grid from file
std::vector<std::vector<char>> read_grid(const std::string& filename) {
    std::ifstream infile(filename);
    std::vector<std::vector<char>> grid;
    std::string line;
    while (std::getline(infile, line)) {
        if (!line.empty()) grid.emplace_back(line.begin(), line.end());
    }
    return grid;
}

// Part 1: Find unique antinode locations
int part1(const std::vector<std::vector<char>>& grid) {
    int ROWS = grid.size(), COLS = grid[0].size();
    std::map<char, std::vector<std::pair<int, int>>> node_symbols;
    for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLS; ++c) {
            if (grid[r][c] != '.') node_symbols[grid[r][c]].emplace_back(r, c);
        }
    }
    std::set<std::pair<int, int>> antinode_locations;
    for (const auto& [symbol, locs] : node_symbols) {
        for (size_t i = 0; i < locs.size(); ++i) {
            for (size_t j = i + 1; j < locs.size(); ++j) {
                auto [x0, y0] = locs[i];
                auto [x1, y1] = locs[j];
                if (std::tie(x0, y0) > std::tie(x1, y1)) std::swap(x0, x1), std::swap(y0, y1);
                int dx = x1 - x0, dy = y1 - y0;
                antinode_locations.emplace(x0 + 2 * dx, y0 + 2 * dy);
                antinode_locations.emplace(x1 - 2 * dx, y1 - 2 * dy);
            }
        }
    }
    // Only count those within bounds
    int count = 0;
    for (const auto& loc : antinode_locations) {
        int r = loc.first, c = loc.second;
        if (r >= 0 && r < ROWS && c >= 0 && c < COLS) ++count;
    }
    return count;
}

// Part 2: Find all antinode locations extended along the direction, plus all node locations
int part2(const std::vector<std::vector<char>>& grid) {
    int ROWS = grid.size(), COLS = grid[0].size();
    std::map<char, std::vector<std::pair<int, int>>> node_symbols;
    for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLS; ++c) {
            if (grid[r][c] != '.') node_symbols[grid[r][c]].emplace_back(r, c);
        }
    }
    std::set<std::pair<int, int>> antinode_locations;
    for (const auto& [symbol, locs] : node_symbols) {
        for (size_t i = 0; i < locs.size(); ++i) {
            for (size_t j = i + 1; j < locs.size(); ++j) {
                auto [x0, y0] = locs[i];
                auto [x1, y1] = locs[j];
                if (std::tie(x0, y0) > std::tie(x1, y1)) std::swap(x0, x1), std::swap(y0, y1);
                int dx = x1 - x0, dy = y1 - y0;
                // Extend from (x0, y0) in direction (dx, dy)
                int steps = 1;
                while (true) {
                    int r = x0 + (1 + steps) * dx;
                    int c = y0 + (1 + steps) * dy;
                    if (r < 0 || r >= ROWS || c < 0 || c >= COLS) break;
                    antinode_locations.emplace(r, c);
                    ++steps;
                }
                steps = 1;
                while (true) {
                    int r = x1 - (1 + steps) * dx;
                    int c = y1 - (1 + steps) * dy;
                    if (r < 0 || r >= ROWS || c < 0 || c >= COLS) break;
                    antinode_locations.emplace(r, c);
                    ++steps;
                }
            }
        }
    }
    // Add all node locations
    for (const auto& [symbol, locs] : node_symbols) {
        for (const auto& loc : locs) antinode_locations.insert(loc);
    }
    // Only count those within bounds
    int count = 0;
    for (const auto& loc : antinode_locations) {
        int r = loc.first, c = loc.second;
        if (r >= 0 && r < ROWS && c >= 0 && c < COLS) ++count;
    }
    return count;
}

int main(int argc, char* argv[]) {
    std::string filename = argc > 1 ? argv[1] : "../data/day8.txt";
    auto grid = read_grid(filename);
    std::cout << "part1=" << part1(grid) << std::endl;
    std::cout << "part2=" << part2(grid) << std::endl;
    return 0;
} 