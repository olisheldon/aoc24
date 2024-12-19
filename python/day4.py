import sys
import re
from pathlib import Path

XMAS = "XMAS"
DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))

def part1():
    grid = lines
    ROWS, COLS = len(grid), len(grid[0])
    
    def word_found(r, c, i, dr, dc) -> bool:
        if i == len(XMAS):
            return True
        return r in range(ROWS) and c in range(COLS) and grid[r][c] == XMAS[i] and word_found(r + dr, c + dc, i + 1, dr, dc)
    
    return sum(word_found(r, c, 0, dr, dc) for r in range(ROWS) for c in range(COLS) for dr, dc in DIRECTIONS)

def part2():
    grid = lines
    ROWS, COLS = len(grid), len(grid[0])
    
    def word_found(r, c) -> bool:
        return (
                    grid[r][c] == "A" and
                    (
                        (
                            (
                                grid[r - 1][c - 1] == "M" and grid[r + 1][c + 1] == "S"
                            )
                            or
                            (
                                grid[r - 1][c - 1] == "S" and grid[r + 1][c + 1] == "M"
                            )
                        ) 
                        and
                        (
                            (
                                grid[r + 1][c - 1] == "M" and grid[r - 1][c + 1] == "S"
                            )
                            or
                            (
                                grid[r + 1][c - 1] == "S" and grid[r - 1][c + 1] == "M"
                            )
                        ) 
                    )
                )
    
    count = 0
    for r in range(1, ROWS - 1):
        for c in range(1, COLS - 1):
            count += word_found(r, c)
    return count
            
            
                    

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()

    lines = list(map(list, inp.split("\n")))
    
    print("part1=" + str(part1()))
    print("part2=" + str(part2()))