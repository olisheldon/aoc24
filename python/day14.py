import sys
import functools

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

def part2():
    pass

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

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day14.txt"

    print(f"{part1()=}")
    print(f"{part2()=}")