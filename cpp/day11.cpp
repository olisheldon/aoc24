#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>

// Linked list node for part1
struct Node {
    long long val; // Use long long to prevent overflow
    Node* next;
    Node(long long v) : val(v), next(nullptr) {}
};

// Create linked list from vector
Node* create_stones(const std::vector<long long>& stones) {
    Node dummy(0);
    Node* curr = &dummy;
    for (long long stone : stones) {
        curr->next = new Node(stone);
        curr = curr->next;
    }
    return dummy.next;
}

// Apply rules to linked list for one step
Node* blink_linked_list(Node* head) {
    Node* curr = head;
    while (curr) {
        std::string curr_val_str = std::to_string(curr->val);
        if (curr->val == 0) {
            curr->val = 1;
        } else if (curr_val_str.size() % 2 == 0) {
            int mid = curr_val_str.size() / 2;
            long long left = std::stoll(curr_val_str.substr(0, mid));
            long long right = std::stoll(curr_val_str.substr(mid));
            Node* old_next = curr->next;
            curr->val = left;
            curr->next = new Node(right);
            curr->next->next = old_next;
            curr = curr->next;
        } else {
            curr->val *= 2024;
        }
        curr = curr->next;
    }
    return head;
}

// Count nodes in linked list
int count_nodes(Node* head) {
    int count = 0;
    while (head) {
        ++count;
        head = head->next;
    }
    return count;
}

// Part 1: Linked list simulation for 25 steps
int part1(const std::vector<long long>& stones) {
    Node* head = create_stones(stones);
    for (int i = 0; i < 25; ++i) {
        head = blink_linked_list(head);
    }
    int result = count_nodes(head);
    // Free memory
    while (head) {
        Node* tmp = head;
        head = head->next;
        delete tmp;
    }
    return result;
}

// Part 2: Counter-based simulation for 75 steps
long long part2(const std::vector<long long>& stones) {
    std::unordered_map<long long, long long> tally;
    for (long long stone : stones) tally[stone]++;
    for (int step = 0; step < 75; ++step) {
        std::unordered_map<long long, long long> new_tally;
        for (const auto& [num, count] : tally) {
            if (num == 0) {
                new_tally[1] += count;
            } else {
                std::string num_str = std::to_string(num);
                if (num_str.size() % 2 == 0) {
                    int mid = num_str.size() / 2;
                    long long left = std::stoll(num_str.substr(0, mid));
                    long long right = std::stoll(num_str.substr(mid));
                    new_tally[left] += count;
                    new_tally[right] += count;
                } else {
                    new_tally[num * 2024] += count;
                }
            }
        }
        tally = std::move(new_tally);
    }
    long long total = 0;
    for (const auto& [num, count] : tally) total += count;
    return total;
}

// Parse input: space-separated integers, use long long to prevent overflow
std::vector<long long> parse_input(const std::string& filename) {
    std::ifstream infile(filename);
    std::vector<long long> stones;
    long long x;
    while (infile >> x) stones.push_back(x);
    return stones;
}

int main(int argc, char* argv[]) {
    std::string filename = argc > 1 ? argv[1] : "../data/day11.txt";
    auto stones = parse_input(filename);
    std::cout << "part1=" << part1(stones) << std::endl;
    std::cout << "part2=" << part2(stones) << std::endl;
    return 0;
} 