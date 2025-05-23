import sys
import functools
from pathlib import Path

ROWS, COLS = 101, 103
# ROWS, COLS = 11, 7

def safety_value(robots):
    quadrants = [0] * 4
    for pos, _ in robots:
        if pos[0] == ROWS // 2 or pos[1] == COLS // 2:
            continue
        
        if pos[0] in range(ROWS // 2) and pos[1] in range(COLS // 2):
            quadrants[0] += 1
        if pos[0] in range(ROWS // 2, ROWS) and pos[1] in range(COLS // 2):
            quadrants[1] += 1
        if pos[0] in range(ROWS // 2) and pos[1] in range(COLS // 2, COLS):
            quadrants[2] += 1
        if pos[0] in range(ROWS // 2, ROWS) and pos[1] in range(COLS // 2, COLS):
            quadrants[3] += 1
    return quadrants

def part1():
    robots = parse()

    for _ in range(100):
        for pos, vel in robots:
            pos[0] = (pos[0] + vel[0]) % ROWS
            pos[1] = (pos[1] + vel[1]) % COLS

    return functools.reduce(lambda x, y: x * y, safety_value(robots))

def detect_christmas(robots):
    top_left, top_right, bot_left, bot_right = tuple([0] * 4)
    for pos, _ in robots:
        if pos[0] == ROWS // 2 or pos[1] == COLS // 2:
            continue
        
        if pos[0] in range(ROWS // 2) and pos[1] in range(COLS // 2):
            top_left += 1
        if pos[0] in range(ROWS // 2, ROWS) and pos[1] in range(COLS // 2):
            bot_left += 1
        if pos[0] in range(ROWS // 2) and pos[1] in range(COLS // 2, COLS):
            top_right += 1
        if pos[0] in range(ROWS // 2, ROWS) and pos[1] in range(COLS // 2, COLS):
            bot_right += 1
    if not (top_left == top_right and bot_left == bot_right):
        return False

    grid = create_grid(robots)
    res = list((row[:len(row) // 2] == row[:len(row) // 2:-1]) for row in grid)
    return all(res)


def create_grid(robots):
    grid = [["." for _ in range(COLS)] for _ in range(ROWS)]
    for (r, c), _ in robots:
        if grid[r][c] == ".":
            grid[r][c] = "0"
        grid[r][c] = str(int(grid[r][c]) + 1)
    return grid

def draw(robots):
    for row in create_grid(robots):
        print("".join(row))

def check(robots):
    draw(robots)
    return input("Looking good? (y/n)").lower() == "y"

def part2():
    robots = parse()
    
    min_sf = float("inf")
    best_iteration = None
    
    for iteration in range(ROWS * COLS):
        current_robots = []
        for (px, py), (vx, vy) in robots:
            new_px = (px + vx * iteration) % ROWS
            new_py = (py + vy * iteration) % COLS
            current_robots.append(([new_px, new_py], (vx, vy)))
        
        quadrants = safety_value(current_robots)
        sf = functools.reduce(lambda x, y: x * y, quadrants)
        
        if sf < min_sf and sf > 0:
            min_sf = sf
            best_iteration = iteration
    
    return best_iteration

def parse():
    with open(filename) as f:
        inp = f.read()
    lines = inp.split("\n")
    robots = []
    for line in lines:
        pos, vel = line.split(" ")
        robots.append((list(map(int, pos[2:].split(","))), tuple(map(int, vel[2:].split(",")))))
    return robots

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))