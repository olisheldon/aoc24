import sys

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

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day2.txt"
    with open(filename) as f:
        inp = f.read()

    lines = inp.split("\n")
    reports = [tuple(map(int, line.split())) for line in lines]

    print(f"{part1()=}")
    print(f"{part2()=}")