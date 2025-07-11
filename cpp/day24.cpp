#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <string>
#include <algorithm>
#include <cctype>
#include <cassert>
#include <cstdint>

struct Node {
    std::string name;
    int value; // -1 means unset
    std::vector<std::tuple<Node*, Node*, std::string>> inputs; // (node1, node2, logic)
    Node(const std::string& n, int v = -1) : name(n), value(v) {}
    bool has_value() const { return value != -1; }
};

std::string filename;

// Helper: trim whitespace
std::string trim(const std::string& s) {
    size_t start = s.find_first_not_of(" \t\n\r");
    size_t end = s.find_last_not_of(" \t\n\r");
    return (start == std::string::npos) ? "" : s.substr(start, end - start + 1);
}

// Parse input file into initial values and connections
void parse(std::map<std::string, int>& init_values, std::vector<std::pair<std::vector<std::string>, std::string>>& connections) {
    std::ifstream fin(filename);
    std::string line, block1, block2, content;
    while (std::getline(fin, line)) content += line + "\n";
    size_t split = content.find("\n\n");
    block1 = content.substr(0, split);
    block2 = content.substr(split + 2);
    std::istringstream ss1(block1), ss2(block2);
    while (std::getline(ss1, line)) {
        if (trim(line).empty()) continue;
        size_t pos = line.find(": ");
        std::string gate = line.substr(0, pos);
        int value = std::stoi(line.substr(pos + 2));
        init_values[gate] = value;
    }
    while (std::getline(ss2, line)) {
        if (trim(line).empty()) continue;
        size_t pos = line.find(" -> ");
        std::string logic = line.substr(0, pos);
        std::string target = line.substr(pos + 4);
        std::istringstream lss(logic);
        std::vector<std::string> logic_parts;
        std::string part;
        while (lss >> part) logic_parts.push_back(part);
        connections.emplace_back(logic_parts, target);
    }
}

// Build nodes and wire up connections
std::map<std::string, Node*> create_nodes() {
    std::map<std::string, int> init_values;
    std::vector<std::pair<std::vector<std::string>, std::string>> connections;
    parse(init_values, connections);
    std::map<std::string, Node*> nodes;
    for (auto& [name, val] : init_values)
        nodes[name] = new Node(name, val);
    for (auto& [logic, target] : connections) {
        for (auto& node : logic) if (nodes.find(node) == nodes.end()) nodes[node] = new Node(node);
        if (nodes.find(target) == nodes.end()) nodes[target] = new Node(target);
    }
    for (auto& [logic, target] : connections) {
        nodes[target]->inputs.emplace_back(nodes[logic[0]], nodes[logic[2]], logic[1]);
    }
    return nodes;
}

// Recursively evaluate node values
void dfs(Node* u) {
    if (u->has_value()) return;
    for (auto& [n1, n2, logic] : u->inputs) {
        dfs(n1); dfs(n2);
        if (logic == "AND") u->value = n1->value & n2->value;
        else if (logic == "OR") u->value = n1->value | n2->value;
        else if (logic == "XOR") u->value = n1->value ^ n2->value;
        else { std::cerr << "Unknown logic: " << logic << std::endl; exit(1); }
    }
}

// Part 1: Evaluate circuit and compute binary output
int64_t part1() {
    auto nodes = create_nodes();
    for (auto& [_, node] : nodes) dfs(node);
    std::vector<Node*> z_nodes;
    for (auto& [_, node] : nodes) if (node->name.substr(0,1)=="z") z_nodes.push_back(node);
    std::sort(z_nodes.begin(), z_nodes.end(), [](Node* a, Node* b){ return a->name > b->name; });
    std::string bin_s;
    for (auto node : z_nodes) {
        // Check that node value is 0 or 1
        if (node->value != 0 && node->value != 1) {
            std::cerr << "Error: Node '" << node->name << "' has invalid value: " << node->value << std::endl;
            for (auto& [_, n] : nodes) delete n;
            return -1;
        }
        bin_s += std::to_string(node->value);
    }
    // Check for empty binary string
    if (bin_s.empty()) {
        std::cerr << "Error: No nodes with names starting with 'z' found.\n";
        for (auto& [_, n] : nodes) delete n;
        return -1;
    }
    int64_t result = -1;
    try {
        // Manual conversion to support long binary strings (std::stoi can't handle >32 bits)
        uint64_t val = 0;
        for (char c : bin_s) {
            val = (val << 1) | (c - '0');
        }
        result = static_cast<int64_t>(val); // Use int64_t to avoid overflow
    } catch (const std::exception& e) {
        std::cerr << "Error: Failed to convert binary string '" << bin_s << "' to integer: " << e.what() << std::endl;
        result = -1;
    }
    for (auto& [_, node] : nodes) delete node;
    return result;
}

// --- Part 2 helpers ---
std::string make_wire(const std::string& c, int num) {
    std::ostringstream oss; oss << c << (num<10?"0":"") << num;
    return oss.str();
}

