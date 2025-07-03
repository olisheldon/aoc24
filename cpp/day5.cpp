#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <set>
#include <map>
#include <algorithm>

// Parse input file into ordering rules and pages
void parse_input(const std::string& filename, std::vector<std::pair<int, int>>& rules, std::vector<std::vector<int>>& pages) {
    std::ifstream infile(filename);
    std::string line;
    bool reading_rules = true;
    while (std::getline(infile, line)) {
        if (line.empty()) {
            reading_rules = false;
            continue;
        }
        if (reading_rules) {
            size_t bar = line.find('|');
            int x = std::stoi(line.substr(0, bar));
            int y = std::stoi(line.substr(bar + 1));
            rules.emplace_back(x, y);
        } else {
            std::vector<int> page;
            std::stringstream ss(line);
            std::string num;
            while (std::getline(ss, num, ',')) {
                page.push_back(std::stoi(num));
            }
            pages.push_back(page);
        }
    }
}

// Check if a page is valid according to k_before_v
bool valid(const std::vector<int>& page, const std::map<int, std::set<int>>& k_before_v) {
    for (size_t i = 0; i < page.size(); ++i) {
        for (size_t j = i + 1; j < page.size(); ++j) {
            if (k_before_v.count(page[j]) && k_before_v.at(page[j]).count(page[i]) == 0) {
                return false;
            }
        }
    }
    return true;
}

int part1(const std::vector<std::pair<int, int>>& rules, const std::vector<std::vector<int>>& pages) {
    std::map<int, std::set<int>> k_before_v;
    for (const auto& rule : rules) {
        k_before_v[rule.second].insert(rule.first);
    }
    int res = 0;
    for (const auto& page : pages) {
        if (valid(page, k_before_v)) {
            res += page[page.size() / 2];
        }
    }
    return res;
}

// For part2, sort invalid pages using the rules
int part2(const std::vector<std::pair<int, int>>& rules, const std::vector<std::vector<int>>& pages) {
    std::map<std::pair<int, int>, int> cache;
    for (const auto& rule : rules) {
        cache[{rule.first, rule.second}] = -1;
        cache[{rule.second, rule.first}] = 1;
    }
    auto cmp = [&cache](int x, int y) {
        auto it = cache.find({x, y});
        if (it != cache.end()) return it->second;
        return 0;
    };
    int res = 0;
    for (auto page : pages) {
        // Check if already ordered
        bool ordered = true;
        for (size_t i = 0; i < page.size(); ++i) {
            for (size_t j = i + 1; j < page.size(); ++j) {
                if (cache.find({page[i], page[j]}) != cache.end() && cache[{page[i], page[j]}] == 1) {
                    ordered = false;
                    break;
                }
            }
            if (!ordered) break;
        }
        if (ordered) continue;
        // Sort using cmp
        std::sort(page.begin(), page.end(), [&cmp](int a, int b) { return cmp(a, b) < 0; });
        res += page[page.size() / 2];
    }
    return res;
}

int main(int argc, char* argv[]) {
    std::string filename = argc > 1 ? argv[1] : "../data/day5.txt";
    std::vector<std::pair<int, int>> rules;
    std::vector<std::vector<int>> pages;
    parse_input(filename, rules, pages);
    std::cout << "part1=" << part1(rules, pages) << std::endl;
    std::cout << "part2=" << part2(rules, pages) << std::endl;
    return 0;
} 