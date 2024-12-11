import sys

# RULES

# 1. If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
# 2. If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
# 3. If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.

def blink(stones):
    i = 0
    while i < len(stones):
        stones_i_str = str(stones[i])
        if stones[i] == 0:
            stones[i] = 1
        elif len(stones_i_str) % 2 == 0:
            stones[i] = int(stones_i_str[:len(stones_i_str) // 2])
            stones.insert(i, int(stones_i_str[len(stones_i_str) // 2:]))
            i += 1
        else:
            stones[i] *= 2024
        i += 1
    return stones

def part1():
    stones = lines[:]
    for _ in range(25):
        stones = blink(stones)
    return len(stones)

def part2():
    stones = lines[:]
    for i in range(75):
        print(i)
        stones = blink(stones)
    return len(stones)

def parse():
    with open(filename) as f:
        inp = f.read()
    lines = inp.split()
    return list(map(int, lines))

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day11.txt"
    lines = parse()

    print(part1())
    print(part2())