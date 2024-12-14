import sys
from collections import defaultdict


def print_antinodes(grid, antinode_locs):
    grid = grid.copy()
    for r, row in enumerate(grid):
        for c, elem in enumerate(row):
            if elem == "." and (r, c) in antinode_locs:
                grid[r][c] = "#"
    for line in grid:
        print("".join(line))
            

def part1():

    lines = parse()

    node_symbols = defaultdict(list)
    grid = lines
    ROWS, COLS = len(grid), len(grid[0])

    for r, row in enumerate(lines):
        for c, elem in enumerate(row):
            if elem != ".":
                node_symbols[elem].append((r, c))

    antinode_locations = list()
    for node_symbol, locs in node_symbols.items():
        for i in range(len(locs)):
            for j in range(i + 1, len(locs)):
                (x0, y0), (x1, y1) = sorted(((locs[i][0], locs[i][1]), (locs[j][0], locs[j][1])))
                a1_to_a0 = (x0 - x1, y0 - y1)
                a0_to_a1 = (x1 - x0, y1 - y0)
                antinode_locations.append((x0 + 2 * a0_to_a1[0], y0 + 2 * a0_to_a1[1]))
                antinode_locations.append((x1 + 2 * a1_to_a0[0], y1 + 2 * a1_to_a0[1]))

    within_bounds = lambda x: x[0] in range(ROWS) and x[1] in range(COLS)
    res = set(filter(within_bounds, antinode_locations))
    return len(res)
            

def part2():

    lines = parse()
    grid = lines

    node_symbols = defaultdict(list)
    ROWS, COLS = len(grid), len(grid[0])

    for r, row in enumerate(lines):
        for c, elem in enumerate(row):
            if elem != ".":
                node_symbols[elem].append((r, c))

    antinode_locations = set()
    for node_symbol, locs in node_symbols.items():
        for i in range(len(locs)):
            for j in range(i + 1, len(locs)):
                (x0, y0), (x1, y1) = sorted(((locs[i][0], locs[i][1]), (locs[j][0], locs[j][1])))
                a1_to_a0 = (x0 - x1, y0 - y1)
                a0_to_a1 = (x1 - x0, y1 - y0)

                get_loc1 = lambda steps: (x0 + (1 + steps) * a0_to_a1[0], y0 + (1 + steps) * a0_to_a1[1])
                steps = 1
                loc1 = get_loc1(steps)
                while loc1[0] in range(ROWS) and loc1[1] in range(COLS):
                    loc1 = get_loc1(steps)
                    antinode_locations.add(loc1)

                    steps += 1

                get_loc2 = lambda steps: (x1 + (1 + steps) * a1_to_a0[0], y1 + (1 + steps) * a1_to_a0[1])
                steps = 1
                loc2 = get_loc2(steps)
                while loc2[0] in range(ROWS) and loc2[1] in range(COLS):
                    loc2 = get_loc2(steps)
                    antinode_locations.add(loc2)

                    steps += 1

    within_bounds = lambda x: x[0] in range(ROWS) and x[1] in range(COLS)
    res = set(filter(within_bounds, antinode_locations)) | set(antenna_loc for node in node_symbols.values() for antenna_loc in node)
    return len(res)

def parse():
    with open(filename) as f:
        inp = f.read()
    lines = inp.split("\n")
    return list(map(list, lines))

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day8.txt"

    print(f"{part1()=}")
    print(f"{part2()=}")