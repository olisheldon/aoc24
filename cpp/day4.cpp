#include <iostream>
#include <fstream>
#include <vector>
#include <string>

// Directions: 8 possible (dx, dy) pairs
const std::vector<std::pair<int, int>> DIRECTIONS = {
    {1, 0}, {-1, 0}, {0, 1}, {0, -1},
    {1, 1}, {1, -1}, {-1, 1}, {-1, -1}
};
const std::string XMAS = "XMAS";

// Check if the word XMAS is found starting at (r, c) in direction (dr, dc)
bool word_found(const std::vector<std::string>& grid, int r, int c, int dr, int dc) {
    int ROWS = grid.size(), COLS = grid[0].size();
    for (int i = 0; i < (int)XMAS.size(); ++i) {
        int nr = r + dr * i, nc = c + dc * i;
        if (nr < 0 || nr >= ROWS || nc < 0 || nc >= COLS) return false;
        if (grid[nr][nc] != XMAS[i]) return false;
    }
    return true;
}

int part1(const std::vector<std::string>& grid) {
    int ROWS = grid.size(), COLS = grid[0].size();
    int count = 0;
    for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLS; ++c) {
            for (auto [dr, dc] : DIRECTIONS) {
                if (word_found(grid, r, c, dr, dc)) ++count;
            }
        }
    }
    return count;
}

// For part2, check the described diagonal pattern around 'A'
bool part2_pattern(const std::vector<std::string>& grid, int r, int c) {
    // Check bounds for diagonals
    int ROWS = grid.size(), COLS = grid[0].size();
    if (r - 1 < 0 || r + 1 >= ROWS || c - 1 < 0 || c + 1 >= COLS) return false;
    if (grid[r][c] != 'A') return false;
    // Check the four diagonal pairs
    bool cond1 = (grid[r-1][c-1] == 'M' && grid[r+1][c+1] == 'S') || (grid[r-1][c-1] == 'S' && grid[r+1][c+1] == 'M');
    bool cond2 = (grid[r+1][c-1] == 'M' && grid[r-1][c+1] == 'S') || (grid[r+1][c-1] == 'S' && grid[r-1][c+1] == 'M');
    return cond1 && cond2;
}

int part2(const std::vector<std::string>& grid) {
    int ROWS = grid.size(), COLS = grid[0].size();
    int count = 0;
    for (int r = 1; r < ROWS - 1; ++r) {
        for (int c = 1; c < COLS - 1; ++c) {
            if (part2_pattern(grid, r, c)) ++count;
        }
    }
    return count;
}

// Read the grid from file (each line is a row)
std::vector<std::string> read_grid(const std::string& filename) {
    std::ifstream infile(filename);
    std::vector<std::string> grid;
    std::string line;
    while (std::getline(infile, line)) {
        if (!line.empty()) grid.push_back(line);
    }
    return grid;
}

int main(int argc, char* argv[]) {
    std::string filename = argc > 1 ? argv[1] : "../data/day4.txt";
    auto grid = read_grid(filename);
    std::cout << "part1=" << part1(grid) << std::endl;
    std::cout << "part2=" << part2(grid) << std::endl;
    return 0;
} 