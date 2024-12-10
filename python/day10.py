import sys

SUMMIT = 9
TRAILHEAD = 0

def part1():
    grid = lines
    ROWS, COLS = len(grid), len(grid[0])
    NEIGHBOURS = ((1, 0), (-1, 0), (0, 1), (0, -1))
    
    count = 0
    visited = set()
    def dfs(r, c, prev):
        nonlocal count
        if (
            r not in range(ROWS) or
            c not in range(COLS) or
            (r, c) in visited or
            abs(prev - grid[r][c]) > 1
        ):
            return
        if grid[r][c] == SUMMIT:
            visited.add((r, c))
            count += 1
            return
        
        visited.add((r, c))
        for dr, dc in NEIGHBOURS:
            dfs(r + dr, c + dc, grid[r][c])
        visited.remove((r, c))

    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == TRAILHEAD:
                dfs(r, c, TRAILHEAD)
    return count
        
        

def part2():
    pass

def parse():
    with open(filename) as f:
        inp = f.read()
    return list(list(map(int, line)) for line in inp.splitlines())

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day10.test.txt"
    lines = parse()
    
    print(lines)

    print(f"{part1()=}")
    print(f"{part2()=}")