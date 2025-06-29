#include <iostream>
#include <fstream>
#include <vector>
#include <tuple>
#include <sstream>
#include <algorithm>
#include <unordered_map>

std::vector<std::tuple<int, int>> parse(const std::string& filename) {
    
    std::ifstream file { filename };
    if (!file.is_open()) {
        std::cerr << "Could not open the file!" << std::endl;
        exit(1);
    }

    std::vector<std::tuple<int, int>> data;
    std::string line;

    while (std::getline(file, line)) {
        std::istringstream iss(line);
        int a, b;
        if (iss >> a >> b) {
            data.emplace_back(a, b);
        }
    }

    file.close();
    return data;
}

int part1(const std::vector<std::tuple<int, int>> &data) {
    std::vector<int> left{};
    std::vector<int> right{};

    for (const auto& t : data) {
        left.push_back(std::get<0>(t));
        right.push_back(std::get<1>(t));
    }

    // min heaps
    std::make_heap(left.begin(), left.end(), std::greater<>{});
    std::make_heap(right.begin(), right.end(), std::greater<>{});

    int res = 0;
    while (left.size() != 0 && right.size() != 0) {
        std::pop_heap(left.begin(), left.end(), std::greater<>{});
        std::pop_heap(right.begin(), right.end(), std::greater<>{});
        res += std::abs(left.back() - right.back());
        left.pop_back();
        right.pop_back();
    }
    return res;
}

int part2(const std::vector<std::tuple<int, int>> &data) {
    std::vector<int> left{};
    std::unordered_map<int, int> right{}; // counter, <val, freq>

    for (const auto& t : data) {
        left.push_back(std::get<0>(t));
        if (right.find(std::get<1>(t)) == right.cend()) {
            right[std::get<1>(t)] = 0;
        }
        right[std::get<1>(t)]++;
    }

    int res = 0;
    for (const auto& l : left) {
        res += l * right[l];
    }

    return res;
}

int main(int argc, char *argv[]) {
    
    std::string filename = argc > 1 ? argv[1] : "../../data/day1.txt";
    auto data = parse(filename);

    std::cout << "part1=" << part1(data) << std::endl;
    std::cout << "part2=" << part2(data) << std::endl;

    return 0;
}
