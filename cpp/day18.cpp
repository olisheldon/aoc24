#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <queue>
#include <set>
#include <sstream>

// Grid size and number of steps
const int ROWS = 71;
const int COLS = 71;
const int NUM_STEPS = 1024;

const char EMPTY = '.';
const char WALL = '#';
const int dr[4] = {-1, 1, 0, 0};
const int dc[4] = {0, 0, 1, -1};

// Parse the input file and return a vector of (col, row) pairs
std::vector<std::pair<int, int>> parse(const std::string& filename) {
    std::ifstream infile(filename);
    std::string line;
    std::vector<std::pair<int, int>> coords;
    while (std::getline(infile, line)) {
        if (line.empty()) continue;
        std::istringstream iss(line);
        int c, r;
        char comma;
        iss >> c >> comma >> r;
        coords.emplace_back(c, r);
    }
    return coords;
}

// Create the grid with walls at the given coordinates
std::vector<std::vector<char>> create_grid(const std::vector<std::pair<int, int>>& coords, int num_steps) {
    std::vector<std::vector<char>> grid(ROWS, std::vector<char>(COLS, EMPTY));
    for (int i = 0; i < num_steps && i < (int)coords.size(); ++i) {
        int c = coords[i].first, r = coords[i].second;
        grid[r][c] = WALL;
    }
    return grid;
}

// Find the minimum path from (0,0) to (ROWS-1,COLS-1) using BFS
int min_path(const std::vector<std::pair<int, int>>& coords, int num_steps) {
    auto grid = create_grid(coords, num_steps);
    std::set<std::pair<int, int>> visited;
    using State = std::tuple<int, int, int>; // (steps, r, c)
    std::priority_queue<State, std::vector<State>, std::greater<State>> pq;
    pq.emplace(0, 0, 0);
    while (!pq.empty()) {
        auto [steps, r, c] = pq.top(); pq.pop();
        if (r == ROWS - 1 && c == COLS - 1) return steps;
        if (r < 0 || r >= ROWS || c < 0 || c >= COLS || visited.count({r, c}) || grid[r][c] == WALL) continue;
        visited.insert({r, c});
        for (int d = 0; d < 4; ++d) {
            int nr = r + dr[d], nc = c + dc[d];
            pq.emplace(steps + 1, nr, nc);
        }
    }
    return -1;
}

// Part 1: Find the shortest path with all steps
int part1(const std::vector<std::pair<int, int>>& coords) {
    return min_path(coords, NUM_STEPS);
}

// Part 2: Find the first step where the path is blocked, and return the coordinate that caused it
std::string part2(const std::vector<std::pair<int, int>>& coords) {
    int num_fallen = 0;
    while (min_path(coords, num_fallen) != -1) {
        num_fallen++;
    }
    int c = coords[num_fallen - 1].first;
    int r = coords[num_fallen - 1].second;
    return std::to_string(c) + "," + std::to_string(r);
}

int main(int argc, char* argv[]) {
    std::string filename;
    if (argc > 1) {
        filename = argv[1];
    } else {
        filename = "../data/day18.txt";
    }
    auto coords = parse(filename);
    std::cout << "part1=" << part1(coords) << std::endl;
    std::cout << "part2=" << part2(coords) << std::endl;
    return 0;
} 