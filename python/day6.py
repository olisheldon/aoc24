import sys
from itertools import cycle

def part1():
    ROWS, COLS = len(grid), len(grid[0])
    
    initial_pos = (-1, -1)
    
    for r, row in enumerate(grid):
        for c, elem in enumerate(row):
            if elem == "^":
                initial_pos = (r, c)
                break
    
    rotations = cycle([(-1, 0), (0, 1), (1, 0), (0, -1)])
    
    visited = set()
    dr, dc = next(rotations)
    assert initial_pos != (-1, -1)
    r, c = initial_pos
    while r + dr in range(ROWS) and c + dc in range(COLS):
        visited.add((r, c))
        if grid[r + dr][c + dc] == "#":
            dr, dc = next(rotations)
        else:
            r, c = r + dr, c + dc
    return len(visited) + 1

def sim(initial_pos, grid):
    ROWS, COLS = len(grid), len(grid[0])
    
    rotations = cycle([(-1, 0), (0, 1), (1, 0), (0, -1)])
    
    visited_states: set[tuple[int, int, int, int]] = set() # tuple[r, c, dr, dc]
    dr, dc = next(rotations)
    assert initial_pos != (-1, -1)
    r, c = initial_pos
    while r + dr in range(ROWS) and c + dc in range(COLS):
        if (r, c, dr, dc) in visited_states:
            return True
        visited_states.add((r, c, dr, dc))
        if grid[r + dr][c + dc] == "#":
            dr, dc = next(rotations)
        else:
            r, c = r + dr, c + dc
    return False

def part2():
    
    potential_obstructions = []
    initial_pos = (-1, -1)
    
    for r, row in enumerate(grid):
        for c, elem in enumerate(row):
            if elem == "^":
                initial_pos = (r, c)
            elif elem == ".":
                potential_obstructions.append((r, c))
    assert initial_pos != (-1, -1)
    
    res = 0
    for r, c in potential_obstructions:
        grid[r][c] = "#"
        res += sim(initial_pos, grid)
        grid[r][c] = "."
    return res

def parse():
    with open(filename) as f:
        inp = f.read()
    grid = inp.split("\n")
    return list(map(list, grid))

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day6.txt"
    grid = parse()
    
    print(f"{part1()=}")
    print(f"{part2()=}")