import sys
from pathlib import Path

def part1():
    return "INCOMPLETE"

def part2():
    return "INCOMPLETE"

def parse():
    with open(filename) as f:
        inp = f.read()

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/${Path(__file__).stem}.txt"

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))
