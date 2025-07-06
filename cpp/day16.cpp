#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <queue>
#include <set>
#include <map>
#include <tuple>
#include <algorithm>
#include <climits>

// Constants for grid elements
const char START = 'S';
const char EMPTY = '.';
const char WALL = '#';
const char END = 'E';

// Directions
enum Direction { NORTH = 0, EAST = 1, SOUTH = 2, WEST = 3 };
const int dr[4] = {-1, 0, 1, 0};
const int dc[4] = {0, 1, 0, -1};

// Parse the input file and return the grid
std::vector<std::vector<char>> parse(const std::string& filename) {
    std::ifstream infile(filename);
    std::string line;
    std::vector<std::vector<char>> grid;
    while (std::getline(infile, line)) {
        if (!line.empty()) {
            grid.push_back(std::vector<char>(line.begin(), line.end()));
        }
    }
    return grid;
}

// Part 1: Dijkstra-like search for shortest path from S to E
int part1(const std::vector<std::vector<char>>& grid) {
    int ROWS = grid.size(), COLS = grid[0].size();
    int sr = -1, sc = -1;
    for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLS; ++c) {
            if (grid[r][c] == START) {
                sr = r; sc = c;
            }
        }
    }
    using State = std::tuple<int, int, int, int, std::vector<std::tuple<int, int, int>>>; // (score, r, c, dir, history)
    std::priority_queue<State, std::vector<State>, std::greater<State>> pq;
    pq.emplace(0, sr, sc, EAST, std::vector<std::tuple<int, int, int>>{});
    std::set<std::tuple<int, int, int, int>> visited;
    int final_score = -1;
    while (!pq.empty()) {
        auto [score, r, c, dir, history] = pq.top(); pq.pop();
        int drc = dr[dir], dcc = dc[dir];
        if (r < 0 || r >= ROWS || c < 0 || c >= COLS || grid[r][c] == WALL || visited.count({r, c, drc, dcc})) continue;
        if (grid[r][c] == END) {
            final_score = score;
            break;
        }
        visited.insert({r, c, drc, dcc});
        auto new_history = history;
        new_history.emplace_back(r, c, dir);
        // go straight
        pq.emplace(score + 1, r + drc, c + dcc, dir, new_history);
        // turn right
        pq.emplace(score + 1000, r, c, (dir + 1) % 4, new_history);
        // turn left
        pq.emplace(score + 1000, r, c, (dir + 3) % 4, new_history);
    }
    return final_score;
}

// Part 2: Dijkstra-like search, count unique tiles in all minimal-cost paths
int part2(const std::vector<std::vector<char>>& grid) {
    int ROWS = grid.size(), COLS = grid[0].size();
    int sr = -1, sc = -1;
    for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLS; ++c) {
            if (grid[r][c] == START) {
                sr = r; sc = c;
                break;
            }
        }
        if (sr != -1) break;
    }
    using State = std::tuple<int, int, int, int, int>; // (cost, r, c, dr, dc)
    auto cmp = [](const State& a, const State& b) { return std::get<0>(a) > std::get<0>(b); };
    std::priority_queue<State, std::vector<State>, decltype(cmp)> pq(cmp);
    pq.emplace(0, sr, sc, 0, 1); // start facing east
    std::map<std::tuple<int, int, int, int>, int> lowest_cost;
    std::map<std::tuple<int, int, int, int>, std::set<std::tuple<int, int, int, int>>> backtrack;
    int best_cost = INT_MAX;
    std::set<std::tuple<int, int, int, int>> end_states;
    lowest_cost[{sr, sc, 0, 1}] = 0;
    while (!pq.empty()) {
        auto [cost, r, c, drc, dcc] = pq.top(); pq.pop();
        if (cost > lowest_cost[{r, c, drc, dcc}]) continue;
        if (grid[r][c] == END) {
            if (cost > best_cost) break;
            best_cost = cost;
            end_states.insert({r, c, drc, dcc});
        }
        // go straight
        int nr = r + drc, nc = c + dcc;
        if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS && grid[nr][nc] != WALL) {
            int new_cost = cost + 1;
            auto key = std::make_tuple(nr, nc, drc, dcc);
            if (!lowest_cost.count(key) || new_cost < lowest_cost[key]) {
                backtrack[key] = {};
                lowest_cost[key] = new_cost;
            }
            if (new_cost <= lowest_cost[key]) {
                backtrack[key].insert({r, c, drc, dcc});
                pq.emplace(new_cost, nr, nc, drc, dcc);
            }
        }
        // turn right
        int ndr = dcc, ndc = -drc;
        if (grid[r][c] != WALL) {
            int new_cost = cost + 1000;
            auto key = std::make_tuple(r, c, ndr, ndc);
            if (!lowest_cost.count(key) || new_cost < lowest_cost[key]) {
                backtrack[key] = {};
                lowest_cost[key] = new_cost;
            }
            if (new_cost <= lowest_cost[key]) {
                backtrack[key].insert({r, c, drc, dcc});
                pq.emplace(new_cost, r, c, ndr, ndc);
            }
        }
        // turn left
        ndr = -dcc; ndc = drc;
        if (grid[r][c] != WALL) {
            int new_cost = cost + 1000;
            auto key = std::make_tuple(r, c, ndr, ndc);
            if (!lowest_cost.count(key) || new_cost < lowest_cost[key]) {
                backtrack[key] = {};
                lowest_cost[key] = new_cost;
            }
            if (new_cost <= lowest_cost[key]) {
                backtrack[key].insert({r, c, drc, dcc});
                pq.emplace(new_cost, r, c, ndr, ndc);
            }
        }
    }
    // Backtrack to find all unique tiles in minimal-cost paths
    std::deque<std::tuple<int, int, int, int>> states(end_states.begin(), end_states.end());
    std::set<std::tuple<int, int, int, int>> seen(end_states.begin(), end_states.end());
    while (!states.empty()) {
        auto key = states.front(); states.pop_front();
        for (const auto& last : backtrack[key]) {
            if (seen.count(last)) continue;
            seen.insert(last);
            states.push_back(last);
        }
    }
    std::set<std::pair<int, int>> unique_tiles;
    for (const auto& s : seen) {
        int r, c, drc, dcc;
        std::tie(r, c, drc, dcc) = s;
        unique_tiles.insert({r, c});
    }
    return unique_tiles.size();
}

int main(int argc, char* argv[]) {
    std::string filename;
    if (argc > 1) {
        filename = argv[1];
    } else {
        filename = "../data/day16.txt";
    }
    std::vector<std::vector<char>> grid = parse(filename);
    std::cout << "part1=" << part1(grid) << std::endl;
    std::cout << "part2=" << part2(grid) << std::endl;
    return 0;
} 