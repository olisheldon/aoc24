#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <set>

const int SUMMIT = 9;
const int TRAILHEAD = 0;
const std::vector<std::pair<int, int>> NEIGHBOURS = {
    {1, 0}, {-1, 0}, {0, 1}, {0, -1}
};

// Read the grid from file
std::vector<std::vector<int>> read_grid(const std::string& filename) {
    std::ifstream infile(filename);
    std::vector<std::vector<int>> grid;
    std::string line;
    while (std::getline(infile, line)) {
        if (line.empty()) continue;
        std::vector<int> row;
        for (char ch : line) if (ch >= '0' && ch <= '9') row.push_back(ch - '0');
        grid.push_back(row);
    }
    return grid;
}

// DFS to count routes from (r, c) to summit
int dfs(const std::vector<std::vector<int>>& grid, int r, int c, int prev, std::set<std::pair<int, int>>& visited, bool count_trailheads) {
    int ROWS = grid.size(), COLS = grid[0].size();
    if (r < 0 || r >= ROWS || c < 0 || c >= COLS) return 0;
    if (visited.count({r, c})) return 0;
    if (grid[r][c] - prev != 1) return 0;
    if (grid[r][c] == SUMMIT) {
        if (count_trailheads) visited.insert({r, c});
        return 1;
    }
    int res = 0;
    visited.insert({r, c});
    for (auto [dr, dc] : NEIGHBOURS) {
        res += dfs(grid, r + dr, c + dc, grid[r][c], visited, count_trailheads);
    }
    visited.erase({r, c});
    return res;
}

// Calculate trailhead scores
int calc_trailhead_scores(const std::vector<std::vector<int>>& grid, bool count_trailheads) {
    int ROWS = grid.size(), COLS = grid[0].size();
    int res = 0;
    for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLS; ++c) {
            if (grid[r][c] == TRAILHEAD) {
                std::set<std::pair<int, int>> visited;
                res += dfs(grid, r, c, TRAILHEAD - 1, visited, count_trailheads);
            }
        }
    }
    return res;
}

int main(int argc, char* argv[]) {
    std::string filename = argc > 1 ? argv[1] : "../data/day10.txt";
    auto grid = read_grid(filename);
    std::cout << "part1=" << calc_trailhead_scores(grid, true) << std::endl;
    std::cout << "part2=" << calc_trailhead_scores(grid, false) << std::endl;
    return 0;
} 