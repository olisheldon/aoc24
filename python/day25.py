import sys
from pathlib import Path
from collections import Counter

EMPTY = "."
FILLED = "#"
FULL = 6

def no_overlap(key, lock):
    return all(x < FULL for x in (x + y for (x, y) in zip(lock, key)))

def part1():
    keys, locks = parse()
    
    res = 0
    for lock in locks:
        for key in keys:
            res += no_overlap(key, lock)
    return res

def part2():
    return "INCOMPLETE"
    keys, locks = parse()
    keys = Counter(keys)
    locks = Counter(locks)
    
    # print(locks)
    
    res = 0
    for key, count in keys.items():
        # comp_lock = tuple(map(lambda x, y: x - y, zip([6] * 5, key)))
        comp_lock = tuple((x - y for (x, y) in zip([7] * 5, key)))
        # print(key, comp_lock)
        if comp_lock in locks:
            res += locks[comp_lock] * count
    return res

def parse():
    with open(filename) as f:
        inp = f.read()
    grids = inp.split("\n\n")
    keys, locks = [], []
    for grid in grids:
        grid = grid.split("\n")
        rows = [-1] * len(grid[0])
        for row in grid:
            for i, elem in enumerate(row):
                if elem == FILLED:
                    rows[i] += 1
        rows = tuple(rows)
        if all(elem == FILLED for elem in grid[0]):
            keys.append(rows)
        else:
            locks.append(rows)
    return keys, locks

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))
