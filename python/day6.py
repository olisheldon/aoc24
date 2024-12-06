import sys
from collections import defaultdict, deque
from itertools import cycle



def part1():
    ROWS, COLS = len(grid), len(grid[0])
    
    obstructions = set()
    initial_pos = (-1, -1)
    
    for r, row in enumerate(grid):
        for c, elem in enumerate(row):
            if elem == "#":
                obstructions.add((r, c))
            elif elem == "^":
                initial_pos = (r, c)
    
    rotations = cycle([(-1, 0), (0, 1), (1, 0), (0, -1)])
    
    visited = set()
    dr, dc = next(rotations)
    assert initial_pos != (-1, -1)
    r, c = initial_pos
    while r + dr in range(ROWS) and c + dc in range(COLS):
        visited.add((r, c))
        if (r + dr, c + dc) in obstructions:
            dr, dc = next(rotations)
        else:
            r, c = r + dr, c + dc
    return len(visited) + 1

def part2():
    pass

def parse():
    with open(filename) as f:
        inp = f.read()
    grid = inp.split("\n")
    return grid

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day6.txt"
    grid = parse()
    print(grid)
    
    print(f"{part1()=}")
    print(f"{part2()=}")