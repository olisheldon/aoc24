import sys

SUMMIT = 9
TRAILHEAD = 0

def part1():
    grid = parse()
    ROWS, COLS = len(grid), len(grid[0])
    NEIGHBOURS = ((1, 0), (-1, 0), (0, 1), (0, -1))
    
    def dfs(r, c, prev):
        if (
            r not in range(ROWS) or
            c not in range(COLS) or
            (r, c) in visited or
            grid[r][c] - prev != 1
        ):
            return 0
        if grid[r][c] == SUMMIT:
            visited.add((r, c))
            return 1
        
        res = 0
        visited.add((r, c))
        for dr, dc in NEIGHBOURS:
            res += dfs(r + dr, c + dc, grid[r][c])
        visited.remove((r, c))
        return res

    res = 0
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == TRAILHEAD:
                visited = set()
                res += dfs(r, c, TRAILHEAD - 1)
    return res

def part2():
    pass

def parse():
    with open(filename) as f:
        inp = f.read()
    return list(list(map(int, line)) for line in inp.splitlines())

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day10.txt"
    
    print(f"{part1()=}")
    print(f"{part2()=}")