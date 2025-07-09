#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <set>
#include <map>
#include <algorithm>
#include <iterator>

using Edge = std::pair<std::string, std::string>;
using AdjList = std::map<std::string, std::set<std::string>>;

// Parse the input file into a vector of edges
std::vector<Edge> parse(const std::string& filename) {
    std::vector<Edge> connections;
    std::ifstream infile(filename);
    std::string line;
    while (std::getline(infile, line)) {
        if (line.empty()) continue;
        size_t dash = line.find('-');
        if (dash == std::string::npos) continue;
        std::string u = line.substr(0, dash);
        std::string v = line.substr(dash + 1);
        connections.emplace_back(u, v);
    }
    return connections;
}

// Part 1: Count unique triangles containing a node starting with 't'
int part1(const std::vector<Edge>& connections) {
    std::set<std::string> computers;
    AdjList adj;
    for (const auto& [u, v] : connections) {
        computers.insert(u);
        computers.insert(v);
        adj[u].insert(v);
        adj[v].insert(u);
    }
    std::set<std::set<std::string>> seen;
    for (const auto& first : computers) {
        for (const auto& second : adj[first]) {
            for (const auto& third : adj[second]) {
                std::set<std::string> triangle = {first, second, third};
                if (triangle.size() != 3) continue;
                // Check if all pairs are connected
                if (adj[second].count(first) && adj[third].count(first) && adj[third].count(second)) {
                    seen.insert(triangle);
                }
            }
        }
    }
    // Count triangles containing a node starting with 't'
    int count = 0;
    for (const auto& tri : seen) {
        for (const auto& node : tri) {
            if (!node.empty() && node[0] == 't') {
                ++count;
                break;
            }
        }
    }
    return count;
}

// Part 2: Find the largest clique (fully connected set)
void dfs(const std::string& u, std::set<std::string> required, const AdjList& adj, std::set<std::vector<std::string>>& sets) {
    std::vector<std::string> key(required.begin(), required.end());
    std::sort(key.begin(), key.end());
    if (sets.count(key)) return;
    sets.insert(key);
    for (const auto& v : adj.at(u)) {
        if (required.count(v)) continue;
        bool all_connected = true;
        for (const auto& req : required) {
            if (!adj.at(req).count(v)) {
                all_connected = false;
                break;
            }
        }
        if (all_connected) {
            std::set<std::string> next_required = required;
            next_required.insert(v);
            dfs(v, next_required, adj, sets);
        }
    }
}

std::string part2(const std::vector<Edge>& connections) {
    std::set<std::string> computers;
    AdjList adj;
    for (const auto& [u, v] : connections) {
        computers.insert(u);
        computers.insert(v);
        adj[u].insert(v);
        adj[v].insert(u);
    }
    std::set<std::vector<std::string>> sets;
    for (const auto& computer : computers) {
        dfs(computer, {computer}, adj, sets);
    }
    // Find the largest clique
    std::vector<std::string> largest;
    for (const auto& clique : sets) {
        if (clique.size() > largest.size()) largest = clique;
    }
    std::sort(largest.begin(), largest.end());
    // Join with commas
    std::ostringstream oss;
    for (size_t i = 0; i < largest.size(); ++i) {
        if (i > 0) oss << ",";
        oss << largest[i];
    }
    return oss.str();
}

int main(int argc, char* argv[]) {
    std::string filename;
    if (argc > 1) {
        filename = argv[1];
    } else {
        filename = "../data/day23.txt";
    }
    auto connections = parse(filename);
    std::cout << "part1=" << part1(connections) << std::endl;
    std::cout << "part2=" << part2(connections) << std::endl;
    return 0;
} 