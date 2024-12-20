import sys
from pathlib import Path
import heapq
from collections import Counter

cache = {}

START = "S"
END = "E"
WALL = "#"
TRACK = "."

TIME_SAVED = 2
INVALID_COORD = (-1, -1)

def min_path(grid, cheat_coord, start, end):
    
    ROWS, COLS = len(grid), len(grid[0])
    NEIGHBOURS = ((1, 0), (-1, 0), (0, 1), (0, -1))
    visited = set()
        
    min_heap = [(0, start[0], start[1], [])] # (steps, r, c, history)
    while min_heap:
        steps, r, c, history = heapq.heappop(min_heap)
        if (
            r not in range(ROWS) or
            c not in range(COLS) or
            (r, c) in visited or
            grid[r][c] == WALL or
            (steps and grid[r][c] == START)
        ):
            continue
        if (r, c) in cache:
            return cache[(r, c)]
        if (r, c) == end:
            for steps, r, c in history:
                cache[(r, c)] = steps
            return steps
        visited.add((r, c))
        history = history.copy()
        history.append((steps, r, c))
        
        for dr, dc in NEIGHBOURS:
            if (r + dr, c + dc) == cheat_coord:
                heapq.heappush(min_heap, (steps + 2, r + 2 * dr, c + 2 * dc, history))
            else:
                heapq.heappush(min_heap, (steps + 1, r + dr, c + dc, history))
    return -1

def part1():
    grid =  parse()
    ROWS, COLS = len(grid), len(grid[0])
    
    start = INVALID_COORD
    end = INVALID_COORD
    
    for r, row in enumerate(grid):
        for c, elem in enumerate(row):
            if elem == START:
                start = (r, c)
            elif elem == END:
                end = (r, c)
    assert start != INVALID_COORD and end != INVALID_COORD
    
    default_times = {}
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] in (TRACK, START):
                default_times[(r, c)] = min_path(grid, INVALID_COORD, (r, c), end)
    default_times[end] = 0
    print(f"{default_times=}")
    print(f"{default_times[start]=}")
    print(f"{default_times[end]=}")
    cheat_times = [min_path(grid, (r, c), start, end) for r in range(ROWS) for c in range(COLS)]
    print(default_times[start])
    print(cheat_times)
    times_in_range = list(filter(lambda x: x in range(default_times[start] - TIME_SAVED + 1), cheat_times))

    # counter = Counter(list(map(lambda x: default_time - x, filter(lambda x: x in range(default_time - TIME_SAVED + 1 ), cheat_times))))
    # for time_saved, count in sorted(counter.items()):
    #     print(f"There are {count} cheats that save {time_saved} picoseconds.")
    return len(times_in_range)
    
def part2():
    return "INCOMPLETE"

def parse():
    with open(filename) as f:
        inp = f.read()
    grid = []
    for line in inp.split("\n"):
        grid.append(list(line))
    return grid

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.test.txt"

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))
