import sys
from typing import Callable
from pathlib import Path

def poss_sums(target, nums, ops: Callable):
    def dfs(i, curr):
        if i == len(nums):
            return curr == target
        if curr > target:
            return False
        
        return (
            any(dfs(i + 1, op(curr, nums[i])) for op in ops)
            )
    return dfs(0, 0)

def part1():
    return sum(target for target, nums in lines if poss_sums(target, nums, (int.__add__, int.__mul__)))

def part2():
    concat = lambda x, y: int(str(x) + str(y))
    return sum(target for target, nums in lines if poss_sums(target, nums, (int.__add__, int.__mul__, concat)))

def parse():
    with open(filename) as f:
        inp = f.read()
    lines = inp.split("\n")
    strs = [list(map(str.strip, line.split(":"))) for line in lines]
    return [[int(s[0]), list(map(int, s[1].split()))] for s in strs]

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    lines = parse()

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))