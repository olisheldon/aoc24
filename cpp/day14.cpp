#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
#include <numeric>
#include <tuple>
#include <climits>

// Constants for grid size
const int ROWS = 101;
const int COLS = 103;

// Struct to represent a robot with position and velocity
struct Robot {
    int px, py; // position
    int vx, vy; // velocity
};

// Parse the input file and return a vector of robots
std::vector<Robot> parse(const std::string& filename) {
    std::vector<Robot> robots;
    std::ifstream infile(filename);
    std::string line;
    while (std::getline(infile, line)) {
        if (line.empty()) continue;
        // Format: p=1,2 v=3,4
        size_t p_pos = line.find("p=");
        size_t v_pos = line.find("v=");
        std::string pos_str = line.substr(p_pos + 2, v_pos - p_pos - 3);
        std::string vel_str = line.substr(v_pos + 2);
        int px, py, vx, vy;
        sscanf(pos_str.c_str(), "%d,%d", &px, &py);
        sscanf(vel_str.c_str(), "%d,%d", &vx, &vy);
        robots.push_back({px, py, vx, vy});
    }
    return robots;
}

// Compute the number of robots in each quadrant (excluding center lines)
std::vector<int> safety_value(const std::vector<Robot>& robots) {
    std::vector<int> quadrants(4, 0);
    for (const auto& r : robots) {
        if (r.px == ROWS / 2 || r.py == COLS / 2) continue;
        if (r.px < ROWS / 2 && r.py < COLS / 2) quadrants[0]++;
        if (r.px >= ROWS / 2 && r.py < COLS / 2) quadrants[1]++;
        if (r.px < ROWS / 2 && r.py >= COLS / 2) quadrants[2]++;
        if (r.px >= ROWS / 2 && r.py >= COLS / 2) quadrants[3]++;
    }
    return quadrants;
}

// Part 1: Simulate 100 steps and return the product of quadrant counts
long long part1(const std::vector<Robot>& orig_robots) {
    std::vector<Robot> robots = orig_robots;
    for (int step = 0; step < 100; ++step) {
        for (auto& r : robots) {
            r.px = (r.px + r.vx + ROWS) % ROWS;
            r.py = (r.py + r.vy + COLS) % COLS;
        }
    }
    std::vector<int> quads = safety_value(robots);
    return std::accumulate(quads.begin(), quads.end(), 1LL, std::multiplies<long long>());
}

// Part 2: Find the iteration with the minimum nonzero product of quadrant counts
int part2(const std::vector<Robot>& robots) {
    long long min_sf = LLONG_MAX;
    int best_iteration = -1;
    for (int iteration = 0; iteration < ROWS * COLS; ++iteration) {
        std::vector<Robot> current_robots;
        for (const auto& r : robots) {
            int new_px = (r.px + r.vx * iteration) % ROWS;
            if (new_px < 0) new_px += ROWS;
            int new_py = (r.py + r.vy * iteration) % COLS;
            if (new_py < 0) new_py += COLS;
            current_robots.push_back({new_px, new_py, r.vx, r.vy});
        }
        std::vector<int> quads = safety_value(current_robots);
        long long sf = std::accumulate(quads.begin(), quads.end(), 1LL, std::multiplies<long long>());
        if (sf < min_sf && sf > 0) {
            min_sf = sf;
            best_iteration = iteration;
        }
    }
    return best_iteration;
}

int main(int argc, char* argv[]) {
    // Determine input filename
    std::string filename;
    if (argc > 1) {
        filename = argv[1];
    } else {
        filename = "../data/day14.txt";
    }
    // Parse robots from file
    std::vector<Robot> robots = parse(filename);
    // Compute and print answers
    std::cout << "part1=" << part1(robots) << std::endl;
    std::cout << "part2=" << part2(robots) << std::endl;
    return 0;
} 