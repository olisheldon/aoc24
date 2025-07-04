#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <map>

const int EMPTY = -1;

// Parse input: each character is a digit
std::vector<int> parse_input(const std::string& filename) {
    std::ifstream infile(filename);
    std::vector<int> disk_map;
    char ch;
    while (infile >> ch) {
        if (ch >= '0' && ch <= '9') disk_map.push_back(ch - '0');
    }
    return disk_map;
}

// Checksum function
long long checksum(const std::vector<int>& nums) {
    long long sum = 0;
    for (size_t i = 0; i < nums.size(); ++i) sum += 1LL * i * nums[i];
    return sum;
}

// Part 1: Expand and fill blanks as described
long long part1(const std::vector<int>& disk_map) {
    std::vector<int> expanded;
    for (size_t i = 0; i < disk_map.size(); ++i) {
        int count = disk_map[i];
        if (i % 2) {
            expanded.insert(expanded.end(), count, EMPTY);
        } else {
            expanded.insert(expanded.end(), count, i / 2);
        }
    }
    int l = 0, r = expanded.size() - 1;
    while (l < r) {
        if (expanded[l] != EMPTY) {
            ++l;
        } else if (expanded[r] == EMPTY) {
            --r;
        } else {
            expanded[l] = expanded[r];
            expanded[r] = EMPTY;
            ++l; --r;
        }
    }
    std::vector<int> filtered;
    for (int x : expanded) if (x != EMPTY) filtered.push_back(x);
    return checksum(filtered);
}

// Part 2: Simulate file and blank movement
long long part2(const std::vector<int>& disk_map) {
    std::map<int, std::pair<int, int>> files; // file_id -> (pos, size)
    std::vector<std::pair<int, int>> blanks; // (pos, size)
    int file_id = 0, position = 0;
    for (size_t i = 0; i < disk_map.size(); ++i) {
        int count = disk_map[i];
        if (i % 2 == 0) {
            files[file_id++] = {position, count};
        } else {
            blanks.emplace_back(position, count);
        }
        position += count;
    }
    for (int fid = file_id - 1; fid >= 0; --fid) {
        int pos = files[fid].first, size = files[fid].second;
        int best_pos = -1, best_blank_idx = -1;
        for (size_t i = 0; i < blanks.size(); ++i) {
            int blank_pos = blanks[i].first, blank_len = blanks[i].second;
            if (blank_pos >= pos) break;
            if (blank_len >= size) {
                best_pos = blank_pos;
                best_blank_idx = i;
                break;
            }
        }
        if (best_pos != -1) {
            files[fid] = {best_pos, size};
            if (size == blanks[best_blank_idx].second) {
                blanks.erase(blanks.begin() + best_blank_idx);
            } else {
                blanks[best_blank_idx] = {best_pos + size, blanks[best_blank_idx].second - size};
            }
        }
    }
    long long total = 0;
    for (const auto& [fid, p] : files) {
        int pos = p.first, size = p.second;
        for (int x = pos; x < pos + size; ++x) {
            total += 1LL * fid * x;
        }
    }
    return total;
}

int main(int argc, char* argv[]) {
    std::string filename = argc > 1 ? argv[1] : "../data/day9.txt";
    auto disk_map = parse_input(filename);
    std::cout << "part1=" << part1(disk_map) << std::endl;
    std::cout << "part2=" << part2(disk_map) << std::endl;
    return 0;
} 