import sys
import heapq
from enum import Enum
from pathlib import Path
from collections import deque

PRINT = False

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

def show_history(grid, history, show_path=True):
    if not PRINT:
        return
    grid = grid.copy()
    history_dict = {}
    for r, c, direction in history:
        history_dict[(r, c)] = direction
    for r, row in enumerate(grid):
        for c, elem in enumerate(row):
            if (r, c) in history_dict:
                if show_path:
                    grid[r][c] = Direction.to_str(Direction(direction))
                else:
                    grid[r][c] = "O"
            
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
                
    min_heap = [(0, initial_pos[0], initial_pos[1], EAST, [])] # (score, r, c, direction, history)
    visited = set()
    while min_heap:
        score, r, c, direction, history = heapq.heappop(min_heap)
        dr, dc = ROTATIONS[direction]
        if (
            r not in range(ROWS) or
            c not in range(COLS) or
            grid[r][c] == WALL or
            (r, c, dr, dc) in visited
        ):
            continue
        if grid[r][c] == END:
            break
        visited.add((r, c, dr, dc))
        
        # go straight
        heapq.heappush(min_heap, (score + 1, r + dr, c + dc, direction, history + [(r, c, direction)]))
        
        # try turning
        heapq.heappush(min_heap, (score + 1000, r, c, (direction + 1) % 4, history + [(r, c, direction)]))
        heapq.heappush(min_heap, (score + 1000, r, c, (direction - 1) % 4, history + [(r, c, direction)]))
    
    
    show_history(grid, history)
    return score

def part2():
    grid = parse()
    ROWS, COLS = len(grid), len(grid[0])
    
    initial_pos = (-1, -1)
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == START:
                initial_pos = (r, c)
                break
        if initial_pos != (-1, -1):
            break
    
    sr, sc = initial_pos
    
    pq = [(0, sr, sc, 0, 1)]  # (cost, r, c, dr, dc)
    lowest_cost = {(sr, sc, 0, 1): 0}
    backtrack = {}
    best_cost = float("inf")
    end_states = set()
    
    while pq:
        cost, r, c, dr, dc = heapq.heappop(pq)
        
        if cost > lowest_cost.get((r, c, dr, dc), float("inf")):
            continue
            
        if grid[r][c] == END:
            if cost > best_cost:
                break
            best_cost = cost
            end_states.add((r, c, dr, dc))
            
        for new_cost, nr, nc, ndr, ndc in [
            (cost + 1, r + dr, c + dc, dr, dc),
            (cost + 1000, r, c, dc, -dr),
            (cost + 1000, r, c, -dc, dr)
        ]:
            if nr not in range(ROWS) or nc not in range(COLS) or grid[nr][nc] == WALL:
                continue
                
            lowest = lowest_cost.get((nr, nc, ndr, ndc), float("inf"))
            if new_cost > lowest:
                continue
                
            if new_cost < lowest:
                backtrack[(nr, nc, ndr, ndc)] = set()
                lowest_cost[(nr, nc, ndr, ndc)] = new_cost
                
            backtrack[(nr, nc, ndr, ndc)].add((r, c, dr, dc))
            heapq.heappush(pq, (new_cost, nr, nc, ndr, ndc))
    
    states = deque(end_states)
    seen = set(end_states)
    
    while states:
        key = states.popleft()
        for last in backtrack.get(key, []):
            if last in seen:
                continue
            seen.add(last)
            states.append(last)
    
    unique_tiles = {(r, c) for r, c, _, _ in seen}
    
    if PRINT:
        solution_grid = [row[:] for row in grid]
        for r, c in unique_tiles:
            if solution_grid[r][c] not in (START, END):
                solution_grid[r][c] = "O"
        for row in solution_grid:
            print("".join(row))
        print()
    
    return len(unique_tiles)

def parse():
    with open(filename) as f:
        inp = f.read()
    grid = list(map(list, inp.split("\n")))
    return grid

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))
