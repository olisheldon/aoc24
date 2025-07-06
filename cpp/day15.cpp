#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>

// Constants for grid elements
const char WALL = '#';
const char BOX = 'O';
const char ROBOT = '@';
const char EMPTY = '.';
const char WIDE_BOX_LEFT = '[';
const char WIDE_BOX_RIGHT = ']';

// Move directions: v, >, ^, <
const int dr[4] = {1, 0, -1, 0};
const int dc[4] = {0, 1, 0, -1};
const char moves_char[4] = {'v', '>', '^', '<'};

// Map move character to direction index
int move_index(char move) {
    for (int i = 0; i < 4; ++i) if (moves_char[i] == move) return i;
    return -1;
}

// Parse the input file and return the grid and moves
void parse(const std::string& filename, std::vector<std::vector<char>>& grid, std::string& moves) {
    std::ifstream infile(filename);
    std::string line, grid_str, moves_str;
    bool reading_grid = true;
    while (std::getline(infile, line)) {
        if (line.empty()) {
            reading_grid = false;
            continue;
        }
        if (reading_grid) {
            grid_str += line + '\n';
        } else {
            moves_str += line;
        }
    }
    // Build grid
    std::istringstream grid_stream(grid_str);
    while (std::getline(grid_stream, line)) {
        if (!line.empty()) {
            grid.push_back(std::vector<char>(line.begin(), line.end()));
        }
    }
    moves = moves_str;
}

// Compute the score for part 1
int score(const std::vector<std::vector<char>>& grid) {
    int total = 0;
    for (int r = 0; r < (int)grid.size(); ++r) {
        for (int c = 0; c < (int)grid[0].size(); ++c) {
            if (grid[r][c] == BOX) {
                total += 100 * r + c;
            }
        }
    }
    return total;
}

// Print the grid (for debugging)
void print_grid(const std::vector<std::vector<char>>& grid) {
    for (const auto& row : grid) {
        for (char ch : row) std::cout << ch;
        std::cout << '\n';
    }
    std::cout << std::endl;
}

// Part 1: Simulate robot and box movement
int part1(const std::vector<std::vector<char>>& orig_grid, const std::string& moves) {
    std::vector<std::vector<char>> grid = orig_grid;
    int ROWS = grid.size(), COLS = grid[0].size();
    int r = -1, c = -1;
    // Find robot position
    for (int i = 0; i < ROWS; ++i) {
        for (int j = 0; j < COLS; ++j) {
            if (grid[i][j] == ROBOT) {
                r = i; c = j;
            }
        }
    }
    for (char move : moves) {
        int idx = move_index(move);
        int drc = dr[idx], dcc = dc[idx];
        std::vector<std::pair<int, int>> stack;
        int nr = r + drc, nc = c + dcc;
        while (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS && grid[nr][nc] != EMPTY && grid[nr][nc] != WALL) {
            stack.emplace_back(nr, nc);
            nr += drc; nc += dcc;
        }
        if (nr < 0 || nr >= ROWS || nc < 0 || nc >= COLS || grid[nr][nc] == WALL) {
            continue;
        }
        while (!stack.empty()) {
            auto [x, y] = stack.back(); stack.pop_back();
            grid[nr][nc] = grid[x][y];
            nr -= drc; nc -= dcc;
        }
        grid[r][c] = EMPTY;
        grid[nr][nc] = ROBOT;
        r = nr; c = nc;
    }
    return score(grid);
}

// Widen the grid for part 2
std::vector<std::vector<char>> widen_grid(const std::vector<std::vector<char>>& grid) {
    std::vector<std::vector<char>> widened;
    for (const auto& row : grid) {
        std::vector<char> new_row;
        for (char elem : row) {
            if (elem == WALL) {
                new_row.push_back(WALL); new_row.push_back(WALL);
            } else if (elem == BOX) {
                new_row.push_back(WIDE_BOX_LEFT); new_row.push_back(WIDE_BOX_RIGHT);
            } else if (elem == EMPTY) {
                new_row.push_back(EMPTY); new_row.push_back(EMPTY);
            } else if (elem == ROBOT) {
                new_row.push_back(ROBOT); new_row.push_back(EMPTY);
            }
        }
        widened.push_back(new_row);
    }
    return widened;
}

// Compute the score for part 2 (wide boxes)
int score_wide_boxes(const std::vector<std::vector<char>>& grid) {
    int total = 0;
    for (int r = 0; r < (int)grid.size(); ++r) {
        for (int c = 0; c < (int)grid[0].size(); ++c) {
            if (grid[r][c] == WIDE_BOX_LEFT) {
                total += 100 * r + c;
            }
        }
    }
    return total;
}

// Part 2: Simulate robot and wide box movement
int part2(const std::vector<std::vector<char>>& orig_grid, const std::string& moves) {
    std::vector<std::vector<char>> grid = widen_grid(orig_grid);
    int ROWS = grid.size(), COLS = grid[0].size();
    int r = -1, c = -1;
    // Find robot position
    for (int i = 0; i < ROWS; ++i) {
        for (int j = 0; j < COLS; ++j) {
            if (grid[i][j] == ROBOT) {
                r = i; c = j;
                break;
            }
        }
        if (r != -1) break;
    }
    for (char move : moves) {
        int idx = move_index(move);
        int drc = dr[idx], dcc = dc[idx];
        std::vector<std::pair<int, int>> targets = {{r, c}};
        bool go = true;
        for (size_t i = 0; i < targets.size(); ++i) {
            int cr = targets[i].first, cc = targets[i].second;
            int nr = cr + drc, nc = cc + dcc;
            if (std::find(targets.begin(), targets.end(), std::make_pair(nr, nc)) != targets.end()) continue;
            if (nr < 0 || nr >= ROWS || nc < 0 || nc >= COLS) { go = false; break; }
            char ch = grid[nr][nc];
            if (ch == WALL) { go = false; break; }
            if (ch == WIDE_BOX_LEFT) {
                targets.emplace_back(nr, nc);
                targets.emplace_back(nr, nc + 1);
            }
            if (ch == WIDE_BOX_RIGHT) {
                targets.emplace_back(nr, nc);
                targets.emplace_back(nr, nc - 1);
            }
        }
        if (!go) continue;
        auto grid_copy = grid;
        grid[r][c] = EMPTY;
        for (size_t i = 1; i < targets.size(); ++i) {
            int br = targets[i].first, bc = targets[i].second;
            grid[br][bc] = EMPTY;
        }
        grid[r + drc][c + dcc] = ROBOT;
        for (size_t i = 1; i < targets.size(); ++i) {
            int br = targets[i].first, bc = targets[i].second;
            grid[br + drc][bc + dcc] = grid_copy[br][bc];
        }
        r += drc; c += dcc;
    }
    return score_wide_boxes(grid);
}

int main(int argc, char* argv[]) {
    std::string filename;
    if (argc > 1) {
        filename = argv[1];
    } else {
        filename = "../data/day15.txt";
    }
    std::vector<std::vector<char>> grid;
    std::string moves;
    parse(filename, grid, moves);
    std::cout << "part1=" << part1(grid, moves) << std::endl;
    std::cout << "part2=" << part2(grid, moves) << std::endl;
    return 0;
} 