#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <set>
#include <queue>
#include <map>
#include <cmath>
#include <functional>

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

// Part 1: DFS to compute perimeter and area for each region
std::vector<std::pair<int, int>> part1_helper(const std::vector<std::vector<char>>& grid) {
    int ROWS = grid.size(), COLS = grid[0].size();
    const std::vector<std::pair<int, int>> NEIGHBOURS = {{1,0},{-1,0},{0,1},{0,-1}};
    std::set<std::pair<int, int>> visited;
    std::vector<std::pair<int, int>> res;
    auto calc_perimeter = [&](int r, int c, char veg) {
        int perimeter = 0;
        for (auto [dr, dc] : NEIGHBOURS) {
            int nr = r + dr, nc = c + dc;
            if (nr < 0 || nr >= ROWS || nc < 0 || nc >= COLS || grid[nr][nc] != veg) perimeter++;
        }
        return perimeter;
    };
    std::function<std::pair<int, int>(int, int, char)> dfs = [&](int r, int c, char veg) -> std::pair<int, int> {
        if (visited.count({r, c}) || r < 0 || r >= ROWS || c < 0 || c >= COLS || grid[r][c] != veg) return {0, 0};
        visited.insert({r, c});
        int perim = calc_perimeter(r, c, veg);
        int area = 1;
        for (auto [dr, dc] : NEIGHBOURS) {
            auto [p, a] = dfs(r + dr, c + dc, veg);
            perim += p;
            area += a;
        }
        return {perim, area};
    };
    for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLS; ++c) {
            if (!visited.count({r, c})) {
                res.push_back(dfs(r, c, grid[r][c]));
            }
        }
    }
    return res;
}

int part1(const std::vector<std::vector<char>>& grid) {
    auto regions = part1_helper(grid);
    int sum = 0;
    for (const auto& [perim, area] : regions) sum += perim * area;
    return sum;
}

// Part 2: BFS to find regions, then count sides as described
int part2(const std::vector<std::vector<char>>& grid) {
    int rows = grid.size(), cols = grid[0].size();
    std::set<std::pair<int, int>> seen;
    std::vector<std::pair<char, std::set<std::pair<int, int>>>> regions;
    for (int r = 0; r < rows; ++r) {
        for (int c = 0; c < cols; ++c) {
            if (seen.count({r, c})) continue;
            char crop = grid[r][c];
            std::set<std::pair<int, int>> region = {{r, c}};
            seen.insert({r, c});
            std::queue<std::pair<int, int>> q;
            q.push({r, c});
            while (!q.empty()) {
                auto [cr, cc] = q.front(); q.pop();
                for (auto [dr, dc] : std::vector<std::pair<int, int>>{{-1,0},{1,0},{0,-1},{0,1}}) {
                    int nr = cr + dr, nc = cc + dc;
                    if (nr < 0 || nc < 0 || nr >= rows || nc >= cols) continue;
                    if (grid[nr][nc] != crop) continue;
                    if (region.count({nr, nc})) continue;
                    region.insert({nr, nc});
                    seen.insert({nr, nc});
                    q.push({nr, nc});
                }
            }
            regions.emplace_back(crop, region);
        }
    }
    auto count_sides = [](const std::set<std::pair<int, int>>& region) {
        std::set<std::pair<double, double>> corner_candidates;
        for (auto [r, c] : region) {
            corner_candidates.insert({r-0.5, c-0.5});
            corner_candidates.insert({r+0.5, c-0.5});
            corner_candidates.insert({r+0.5, c+0.5});
            corner_candidates.insert({r-0.5, c+0.5});
        }
        int corners = 0;
        for (auto [cr, cc] : corner_candidates) {
            std::vector<bool> config = {
                region.count({(int)(cr-0.5), (int)(cc-0.5)}) > 0,
                region.count({(int)(cr+0.5), (int)(cc-0.5)}) > 0,
                region.count({(int)(cr+0.5), (int)(cc+0.5)}) > 0,
                region.count({(int)(cr-0.5), (int)(cc+0.5)}) > 0
            };
            int number = config[0] + config[1] + config[2] + config[3];
            if (number == 1) corners += 1;
            else if (number == 2) {
                if ((config[0] && config[2]) || (config[1] && config[3])) corners += 2;
            } else if (number == 3) corners += 1;
        }
        return corners;
    };
    int total_price = 0;
    for (const auto& [crop, region] : regions) {
        int area = region.size();
        int sides = count_sides(region);
        int price = area * sides;
        total_price += price;
    }
    return total_price;
}

int main(int argc, char* argv[]) {
    std::string filename = argc > 1 ? argv[1] : "../data/day12.txt";
    auto grid = read_grid(filename);
    std::cout << "part1=" << part1(grid) << std::endl;
    std::cout << "part2=" << part2(grid) << std::endl;
    return 0;
} 