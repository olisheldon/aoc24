#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
#include <map>
#include <set>
#include <algorithm>
#include <cassert>
#include <string>

const char START = 'S';
const char END = 'E';
const char WALL = '#';
const char TRACK = '.';
const std::pair<int,int> INVALID_COORD = {-1, -1};
const std::vector<std::pair<int,int>> NEIGHBOURS = {{1,0},{-1,0},{0,1},{0,-1}};

const int PART_1_CHEAT_DISTANCE = 2;
const int PART_2_CHEAT_DISTANCE = 20;
const int PART_1_TIME_SAVED = 100;
const int PART_2_TIME_SAVED = 100;

using Grid = std::vector<std::vector<char>>;
using Coord = std::pair<int,int>;
using TimeMap = std::map<Coord, int>;

Grid parse(const std::string& filename) {
    std::ifstream fin(filename);
    std::string line;
    Grid grid;
    while (std::getline(fin, line)) {
        if (!line.empty()) {
            grid.push_back(std::vector<char>(line.begin(), line.end()));
        }
    }
    return grid;
}

// Helper: find start and end coordinates
std::pair<Coord, Coord> get_start_and_end(const Grid& grid) {
    Coord start = INVALID_COORD, end = INVALID_COORD;
    for (int r = 0; r < (int)grid.size(); ++r) {
        for (int c = 0; c < (int)grid[0].size(); ++c) {
            if (grid[r][c] == START) start = {r, c};
            if (grid[r][c] == END) end = {r, c};
        }
    }
    assert(start != INVALID_COORD && end != INVALID_COORD);
    return {start, end};
}

// Helper: Simple BFS to find min path from start to end
int min_path(const Grid& grid, Coord start, Coord end) {
    int ROWS = grid.size(), COLS = grid[0].size();
    std::set<Coord> visited;
    std::queue<std::tuple<int,int,int>> q; // steps, r, c
    q.push({0, start.first, start.second});
    
    while (!q.empty()) {
        auto [steps, r, c] = q.front(); q.pop();
        
        if (r < 0 || r >= ROWS || c < 0 || c >= COLS) continue;
        if (visited.count({r,c})) continue;
        if (grid[r][c] == WALL) continue;
        if (steps > 0 && grid[r][c] == START) continue;
        
        if (std::make_pair(r,c) == end) {
            return steps;
        }
        
        visited.insert({r,c});
        
        for (auto [dr, dc] : NEIGHBOURS) {
            q.push({steps+1, r+dr, c+dc});
        }
    }
    return -1;
}

// Precompute min path from every cell to end (no cheat)
TimeMap all_min_path_no_cheat(const Grid& grid, Coord end) {
    int ROWS = grid.size(), COLS = grid[0].size();
    TimeMap default_times;
    for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLS; ++c) {
            if (grid[r][c] == TRACK || grid[r][c] == START) {
                int dist = min_path(grid, {r,c}, end);
                if (dist != -1) {
                    default_times[{r,c}] = dist;
                }
            }
        }
    }
    default_times[end] = 0;
    return default_times;
}

// Helper: get all possible coords within cheat_distance (Manhattan)
std::vector<Coord> possible_coords(int r, int c, const Grid& grid, int cheat_distance) {
    cheat_distance += 1;  // Match Python behavior
    int ROWS = grid.size(), COLS = grid[0].size();
    std::vector<Coord> result;
    for (int dr = -cheat_distance; dr <= cheat_distance; ++dr) {
        for (int dc = -cheat_distance; dc <= cheat_distance; ++dc) {
            int nr = r + dr, nc = c + dc;
            if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS &&
                abs(nr - r) + abs(nc - c) < cheat_distance &&
                grid[nr][nc] != WALL)
                result.push_back({nr, nc});
        }
    }
    return result;
}

// Helper function to mimic Python's get_times_in_range behavior
std::vector<int> get_times_in_range(const Grid& grid, const TimeMap& default_times, Coord start, int cheat_distance) {
    int ROWS = grid.size(), COLS = grid[0].size();
    int time_from_start = default_times.at(start);
    std::vector<int> times_in_range;
    
    for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLS; ++c) {
            if (grid[r][c] == WALL) continue;
            int time_to_rc = time_from_start - default_times.at({r,c});
            for (auto [nr, nc] : possible_coords(r, c, grid, cheat_distance)) {
                int time_with_skip = time_to_rc + default_times.at({nr, nc}) + abs(r-nr) + abs(c-nc);
                int time_saved = time_from_start - time_with_skip;
                times_in_range.push_back(time_with_skip);
            }
        }
    }
    return times_in_range;
}

// Main logic 
int count_cheats(const Grid& grid, const TimeMap& default_times, Coord start, int cheat_distance, int min_time_saved) {
    int time_from_start = default_times.at(start);
    std::vector<int> times_in_range = get_times_in_range(grid, default_times, start, cheat_distance);
    
    int count = 0;
    for (int time_with_skip : times_in_range) {
        int time_saved = time_from_start - time_with_skip;
        if (time_saved >= min_time_saved) {
            ++count;
        }
    }
    return count;
}

int main(int argc, char* argv[]) {
    std::string filename = argc > 1 ? argv[1] : "../data/day20.txt";
    Grid grid = parse(filename);
    int ROWS = grid.size(), COLS = grid[0].size();
    auto [start, end] = get_start_and_end(grid);
    TimeMap default_times = all_min_path_no_cheat(grid, end);
    int part1 = count_cheats(grid, default_times, start, PART_1_CHEAT_DISTANCE, PART_1_TIME_SAVED);
    int part2 = count_cheats(grid, default_times, start, PART_2_CHEAT_DISTANCE, PART_2_TIME_SAVED);
    std::cout << "part1=" << part1 << std::endl;
    std::cout << "part2=" << part2 << std::endl;
    return 0;
} 
