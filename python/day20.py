import sys
from pathlib import Path
import heapq
from collections import Counter

PRINT = False
TEST = False
if TEST:
    DEFAULT_FILEPATH = f"../data/{Path(__file__).stem}.test.txt"
    PART_1_TIME_SAVED = 2
    PART_2_TIME_SAVED = 50
else:
    DEFAULT_FILEPATH = f"../data/{Path(__file__).stem}.txt"
    PART_1_TIME_SAVED = 100
    PART_2_TIME_SAVED = 100
PART_1_CHEAT_DISTANCE = 2
PART_2_CHEAT_DISTANCE = 20

START = "S"
END = "E"
WALL = "#"
TRACK = "."

INVALID_COORD = (-1, -1)
NEIGHBOURS = ((1, 0), (-1, 0), (0, 1), (0, -1))

def possible_coords(r, c, grid, cheat_distance):
    cheat_distance += 1
    ROWS, COLS = len(grid), len(grid[0])
    cheat_range = range(-cheat_distance, cheat_distance + 1)
    possible_coords = []

    for dr in cheat_range:
        for dc in cheat_range:
            nr = r + dr
            nc = c + dc
            if (nr in range(ROWS) and
                nc in range(COLS) and
                abs(nr - r) + abs(nc - c) < cheat_distance
                and grid[nr][nc] != WALL
            ):
                possible_coords.append((nr, nc))
    return possible_coords

def min_path(grid, start, end, cache):
    
    ROWS, COLS = len(grid), len(grid[0])
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
                cache[(r, c)] = steps + 1
            return steps + 1
        visited.add((r, c))
        history = history.copy()
        history.append((steps, r, c))
        
        for dr, dc in NEIGHBOURS:
            heapq.heappush(min_heap, (steps + 1, r + dr, c + dc, history))
    return -1

def all_min_path_no_cheat(grid, end):
    ROWS, COLS = len(grid), len(grid[0])
    default_times = {}
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] in (TRACK, START):
                default_times[(r, c)] = min_path(grid, (r, c), end, dict())
    default_times[end] = 0
    return default_times

def get_start_and_end(grid):
    start = INVALID_COORD
    end = INVALID_COORD
    
    for r, row in enumerate(grid):
        for c, elem in enumerate(row):
            if elem == START:
                start = (r, c)
            elif elem == END:
                end = (r, c)
    assert start != INVALID_COORD and end != INVALID_COORD
    return start, end

def get_times_in_range(cheat_distance, time_saved):
    
    times_in_range = []
    time_from_start = default_times[start]
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] != WALL:
                time_to_r_c = time_from_start - default_times[(r, c)]
                for nr, nc in possible_coords(r, c, grid, cheat_distance):
                    time_with_skip = time_to_r_c + default_times[(nr, nc)] + abs(r - nr) + abs(c - nc)
                    time_saved = time_from_start - time_with_skip
                    if time_saved >= time_saved:
                        times_in_range.append(time_with_skip)
    return times_in_range

def get_counter(times_in_range):
    counter = Counter(list(map(lambda x: default_times[start] - x, filter(lambda x: x in range(default_times[start] - PART_1_TIME_SAVED + 1 ), times_in_range))))
    for time_saved, count in sorted(counter.items()):
        if PRINT:
            print(f"There are {count} cheats that save {time_saved} picoseconds.")
    return counter

def part1():
    times_in_range = get_times_in_range(PART_1_CHEAT_DISTANCE, PART_1_TIME_SAVED)
    counter = get_counter(times_in_range)
    return sum(counter.values())
    
def part2():
    
    times_in_range = get_times_in_range(PART_2_CHEAT_DISTANCE, PART_2_TIME_SAVED)

    counter = Counter(list(map(lambda x: default_times[start] - x, filter(lambda x: x in range(default_times[start] - PART_2_TIME_SAVED + 1 ), times_in_range))))
    for time_saved, count in sorted(counter.items()):
        if PRINT:
            print(f"There are {count} cheats that save {time_saved} picoseconds.")
    return sum(counter.values())

def parse():
    with open(filename) as f:
        inp = f.read()
    grid = []
    for line in inp.split("\n"):
        grid.append(list(line))
    return grid

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILEPATH
    
    grid =  parse()
    ROWS, COLS = len(grid), len(grid[0])
    
    start, end = get_start_and_end(grid)
    default_times = all_min_path_no_cheat(grid, end)

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))
