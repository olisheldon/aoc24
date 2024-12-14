import sys

def part1():
    
    node_symbols = {x : [] for x in set("".join(line) for line in lines) - set(".")}
    grid = lines
    ROWS, COLS = len(grid), len(grid[0])

    for r, row in enumerate(lines):
        for c, elem in enumerate(row):
            if elem in node_symbols:
                node_symbols[elem].append((r, c))

    antinode_locations = set()
    for node_symbol, locs in node_symbols.items():
        potential_antinode_locations = set()
        for i in range(len(locs)):
            for j in range(i + 1, len(locs)):
                (x0, y0), (x1, y1) = sorted(((locs[i][0], locs[i][1]), (locs[j][0], locs[j][1])))
                a1_to_a0 = (x0 - x1, y0 - y1)
                a0_to_a1 = (x1 - x0, y1 - y0)
                potential_loc_1 = (x0 + a0_to_a1[0], y0 + a0_to_a1[1])
                if potential_loc_1 in potential_antinode_locations:
                    antinode_locations.add(potential_loc_1)
                potential_antinode_locations.add(potential_loc_1)
                potential_loc_2 = (x1 + a1_to_a0[0], y1 + a1_to_a0[1])
                if potential_loc_2 in potential_antinode_locations:
                    antinode_locations.add(potential_loc_2)
                potential_antinode_locations.add(potential_loc_2)

    within_bounds = lambda x: x[0] in range(ROWS) and x[1] in range(COLS)
    res = list(filter(within_bounds, antinode_locations))
    return res

def part2():
    pass

def parse():
    with open(filename) as f:
        inp = f.read()
    lines = inp.split("\n")
    return list(map(list, lines))

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day8.test.txt"
    lines = parse()
    print(lines)

    print(f"{part1()=}")
    print(f"{part2()=}")