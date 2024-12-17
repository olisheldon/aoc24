import sys

PRINT = False

WALL = "#"
BOX = "O"
ROBOT = "@"
EMPTY = "."

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
        
        # move not possible, do nothing
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
    for r, row in enumerate(grid):
        for c, elem in enumerate(row):
            if elem == WALL:
                widened_grid.append(2 * WALL)
            elif elem == BOX:
                widened_grid.append(2 * BOX)
            elif elem == EMPTY:
                widened_grid.append(2 * EMPTY)
            elif elem == ROBOT:
                widened_grid.append(ROBOT + EMPTY)
            else:
                raise RuntimeError()
        widened_grid.append("\n")
    a = "".join("".join(row) for row in widened_grid).split("\n")[:-1]
    return [list(b) for b in a]

def part2():
    
    grid, moves = parse()
    grid = widen_grid(grid)
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
        
        # move not possible, do nothing
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

def parse():
    with open(filename) as f:
        inp = f.read()
    grid, moves = inp.split("\n\n")

    grid = list(map(list, grid.split("\n")))
    moves = moves.replace("\n", "")
    return grid, moves

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day15.txt"

    # print(part1())
    print(part2())
