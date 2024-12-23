import sys
from pathlib import Path
from collections import defaultdict
from itertools import chain

def part1():
    connections = parse()
    computers = set(chain(*connections))
    
    adj = defaultdict(list)
    for u, v in connections:
        adj[u].append(v)
        adj[v].append(u)
    
    def dfs(u, prev=None, history=0):
        if u in visited:
            return history == 3
        visited.add(u)
        
        for v in adj[u]:
            if v != prev and dfs(v, u, history + 1):
                return True
        return False

    three_computers = 0
    for u in computers:
        visited = set()
        if dfs(u):
            three_computers += 1
    return three_computers
            
def part2():
    return "INCOMPLETE"

def parse():
    with open(filename) as f:
        inp = f.read()
    lines = inp.split("\n")
    return [tuple(line.split("-")) for line in lines]

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.test.txt"

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))
