#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <set>
#include <tuple>

// Directions: up, right, down, left
const std::vector<std::pair<int, int>> ROTATIONS = {
    {-1, 0}, {0, 1}, {1, 0}, {0, -1}
};

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

// Part 1: Simulate movement from '^' and count unique visited cells
int part1(const std::vector<std::vector<char>>& grid) {
    int ROWS = grid.size(), COLS = grid[0].size();
    int start_r = -1, start_c = -1;
    for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLS; ++c) {
            if (grid[r][c] == '^') {
                start_r = r; start_c = c;
                break;
            }
        }
    }
    if (start_r == -1) return 0;
    std::set<std::pair<int, int>> visited;
    int dir = 0;
    int r = start_r, c = start_c;
    while (true) {
        visited.insert({r, c});
        int dr = ROTATIONS[dir].first, dc = ROTATIONS[dir].second;
        int nr = r + dr, nc = c + dc;
        if (nr < 0 || nr >= ROWS || nc < 0 || nc >= COLS) break;
        if (grid[nr][nc] == '#') {
            dir = (dir + 1) % 4;
        } else {
            r = nr; c = nc;
        }
    }
    return visited.size();
}

// Simulate movement for part2, return true if a loop is detected
bool sim(const std::vector<std::vector<char>>& grid, int start_r, int start_c) {
    int ROWS = grid.size(), COLS = grid[0].size();
    int dir = 0;
    int r = start_r, c = start_c;
    std::set<std::tuple<int, int, int, int>> visited_states;
    while (true) {
        int dr = ROTATIONS[dir].first, dc = ROTATIONS[dir].second;
        int nr = r + dr, nc = c + dc;
        if (nr < 0 || nr >= ROWS || nc < 0 || nc >= COLS) break;
        auto state = std::make_tuple(r, c, dr, dc);
        if (visited_states.count(state)) return true;
        visited_states.insert(state);
        if (grid[nr][nc] == '#') {
            dir = (dir + 1) % 4;
        } else {
            r = nr; c = nc;
        }
    }
    return false;
}

// Part 2: For each '.' cell, temporarily set to '#' and check for loop
int part2(std::vector<std::vector<char>> grid) {
    int ROWS = grid.size(), COLS = grid[0].size();
    int start_r = -1, start_c = -1;
    std::vector<std::pair<int, int>> potentials;
    for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLS; ++c) {
            if (grid[r][c] == '^') {
                start_r = r; start_c = c;
            } else if (grid[r][c] == '.') {
                potentials.emplace_back(r, c);
            }
        }
    }
    if (start_r == -1) return 0;
    int res = 0;
    for (auto [r, c] : potentials) {
        grid[r][c] = '#';
        if (sim(grid, start_r, start_c)) ++res;
        grid[r][c] = '.';
    }
    return res;
}

int main(int argc, char* argv[]) {
    std::string filename = argc > 1 ? argv[1] : "../data/day6.txt";
    auto grid = read_grid(filename);
    std::cout << "part1=" << part1(grid) << std::endl;
    std::cout << "part2=" << part2(grid) << std::endl;
    return 0;
} 