import heapq
from collections import defaultdict

with open("../../data/day1.txt") as f:
    inp = f.read()

lines = inp.split("\n")
values = [tuple(map(int, line.split())) for line in lines]

def part1():

    left = []
    right = []

    for l, r in values:
        heapq.heappush(left, l)
        heapq.heappush(right, r)

    res = 0
    while left and right:
        res += abs(heapq.heappop(left) - heapq.heappop(right))
    assert(len(left) == len(right) == 0)
    return res

def part2():

    left, right = [], defaultdict(int)

    for l, r in values:
        left.append(l)
        right[r] += 1
    
    res = 0
    for l in left:
        res += l * right[l]
    return res


if __name__ == "__main__":
    print(f"{part1()=}")
    print(f"{part2()=}")