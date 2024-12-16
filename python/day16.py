import sys
import heapq
from enum import Enum

START = "S"
EMPTY = "."
WALL = "#"
END = "E"

NORTH, EAST, SOUTH, WEST = range(4)
class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    
    @staticmethod
    def to_str(direction):
        match direction:
            case Direction.NORTH:
                return "^"
            case Direction.EAST:
                return ">"
            case Direction.SOUTH:
                return "v"
            case Direction.WEST:
                return "<"
        return "X"
    
ROTATIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))

def show_history(grid, history):
    grid = grid.copy()
    history_dict = {}
    for r, c, direction in history:
        history_dict[(r, c)] = direction
    for r, row in enumerate(grid):
        for c, elem in enumerate(row):
            if (r, c) in history_dict:
                grid[r][c] = Direction.to_str(Direction(direction))
                
    for row in grid:
        print("".join(row))
    print()

def part1():
    
    grid = parse()
    ROWS, COLS = len(grid), len(grid[0])
    
    initial_pos = (-1, -1)
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == START:
                initial_pos = (r, c)
    print(f"{initial_pos=}")
    min_heap = [(0, initial_pos[0], initial_pos[1], EAST, [])] # (score, r, c, direction, history)
    visited = set()
    while min_heap:
        score, r, c, direction, history = heapq.heappop(min_heap)
        # print(score, r, c, direction)
        dr, dc = ROTATIONS[direction]
        if (
            r not in range(ROWS) or
            c not in range(COLS) or
            grid[r][c] == WALL or
            (r, c, dr, dc) in visited
        ):
            continue
        if grid[r][c] == END:
            show_history(grid, history)
            return score
        visited.add((r, c, dr, dc))
        
        # go straight
        heapq.heappush(min_heap, (score + 1, r + dr, c + dc, direction, history + [(r, c, direction)]))
        
        # try turning
        heapq.heappush(min_heap, (score + 1000, r, c, (direction + 1) % 4, history + [(r, c, direction)]))
        heapq.heappush(min_heap, (score + 1000, r, c, (direction - 1) % 4, history + [(r, c, direction)]))
    
    return -1

def part2():
    pass

def parse():
    with open(filename) as f:
        inp = f.read()

    grid = list(map(list, inp.split("\n")))
    return grid

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day16.txt"

    print(part1())
    print(part2())
