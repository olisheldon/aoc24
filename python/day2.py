import sys
from pathlib import Path

def safe(report):
    return ((all(x < y for x, y in zip(report, report[1:])) or 
            all(x > y for x, y in zip(report, report[1:]))) and 
            all(1 <= abs(x - y) <= 3 for x, y in zip(report, report[1:])))

def part1():
    return sum(safe(report) for report in reports)

def part2():
    mod_reports = ((report[:i] + report[i + 1:] for i in range(len(report))) for report in reports)
    return sum(any(safe(report) for report in possible_reports) for possible_reports in mod_reports)

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()

    lines = inp.split("\n")
    reports = [tuple(map(int, line.split())) for line in lines]

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))