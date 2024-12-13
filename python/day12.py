import sys
from enum import Enum, auto
from collections import defaultdict

class Direction(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()
    
    @staticmethod
    def get_direction(dr, dc):
        if dr:
            return Direction.HORIZONTAL
        elif dc:
            return Direction.VERTICAL
        raise RuntimeError(f"dr or dc must be specified for direction {dr=}{dc=}")

def part1_helper():
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
    return res

def part1():
    return sum(map(lambda x: x[0] * x[1], part1_helper()))

def part2():
    NEIGHBOURS = ((1, 0), (-1, 0), (0, 1), (0, -1))
    grid = parse()
    ROWS, COLS = len(grid), len(grid[0])
    visited = set()
    
    side_id = 0
    coords_to_side_ids = defaultdict(set) # (r, c) : set(int)
    side_id_to_coords = defaultdict(set)
    
    def dfs_side(dr, dc, r, c, veg, seen):
        nonlocal side_id
        direction = Direction.get_direction(dr, dc)
        if (
            (r, c) in seen or
            r not in range(ROWS) or
            c not in range(COLS) or
            grid[r][c] != veg
        ):
            return 0
        seen.add((r, c))
        
        side_id_to_coords[side_id].add((r, c))
        coords_to_side_ids[(r, c)].add(side_id)
        
        # r, c is new coord of this side
        return 1 + dfs_side(dr, dc, r + dr, c + dc, veg, seen)
    
    def dfs(r, c, veg): # -> area
        nonlocal side_id
        if (
            (r, c) in visited or
            r not in range(ROWS) or
            c not in range(COLS) or
            grid[r][c] != veg
            ):
            return 0, 0
        visited.add((r, c))
        
        if not side_id_to_coords[(r, c)]:
            side_id += 1
        
        perim = 0
        for dr in (-1, 1):
            perim += dfs_side(dr, 0, r, c, veg, set())
        for dc in (-1, 1):
            perim += dfs_side(0, dc, r, c, veg, set())
        
        area = 0
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
    return part1_helper()
    return side_id_to_coords

def parse():
    with open(filename) as f:
        inp = f.read()
    return list(list(line) for line in inp.splitlines())

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day12.test.txt"

    print(f"{part1()=}")
    print(f"{part2()=}")