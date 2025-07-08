#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
#include <map>
#include <set>
#include <string>
#include <algorithm>
#include <tuple>
#include <functional>
#include <cctype> // For isdigit

// Keypad definitions
const std::vector<std::vector<std::string>> NUM_KEYPAD = {
    {"7", "8", "9"},
    {"4", "5", "6"},
    {"1", "2", "3"},
    {"",  "0", "A"}
};
const std::vector<std::vector<std::string>> DIR_KEYPAD = {
    {"",  "^", "A"},
    {"<", "v", ">"}
};
const std::vector<std::tuple<int,int,std::string>> NEIGHBOURS = {
    {1, 0, "v"}, {-1, 0, "^"}, {0, 1, ">"}, {0, -1, "<"}
};

// Helper to get positions of each button
std::map<std::string, std::pair<int,int>> get_positions(const std::vector<std::vector<std::string>>& keypad) {
    std::map<std::string, std::pair<int,int>> pos;
    for (int r = 0; r < keypad.size(); ++r) {
        for (int c = 0; c < keypad[r].size(); ++c) {
            if (!keypad[r][c].empty())
                pos[keypad[r][c]] = {r, c};
        }
    }
    return pos;
}

// Compute all shortest sequences between every button pair
std::map<std::pair<std::string,std::string>, std::vector<std::string>> compute_seqs(const std::vector<std::vector<std::string>>& keypad) {
    std::map<std::string, std::pair<int,int>> pos = get_positions(keypad);
    std::map<std::pair<std::string,std::string>, std::vector<std::string>> seqs;
    for (const auto& u : pos) {
        for (const auto& v : pos) {
            if (u.first == v.first) {
                seqs[{u.first, v.first}] = {"A"};
                continue;
            }
            std::vector<std::string> possibilities;
            std::queue<std::pair<std::pair<int,int>, std::string>> q;
            q.push({u.second, ""});
            int optimal = -1;
            while (!q.empty()) {
                int qsize = q.size();
                bool found = false;
                for (int i = 0; i < qsize; ++i) {
                    auto [rc, moves] = q.front(); q.pop();
                    int r = rc.first, c = rc.second;
                    for (const auto& [dr, dc, m] : NEIGHBOURS) {
                        int nr = r + dr, nc = c + dc;
                        if (nr < 0 || nr >= keypad.size() || nc < 0 || nc >= keypad[nr].size() || keypad[nr][nc].empty())
                            continue;
                        if (keypad[nr][nc] == v.first) {
                            if (optimal == -1) optimal = moves.size() + 1;
                            if ((int)moves.size() + 1 == optimal) {
                                possibilities.push_back(moves + m + "A");
                                found = true;
                            }
                        } else if (optimal == -1) {
                            q.push({{nr, nc}, moves + m});
                        }
                    }
                }
                if (found) break; // Only process the first level where a solution is found
            }
            seqs[{u.first, v.first}] = possibilities;
        }
    }
    return seqs;
}

// Generate all possible sequences for a code
std::vector<std::string> solve(const std::string& code, const std::map<std::pair<std::string,std::string>, std::vector<std::string>>& seqs) {
    std::vector<std::vector<std::string>> options;
    std::string prev = "A";
    for (char ch : code) {
        std::string curr(1, ch);
        options.push_back(seqs.at({prev, curr}));
        prev = curr;
    }
    // Cartesian product
    std::vector<std::string> result = {""};
    for (const auto& opt : options) {
        std::vector<std::string> temp;
        for (const auto& prefix : result)
            for (const auto& s : opt)
                temp.push_back(prefix + s);
        result.swap(temp);
    }
    return result;
}

// Parse input file
std::vector<std::string> parse(const std::string& filename) {
    std::ifstream in(filename);
    std::vector<std::string> codes;
    std::string line;
    while (std::getline(in, line)) {
        if (!line.empty()) codes.push_back(line);
    }
    return codes;
}

// Part 1 logic
long long part1(const std::vector<std::string>& codes) {
    auto num_seqs = compute_seqs(NUM_KEYPAD);
    long long total = 0;
    for (const auto& code : codes) {
        auto robot1 = solve(code, num_seqs);
        std::vector<std::string> next = robot1;
        for (int i = 0; i < 2; ++i) {
            std::vector<std::string> possible_next;
            auto dir_seqs = compute_seqs(DIR_KEYPAD);
            for (const auto& seq : next) {
                auto solved = solve(seq, dir_seqs);
                possible_next.insert(possible_next.end(), solved.begin(), solved.end());
            }
            // Correct filtering: only keep minimum-length sequences
            size_t minlen = std::min_element(possible_next.begin(), possible_next.end(), [](const std::string& a, const std::string& b){return a.size() < b.size();})->size();
            std::vector<std::string> filtered;
            for (const auto& s : possible_next)
                if (s.size() == minlen)
                    filtered.push_back(s);
            next = filtered;
        }
        int length = next[0].size();
        // Extract the number part from the code (all digits before the last character)
        std::string numpart;
        for (char ch : code) if (isdigit(ch)) numpart += ch;
        long long factor = std::stoll(numpart);
        long long complexity = length * factor;
        total += complexity;
    }
    return total;
}

// Part 2 logic (with memoization)
long long part2(const std::vector<std::string>& codes) {
    auto dir_seqs = compute_seqs(DIR_KEYPAD);
    std::map<std::pair<std::string,std::string>, int> dir_lens;
    for (const auto& kv : dir_seqs)
        dir_lens[kv.first] = kv.second[0].size();
    auto num_seqs = compute_seqs(NUM_KEYPAD);
    // Memoization cache
    std::map<std::pair<std::string,int>, long long> cache;
    std::function<long long(const std::string&, int)> compute_length = [&](const std::string& seq, int depth) -> long long {
        if (depth == 1) {
            long long sum = 0;
            std::string prev = "A";
            for (char ch : seq) {
                std::string curr(1, ch);
                sum += dir_lens[{prev, curr}];
                prev = curr;
            }
            return sum;
        }
        auto key = std::make_pair(seq, depth);
        if (cache.count(key)) return cache[key];
        long long length = 0;
        std::string prev = "A";
        for (char ch : seq) {
            std::string curr(1, ch);
            long long minlen = 1e18;
            for (const auto& subseq : dir_seqs[{prev, curr}]) {
                minlen = std::min(minlen, compute_length(subseq, depth-1));
            }
            length += minlen;
            prev = curr;
        }
        return cache[key] = length;
    };
    long long total = 0;
    for (const auto& code : codes) {
        auto inputs = solve(code, num_seqs);
        long long optimal_length = 1e18;
        for (const auto& seq : inputs)
            optimal_length = std::min(optimal_length, compute_length(seq, 25));
        // Extract the number part from the code (all digits before the last character)
        std::string numpart;
        for (char ch : code) if (isdigit(ch)) numpart += ch;
        long long factor = std::stoll(numpart);
        total += optimal_length * factor;
    }
    return total;
}

int main(int argc, char* argv[]) {
    std::string filename = (argc > 1) ? argv[1] : "../data/day21.txt";
    auto codes = parse(filename);
    std::cout << "part1=" << part1(codes) << std::endl;
    std::cout << "part2=" << part2(codes) << std::endl;
    return 0;
} 