import sys
from pathlib import Path

PRINT = True

WALL = "#"
BOX = "O"
ROBOT = "@"
EMPTY = "."

# Part 2 constants
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

def score_wide_boxes(grid):
    """Score for Part 2, handles wide boxes represented as [] pairs"""
    total = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == WIDE_BOX_LEFT:
                # GPS coordinate is calculated from the edge of the map to the left edge of the box
                total += 100 * r + c
    return total

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
    """
    Transform the grid for Part 2:
    - Wall (#) becomes ##
    - Box (O) becomes []
    - Empty (.) becomes ..
    - Robot (@) becomes @.
    """
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

def part2():
    grid, moves = parse()
    original_grid = grid
    grid = widen_grid(grid)
    
    # Just for debugging
    if PRINT:
        print("Widened grid:")
        for row in grid:
            print("".join(row))
        print()
        
    ROWS, COLS = len(grid), len(grid[0])

    initial_pos = (-1, -1)
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == ROBOT:
                initial_pos = (r, c)
    
    r, c = initial_pos

    for move in moves:
        dr, dc = move_to_dir[move]
        nr, nc = r + dr, c + dc
        
        # Check if the move is valid
        if nr not in range(ROWS) or nc not in range(COLS) or grid[nr][nc] == WALL:
            # Cannot move into a wall or out of bounds
            print_grid(move, grid)
            continue
            
        if grid[nr][nc] == EMPTY:
            # Simple move to an empty space
            grid[r][c] = EMPTY
            grid[nr][nc] = ROBOT
            r, c = nr, nc
            print_grid(move, grid)
            continue
        
        # Handle moving boxes
        if dc != 0:  # Horizontal movement
            # Check if pushing a box
            if grid[nr][nc] == WIDE_BOX_LEFT and nc + 1 < COLS and grid[nr][nc + 1] == WIDE_BOX_RIGHT:
                # We're pushing the left side of a wide box
                boxes_to_push = []
                curr_r, curr_c = nr, nc
                
                # Find all consecutive boxes
                while (curr_r in range(ROWS) and curr_c in range(COLS) and 
                       curr_c + 1 < COLS and 
                       grid[curr_r][curr_c] == WIDE_BOX_LEFT and 
                       grid[curr_r][curr_c + 1] == WIDE_BOX_RIGHT):
                    boxes_to_push.append((curr_r, curr_c))
                    curr_r, curr_c = curr_r + dr, curr_c + dc
                    
                    # Skip over the right part of the box when moving right
                    if dc > 0:
                        curr_c += 1
                
                # Check if the push is valid
                if (curr_r in range(ROWS) and curr_c in range(COLS) and 
                    curr_c + dc in range(COLS) and 
                    grid[curr_r][curr_c] == EMPTY and 
                    (dc < 0 or (dc > 0 and grid[curr_r][curr_c + 1] == EMPTY))):
                    
                    # Move boxes starting from the farthest one
                    for box_r, box_c in reversed(boxes_to_push):
                        if dc > 0:  # Moving right
                            # Move the box right
                            grid[box_r][box_c + 2] = WIDE_BOX_RIGHT
                            grid[box_r][box_c + 1] = WIDE_BOX_LEFT
                            grid[box_r][box_c] = EMPTY
                        else:  # Moving left
                            # Move the box left
                            grid[box_r][box_c - 1] = WIDE_BOX_LEFT
                            grid[box_r][box_c] = WIDE_BOX_RIGHT
                            grid[box_r][box_c + 1] = EMPTY
                    
                    # Move the robot
                    grid[r][c] = EMPTY
                    grid[nr][nc] = ROBOT
                    r, c = nr, nc
                    print_grid(move, grid)
                    continue
            
            elif grid[nr][nc] == WIDE_BOX_RIGHT and nc - 1 >= 0 and grid[nr][nc - 1] == WIDE_BOX_LEFT:
                # We're pushing the right side of a wide box - this is invalid
                print_grid(move, grid)
                continue
        
        elif dr != 0:  # Vertical movement
            # For vertical movement, we need to check if we're pushing a box from above/below
            if grid[nr][nc] == WIDE_BOX_LEFT and nc + 1 < COLS and grid[nr][nc + 1] == WIDE_BOX_RIGHT:
                # We're pushing a box vertically
                boxes_to_push = []
                curr_r, curr_c = nr, nc
                
                # Find all consecutive box pairs in the vertical direction
                while (curr_r in range(ROWS) and curr_c in range(COLS) and 
                       curr_c + 1 < COLS and 
                       grid[curr_r][curr_c] == WIDE_BOX_LEFT and 
                       grid[curr_r][curr_c + 1] == WIDE_BOX_RIGHT):
                    boxes_to_push.append((curr_r, curr_c))
                    curr_r += dr
                    
                # Check if push is valid (need two empty spaces for the wide box)
                if (curr_r in range(ROWS) and curr_c in range(COLS) and 
                    curr_c + 1 < COLS and 
                    grid[curr_r][curr_c] == EMPTY and 
                    grid[curr_r][curr_c + 1] == EMPTY):
                    
                    # Move boxes starting from the farthest one
                    for box_r, box_c in reversed(boxes_to_push):
                        # Move the box vertically
                        target_r = box_r + dr
                        grid[target_r][box_c] = WIDE_BOX_LEFT
                        grid[target_r][box_c + 1] = WIDE_BOX_RIGHT
                        grid[box_r][box_c] = EMPTY
                        grid[box_r][box_c + 1] = EMPTY
                    
                    # Move the robot
                    grid[r][c] = EMPTY
                    grid[nr][nc] = ROBOT
                    r, c = nr, nc
                    print_grid(move, grid)
                    continue
        
        # If we get here, the move failed
        print_grid(move, grid)
    
    # Just for debugging - print the final state
    if PRINT:
        print("Final state:")
        for row in grid:
            print("".join(row))
        print()
        
    # Compare against the expected final state from problem description
    expected_final = [
        "####################",
        "##[].......[].[][]##",
        "##[]...........[].##",
        "##[]........[][][]##",
        "##[]......[]....[]##",
        "##..##......[]....##",
        "##..[]............##",
        "##..@......[].[][]##",
        "##......[][]..[]..##",
        "####################"
    ]
    
    if PRINT:
        print("Expected final state:")
        for row in expected_final:
            print(row)
        print()
        
        # Debug: count boxes in both states
        actual_boxes = sum(1 for r in range(ROWS) for c in range(COLS) if grid[r][c] == WIDE_BOX_LEFT)
        expected_boxes = sum(1 for r in range(len(expected_final)) for c in range(len(expected_final[0])) if c < len(expected_final[r]) and expected_final[r][c] == WIDE_BOX_LEFT)
        print(f"Actual boxes: {actual_boxes}")
        print(f"Expected boxes: {expected_boxes}")
        
        # Debug: match positions
        actual_positions = [(r, c) for r in range(ROWS) for c in range(COLS) if grid[r][c] == WIDE_BOX_LEFT]
        expected_positions = [(r, c) for r in range(len(expected_final)) for c in range(len(expected_final[0])) if c < len(expected_final[r]) and expected_final[r][c] == WIDE_BOX_LEFT]
        
        for i, (r, c) in enumerate(actual_positions):
            if i < len(expected_positions):
                er, ec = expected_positions[i]
                print(f"Box {i+1}: Actual ({r}, {c}) | Expected ({er}, {ec})")
    
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
