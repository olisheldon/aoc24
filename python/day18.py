import sys
import heapq

# ROWS, COLS = 7, 7
ROWS, COLS = 71, 71

# NUM_STEPS = 12
NUM_STEPS = 1024

NEIGHBOURS = ((-1, 0), (1, 0), (0, 1), (0, -1))

EMPTY = "."
WALL = "#"

def create_grid(num_steps):
    grid = [["." for _ in range(COLS)] for _ in range(ROWS)]
    coords = parse()
    for c, r in coords[:num_steps]:
        grid[r][c] = "#"
    return grid

def print_grid(grid):
    for row in grid:
        print("".join(row))
    print()
    
def print_history(grid, history):
    history = set(history)
    grid = grid.copy()
    for r, row in enumerate(grid):
        for c, elem in enumerate(row):
            if (r, c) in history:
                grid[r][c] = "O"
    print_grid(grid)
    
def min_path(num_steps):
    grid = create_grid(num_steps)
    visited = set()
        
    min_heap = [(0, 0, 0)] # (steps, r, c)
    while min_heap:
        steps, r, c = heapq.heappop(min_heap)
        if (r, c) == (ROWS - 1, COLS - 1):
            return steps
        if (
            r not in range(ROWS) or
            c not in range(COLS) or
            (r, c) in visited or
            grid[r][c] == WALL
        ):
            continue
        visited.add((r, c))
        
        for dr, dc in NEIGHBOURS:
            heapq.heappush(min_heap, (steps + 1, r + dr, c + dc))
    return -1
    
def part1():
    return min_path(NUM_STEPS)

def part2():
    num_fallen = 0
    while min_path(num_fallen) != -1:
        num_fallen += 1
    return ",".join(map(str, parse()[num_fallen - 1]))

def parse():
    with open(filename) as f:
        inp = f.read()
    return list(tuple(map(int, line.split(","))) for line in inp.split("\n"))

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day18.txt"

    print(part1())
    print(part2())
