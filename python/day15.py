import sys
from pathlib import Path

PRINT = False

WALL = "#"
BOX = "O"
ROBOT = "@"
EMPTY = "."

WIDE_BOX_LEFT = "["
WIDE_BOX_RIGHT = "]"

move_to_dir = {
    "v" : (1, 0),
    ">" : (0, 1),
    "^" : (-1, 0),
    "<" : (0, -1),
}

def score(grid):
    return sum(100 * r + c for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == BOX)

def print_grid(move, grid):
    if not PRINT:
        return
    print(f"Move {move}:")
    for row in grid:
        print("".join(row))
    print()

def part1():
    
    grid, moves = parse()
    ROWS, COLS = len(grid), len(grid[0])

    initial_pos = (-1, -1)
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == ROBOT:
                initial_pos = (r, c)
    
    r, c = initial_pos

    for move in moves:
        dr, dc = move_to_dir[move]

        stack = []
        nr, nc = r + dr, c + dc
        while nr in range(ROWS) and nc in range(COLS) and grid[nr][nc] != EMPTY and grid[nr][nc] != WALL:
            stack.append((nr, nc))

            nr += dr
            nc += dc
        
        if nr not in range(ROWS) or nc not in range(COLS) or grid[nr][nc] == WALL:
            stack = []
            print_grid(move, grid)
            continue
        
        while stack:
            x, y = stack.pop()
            
            grid[nr][nc] = grid[x][y]

            nr -= dr
            nc -= dc
        grid[r][c] = EMPTY
        grid[nr][nc] = ROBOT
        r, c = nr, nc

        print_grid(move, grid)
    
    return score(grid)

def widen_grid(grid):
    widened_grid = []
    for row in grid:
        new_row = []
        for elem in row:
            if elem == WALL:
                new_row.extend([WALL, WALL])
            elif elem == BOX:
                new_row.extend([WIDE_BOX_LEFT, WIDE_BOX_RIGHT])
            elif elem == EMPTY:
                new_row.extend([EMPTY, EMPTY])
            elif elem == ROBOT:
                new_row.extend([ROBOT, EMPTY])
            else:
                raise RuntimeError(f"Unknown element: {elem}")
        widened_grid.append(new_row)
    return widened_grid

def score_wide_boxes(grid):
    total = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == WIDE_BOX_LEFT:
                total += 100 * r + c
    return total

def part2():
    grid, moves = parse()
    
    grid = widen_grid(grid)
    
    ROWS, COLS = len(grid), len(grid[0])
    
    r, c = -1, -1
    for i in range(ROWS):
        for j in range(COLS):
            if grid[i][j] == ROBOT:
                r, c = i, j
                break
        if r != -1:
            break
    
    for move in moves:
        dr, dc = move_to_dir[move]
        
        targets = [(r, c)]
        go = True
        
        for cr, cc in targets:
            nr = cr + dr
            nc = cc + dc
            
            if (nr, nc) in targets:
                continue
                
            if nr < 0 or nr >= ROWS or nc < 0 or nc >= COLS:
                go = False
                break
                
            char = grid[nr][nc]
            
            if char == WALL:
                go = False
                break
                
            if char == WIDE_BOX_LEFT:
                targets.append((nr, nc))
                targets.append((nr, nc + 1))
                
            if char == WIDE_BOX_RIGHT:
                targets.append((nr, nc))
                targets.append((nr, nc - 1))
        
        if not go:
            print_grid(move, grid)
            continue
            
        grid_copy = [list(row) for row in grid]
        
        grid[r][c] = EMPTY
        for br, bc in targets[1:]:
            grid[br][bc] = EMPTY
            
        grid[r + dr][c + dc] = ROBOT
        
        for br, bc in targets[1:]:
            grid[br + dr][bc + dc] = grid_copy[br][bc]
            
        r += dr
        c += dc
        
        print_grid(move, grid)
    
    return score_wide_boxes(grid)

def parse():
    with open(filename) as f:
        inp = f.read()
    grid, moves = inp.split("\n\n")

    grid = list(map(list, grid.split("\n")))
    moves = moves.replace("\n", "")
    return grid, moves

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))
