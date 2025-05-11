import sys
from enum import Enum, auto
from collections import defaultdict, deque
from pathlib import Path

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
    grid = parse()
    rows = len(grid)
    cols = len(grid[0])
    
    regions = []
    seen = set()
    
    for r in range(rows):
        for c in range(cols):
            if (r, c) in seen:
                continue
                
            crop = grid[r][c]
            region = {(r, c)}
            seen.add((r, c))
            
            q = deque([(r, c)])
            while q:
                cr, cc = q.popleft()
                for nr, nc in [(cr-1, cc), (cr+1, cc), (cr, cc-1), (cr, cc+1)]:
                    if nr < 0 or nc < 0 or nr >= rows or nc >= cols:
                        continue
                    if grid[nr][nc] != crop:
                        continue
                    if (nr, nc) in region:
                        continue
                    region.add((nr, nc))
                    seen.add((nr, nc))
                    q.append((nr, nc))
            
            regions.append((crop, region))
    
    def count_sides(region):
        corner_candidates = set()
        for r, c in region:
            for cr, cc in [(r-0.5, c-0.5), (r+0.5, c-0.5), (r+0.5, c+0.5), (r-0.5, c+0.5)]:
                corner_candidates.add((cr, cc))
        
        corners = 0
        for cr, cc in corner_candidates:
            config = [
                (int(cr-0.5), int(cc-0.5)) in region,
                (int(cr+0.5), int(cc-0.5)) in region,
                (int(cr+0.5), int(cc+0.5)) in region,
                (int(cr-0.5), int(cc+0.5)) in region,
            ]
            
            number = sum(config)
            if number == 1:
                corners += 1
            elif number == 2:
                if (config[0] and config[2]) or (config[1] and config[3]):
                    corners += 2
            elif number == 3:
                corners += 1
        
        return corners
    
    total_price = 0
    for crop, region in regions:
        area = len(region)
        sides = count_sides(region)
        price = area * sides
        total_price += price
        
    return total_price

def parse():
    with open(filename) as f:
        inp = f.read()
    return list(list(line) for line in inp.splitlines())

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))