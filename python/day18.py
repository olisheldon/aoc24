import sys
from collections import deque

ROWS, COLS = 7, 7
# ROWS, COLS = 71, 71

NUM_STEPS = 12
# NUM_STEPS = 1024

NEIGHBOURS = ((-1, 0), (1, 0), (0, 1), (0, -1))

EMPTY = "."
WALL = "#"

def create_grid():
    grid = [["." for _ in range(COLS)] for _ in range(ROWS)]
    coords = parse()
    for c, r in coords[:NUM_STEPS]:
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
    
    
def part1():
    grid = create_grid()
    print_grid(grid)
        
    q = deque()
    q.append((0, 0, 0, set()))
    while q:
        for _ in range(len(q)):
            r, c, steps, visited = q.popleft()
            if (
                r not in range(ROWS) or
                c not in range(COLS) or
                (r, c) in visited or
                grid[r][c] == WALL
            ):
                continue
            if (r, c) == (ROWS - 1, COLS - 1):
                print_history(grid, visited & set((r, c)))
                return steps
            
            for dr, dc in NEIGHBOURS:
                q.appendleft((r + dr, c + dc, steps + 1, visited & set((r, c))))
    return -1
        
    # min_heap = [(0, 0, 0)] # (steps, r, c)
    # while min_heap:
    #     steps, r, c = heapq.heappop(min_heap)
    #     if (r, c) == (ROWS - 1, COLS - 1):
    #         return steps
    #     if (
    #         r not in range(ROWS) or
    #         c not in range(COLS) or
    #         # (r, c) in visited or
    #         grid[r][c] == WALL
    #     ):
    #         continue
    #     # visited.add((r, c))
        
    #     for dr, dc in NEIGHBOURS:
    #         heapq.heappush(min_heap, (steps + 1, )))

def part2():
    pass

def parse():
    with open(filename) as f:
        inp = f.read()
    return list(tuple(map(int, line.split(","))) for line in inp.split("\n"))

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day18.test.txt"

    print(part1())
    print(part2())
