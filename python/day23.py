import sys
from pathlib import Path
from collections import defaultdict
from itertools import chain

def part1():
    connections = parse()
    computers = set(chain(*connections))
    
    adj = defaultdict(set)
    for u, v in connections:
        adj[u].add(v)
        adj[v].add(u)

    seen = set()
    for first_computer in computers:
        for second_computer in adj[first_computer]:
            for third_computer in adj[second_computer]:
                three_computers = frozenset([first_computer, second_computer, third_computer])
                if len(three_computers) != 3:
                    continue
                if (
                    first_computer in adj[second_computer] and
                    first_computer in adj[third_computer] and
                    second_computer in adj[third_computer]
                ):
                    seen.add(three_computers)
                    
    def contains_element_starting_with_t(iter):
        return any(element.startswith('t') for element in iter)
    return len(list(filter(lambda x: contains_element_starting_with_t(x), seen)))

def part2():
    return "INCOMPLETE"

def parse():
    with open(filename) as f:
        inp = f.read()
    lines = inp.split("\n")
    return [tuple(line.split("-")) for line in lines]

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))