// Helper to get gate info
void get_gate_info(Node* node, std::string& gate, std::string& x, std::string& y) {
    if (node->inputs.empty()) { gate=x=y=""; return; }
    auto& [n1, n2, g] = node->inputs[0];
    gate = g; x = n1->name; y = n2->name;
}

// Verification functions
bool verify_intermediate_xor(std::map<std::string, Node*>& nodes, Node* node, int num);
bool verify_carry_bit(std::map<std::string, Node*>& nodes, Node* node, int num);
bool verify_direct_carry(std::map<std::string, Node*>& nodes, Node* node, int num);
bool verify_recarry(std::map<std::string, Node*>& nodes, Node* node, int num);

bool verify_z(std::map<std::string, Node*>& nodes, Node* node, int num) {
    if (node->inputs.empty()) return false;
    std::string gate, x, y; get_gate_info(node, gate, x, y);
    if (gate != "XOR") return false;
    if (num == 0) return std::vector<std::string>{x,y} == std::vector<std::string>{"x00","y00"} || std::vector<std::string>{y,x} == std::vector<std::string>{"x00","y00"};
    return (verify_intermediate_xor(nodes, nodes[x], num) && verify_carry_bit(nodes, nodes[y], num)) ||
           (verify_intermediate_xor(nodes, nodes[y], num) && verify_carry_bit(nodes, nodes[x], num));
}
bool verify_intermediate_xor(std::map<std::string, Node*>& nodes, Node* node, int num) {
    if (node->inputs.empty()) return false;
    std::string gate, x, y; get_gate_info(node, gate, x, y);
    if (gate != "XOR") return false;
    return (std::vector<std::string>{x,y} == std::vector<std::string>{make_wire("x",num), make_wire("y",num)} ||
            std::vector<std::string>{y,x} == std::vector<std::string>{make_wire("x",num), make_wire("y",num)});
}
bool verify_direct_carry(std::map<std::string, Node*>& nodes, Node* node, int num) {
    if (node->inputs.empty()) return false;
    std::string gate, x, y; get_gate_info(node, gate, x, y);
    if (gate != "AND") return false;
    return (std::vector<std::string>{x,y} == std::vector<std::string>{make_wire("x",num), make_wire("y",num)} ||
            std::vector<std::string>{y,x} == std::vector<std::string>{make_wire("x",num), make_wire("y",num)});
}
bool verify_recarry(std::map<std::string, Node*>& nodes, Node* node, int num) {
    if (node->inputs.empty()) return false;
    std::string gate, x, y; get_gate_info(node, gate, x, y);
    if (gate != "AND") return false;
    return (verify_intermediate_xor(nodes, nodes[x], num) && verify_carry_bit(nodes, nodes[y], num)) ||
           (verify_intermediate_xor(nodes, nodes[y], num) && verify_carry_bit(nodes, nodes[x], num));
}
bool verify_carry_bit(std::map<std::string, Node*>& nodes, Node* node, int num) {
    if (node->inputs.empty()) return false;
    std::string gate, x, y; get_gate_info(node, gate, x, y);
    if (num == 1) return gate=="AND" && (std::vector<std::string>{x,y}==std::vector<std::string>{"x00","y00"}||std::vector<std::string>{y,x}==std::vector<std::string>{"x00","y00"});
    if (gate != "OR") return false;
    return (verify_direct_carry(nodes, nodes[x], num-1) && verify_recarry(nodes, nodes[y], num-1)) ||
           (verify_direct_carry(nodes, nodes[y], num-1) && verify_recarry(nodes, nodes[x], num-1));
}
bool verify(std::map<std::string, Node*>& nodes, int num) {
    return verify_z(nodes, nodes[make_wire("z", num)], num);
}
int progress(std::map<std::string, Node*>& nodes) {
    int i=0; while (verify(nodes, i)) ++i; return i;
}

// Part 2: Try swaps to maximize progress
std::string part2() {
    auto nodes = create_nodes();
    std::vector<std::string> swaps;
    for (int iter=0; iter<4; ++iter) {
        int baseline = progress(nodes);
        std::string x, y; bool found=false;
        for (auto& [nx, nodex] : nodes) {
            for (auto& [ny, nodey] : nodes) {
                if (nx==ny) continue;
                std::swap(nodex->inputs, nodey->inputs);
                if (progress(nodes) > baseline) { x=nx; y=ny; found=true; break; }
                std::swap(nodex->inputs, nodey->inputs);
            }
            if (found) break;
        }
        swaps.push_back(x); swaps.push_back(y);
    }
    std::sort(swaps.begin(), swaps.end());
    for (auto& [_, node] : nodes) delete node;
    std::string res;
    for (size_t i=0; i<swaps.size(); ++i) {
        res += swaps[i];
        if (i+1<swaps.size()) res += ",";
    }
    return res;
}

int main(int argc, char* argv[]) {
    filename = (argc > 1) ? argv[1] : "../data/day24.txt";
    std::cout << "part1=" << part1() << std::endl;
    std::cout << "part2=" << part2() << std::endl;
    return 0;
} 