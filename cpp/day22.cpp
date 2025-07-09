#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <unordered_map>
#include <algorithm>
#include <iterator>
#include <functional>

// This function mixes the secret number with a mixer using XOR
long long mix(long long secret_number, long long mixer) {
    return secret_number ^ mixer;
}

// This function prunes the secret number to fit within 24 bits
long long prune(long long secret_number) {
    return secret_number % 16777216LL;
}

// This function evolves the secret number through a deterministic process
long long evolve(long long secret_number) {
    secret_number = mix(secret_number, secret_number * 64LL);
    secret_number = prune(secret_number);
    // Python's int(secret_number / 32) is floor division
    long long div = secret_number / 32LL;
    if ((secret_number < 0) != (32LL < 0) && secret_number % 32LL != 0) div -= 1;
    secret_number = mix(secret_number, div);
    secret_number = prune(secret_number);
    secret_number = mix(secret_number, secret_number * 2048LL);
    return prune(secret_number);
}

// Parse the input file into a vector of long long integers
std::vector<long long> parse(const std::string& filename) {
    std::ifstream infile(filename);
    std::vector<long long> numbers;
    std::string line;
    while (std::getline(infile, line)) {
        if (!line.empty()) {
            numbers.push_back(std::stoll(line));
        }
    }
    return numbers;
}

// Custom hash function for std::vector<long long>
struct VectorHash {
    std::size_t operator()(const std::vector<long long>& v) const {
        std::size_t hash = v.size();
        for (long long x : v) {
            hash ^= std::hash<long long>{}(x) + 0x9e3779b9 + (hash << 6) + (hash >> 2);
        }
        return hash;
    }
};

// Part 1: Evolve each secret number 2000 times and sum the results
long long part1(const std::vector<long long>& secret_numbers) {
    long long res = 0;
    for (long long secret_number : secret_numbers) {
        for (int i = 0; i < 2000; ++i) {
            secret_number = evolve(secret_number);
        }
        res += secret_number;
    }
    return res;
}

// Part 2: Analyze price changes and find the most common 4-diff pattern
long long part2(const std::vector<long long>& secret_numbers) {
    std::vector<std::unordered_map<std::vector<long long>, long long, VectorHash>> all_price_changes_to_prof;
    for (long long secret_number : secret_numbers) {
        std::vector<long long> prices;
        std::vector<long long> price_differences;
        for (int i = 0; i < 2000; ++i) {
            // Get the last digit of the secret number as the price
            prices.push_back(std::llabs(secret_number) % 10LL);
            secret_number = evolve(secret_number);
        }
        for (size_t i = 0; i + 1 < prices.size(); ++i) {
            price_differences.push_back(prices[i + 1] - prices[i]);
        }
        std::unordered_map<std::vector<long long>, long long, VectorHash> price_changes_to_prof;
        for (size_t i = 0; i + 4 < prices.size(); ++i) {
            std::vector<long long> price_changes(price_differences.begin() + i, price_differences.begin() + i + 4);
            if (price_changes_to_prof.count(price_changes)) continue;
            price_changes_to_prof[price_changes] = prices[i + 4];
        }
        all_price_changes_to_prof.push_back(price_changes_to_prof);
    }
    // Sum profit values for each price change pattern
    std::unordered_map<std::vector<long long>, long long, VectorHash> counter;
    for (const auto& p : all_price_changes_to_prof) {
        for (const auto& kv : p) {
            counter[kv.first] += kv.second;
        }
    }
    // Find the pattern with maximum total profit
    long long max_profit = 0;
    std::vector<long long> max_pattern;
    for (const auto& kv : counter) {
        if (kv.second > max_profit) {
            max_profit = kv.second;
            max_pattern = kv.first;
        }
    }
    // Return the maximum total profit
    return max_profit;
}

int main(int argc, char* argv[]) {
    // Determine input filename
    std::string filename;
    if (argc > 1) {
        filename = argv[1];
    } else {
        filename = "../data/day22.txt";
    }
    std::vector<long long> secret_numbers = parse(filename);
    std::cout << "part1=" << part1(secret_numbers) << std::endl;
    std::cout << "part2=" << part2(secret_numbers) << std::endl;
    return 0;
} 