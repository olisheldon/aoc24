import sys

def part1():
    towels, target_towels = parse()
    count = []
    for target_towel in target_towels:
        res = [False] * (len(target_towel) + 1)
        res[-1] = True
        for i in range(len(target_towel) - 1, -1, -1):
            for towel in towels:
                if i + len(towel) <= len(target_towel) and towel == target_towel[ i : i + len(towel) ]:
                    res[i] = max(res[i], res[i + len(towel)])
        count.append(res[0])
    return sum(count)

def part2():
    towels, target_towels = parse()
    count = []
    for target_towel in target_towels:
        res = [0] * (len(target_towel) + 1)
        res[-1] = 1
        for i in range(len(target_towel) - 1, -1, -1):
            for towel in towels:
                if i + len(towel) <= len(target_towel) and towel == target_towel[ i : i + len(towel) ]:
                    res[i] += res[i + len(towel)]
        count.append(res[0])
    return sum(count)

def parse():
    with open(filename) as f:
        inp = f.read()
    towels, target_towels = inp.split("\n\n")
    return towels.split(", "), target_towels.split("\n")

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day19.txt"

    print(part1())
    print(part2())
