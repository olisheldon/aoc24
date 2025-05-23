import sys
from pathlib import Path
import itertools

class Node:
    
    def __init__(self, name, init_value=None):
        self.name = name
        self.value = init_value
        self.inputs = [] # (node1, node2, logic)
    
    def __repr__(self):
        return f"Node(name={self.name}, value={self.value}, inputs={self.inputs})"
    
    @property
    def has_value(self):
        return self.value is not None

def create_nodes():
    init_values, connections = parse()
    
    nodes = {}
    for init_node_name, value in init_values.items():
        nodes[init_node_name] = Node(init_node_name, value)
    for (i_node_1, gate, i_node_2), target_node in connections:
        for node in (i_node_1, i_node_2, target_node):
            if node not in nodes:
                nodes[node] = Node(node)
    for (i_node_1, gate, i_node_2), target_node in connections:
        nodes[target_node].inputs.append((nodes[i_node_1], nodes[i_node_2], gate))
    return nodes

def part1():
    
    nodes = create_nodes()
    
    def dfs(u: Node):
        if u.has_value:
            return
        
        for n1, n2, logic in u.inputs:
            dfs(n1)
            dfs(n2)
            match logic:
                case "AND":
                    u.value = n1.value & n2.value
                case "OR":
                    u.value = n1.value | n2.value
                case "XOR":
                    u.value = n1.value ^ n2.value
                case _:
                    raise RuntimeError()
    
    for node in nodes.values():
        dfs(node)
    
    bin_s = "".join((str(node.value) for node in sorted(nodes.values(), key=lambda x: x.name, reverse=True) if node.name.startswith("z")))
    return int(bin_s, base=2)

def part2():
    nodes = create_nodes()
    
    def make_wire(char, num):
        return char + str(num).rjust(2, "0")
    
    def get_gate_info(node: Node):
        if not node.inputs:
            return None, None, None
        n1, n2, gate = node.inputs[0]
        return gate, n1.name, n2.name

    def verify_z(node: Node, num):
        if not node.inputs: return False
        gate, x, y = get_gate_info(node)
        if gate != "XOR": return False
        if num == 0: return sorted([x, y]) == ["x00", "y00"]
        return verify_intermediate_xor(nodes[x], num) and verify_carry_bit(nodes[y], num) or \
               verify_intermediate_xor(nodes[y], num) and verify_carry_bit(nodes[x], num)

    def verify_intermediate_xor(node: Node, num):
        if not node.inputs: return False
        gate, x, y = get_gate_info(node)
        if gate != "XOR": return False
        return sorted([x, y]) == [make_wire("x", num), make_wire("y", num)]

    def verify_carry_bit(node: Node, num):
        if not node.inputs: return False
        gate, x, y = get_gate_info(node)
        if num == 1:
            if gate != "AND": return False
            return sorted([x, y]) == ["x00", "y00"]
        if gate != "OR": return False
        return verify_direct_carry(nodes[x], num - 1) and verify_recarry(nodes[y], num - 1) or \
               verify_direct_carry(nodes[y], num - 1) and verify_recarry(nodes[x], num - 1)

    def verify_direct_carry(node: Node, num):
        if not node.inputs: return False
        gate, x, y = get_gate_info(node)
        if gate != "AND": return False
        return sorted([x, y]) == [make_wire("x", num), make_wire("y", num)]

    def verify_recarry(node: Node, num):
        if not node.inputs: return False
        gate, x, y = get_gate_info(node)
        if gate != "AND": return False
        return verify_intermediate_xor(nodes[x], num) and verify_carry_bit(nodes[y], num) or \
               verify_intermediate_xor(nodes[y], num) and verify_carry_bit(nodes[x], num)

    def verify(num):
        return verify_z(nodes[make_wire("z", num)], num)

    def progress():
        i = 0
        while True:
            if not verify(i): break
            i += 1
        return i

    swaps = []
    for _ in range(4):
        baseline = progress()
        for x in nodes:
            for y in nodes:
                if x == y: continue
                # Swap the inputs of the nodes
                nodes[x].inputs, nodes[y].inputs = nodes[y].inputs, nodes[x].inputs
                if progress() > baseline:
                    break
                # Swap back if no improvement
                nodes[x].inputs, nodes[y].inputs = nodes[y].inputs, nodes[x].inputs
            else:
                continue
            break
        swaps += [x, y]

    return ",".join(sorted(swaps))

def parse():
    with open(filename) as f:
        inp = f.read()
    init_values_s, connections_s = inp.split("\n\n")
    
    init_values = {}
    for init_value in init_values_s.split("\n"):
        gate, value = init_value.split(": ")
        init_values[gate] = int(value)

    connections = []
    for connection in connections_s.split("\n"):
        logic, target = connection.split(" -> ")
        connections.append((logic.split(), target))
        
    return init_values, connections

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))
