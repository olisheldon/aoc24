import sys

A = "A"
B = "B"
C = "C"
D = "D"
E = "E"


def part1():
    NEIGHBOURS = ((1, 0), (-1, 0), (0, 1), (0, -1))
    grid = parse()
    ROWS, COLS = len(grid), len(grid[0])
    
    def calc_perimeter(grid, r, c, veg):
        perimeter = 0
        for dr, dc in NEIGHBOURS:
            if r + dr not in range(ROWS) or c + dc not in range(COLS) or grid[r + dr][c + dc] != veg:
                perimeter += 1
        return perimeter
    
    visited = set()
    def dfs(r, c, veg): # -> perim, area
        if (
            (r, c) in visited or
            r not in range(ROWS) or
            c not in range(COLS) or
            grid[r][c] != veg
            ):
            return 0, 0
        visited.add((r, c))
        
        perim = calc_perimeter(grid, r, c, veg)
        area = 1
        
        for dr, dc in NEIGHBOURS:
            res = dfs(r + dr, c + dc, veg)
            perim += res[0]
            area += res[1]
        return perim, area
    
    res = []
    for r in range(ROWS):
        for c in range(COLS):
            if (r, c) not in visited:
                res.append(dfs(r, c, grid[r][c]))
    return sum(map(lambda x: x[0] * x[1], res))
        

def part2():
    pass

def parse():
    with open(filename) as f:
        inp = f.read()
    return list(list(line) for line in inp.splitlines())

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day12.txt"

    print(f"{part1()=}")
    print(f"{part2()=}")