import sys
from pathlib import Path

EMPTY = -1


def checksum(nums):
    return sum(i * num for i, num in enumerate(nums))

def part1():
    
    expanded = []
    for i, count in enumerate(disk_map):
        if i % 2:
            expanded += [EMPTY] * count
        else:
            expanded += [i // 2] * count

    l, r = 0, len(expanded) - 1
    while l < r:
        if expanded[l] != EMPTY:
            l += 1
        elif expanded[r] == EMPTY:
            r -= 1
        else:
            expanded[l] = expanded[r]
            expanded[r] = EMPTY
            l += 1
            r -= 1
    expanded = list(filter(lambda x: x != EMPTY, expanded))
    return checksum(expanded)

def part2():
    return "INCOMPLETE"    
        
    def convert(expanded):
        res = []
        for file_id, count in expanded:
            if file_id == EMPTY:
                file_id = 0
            res += [file_id] * count
        return res
    
    assign_file_id = lambda x: x // 2 if not x % 2 else EMPTY
    expanded = [[assign_file_id(i), count] for i, count in enumerate(disk_map)]

    r = len(expanded) - 1
    while r > 0:
        if expanded[r][0] == EMPTY:
            r -= 1
            continue
        for l, (file_id, count) in enumerate(expanded):
            if l > r:
                break
            if file_id != EMPTY:
                continue
            move_file_id, move_count = expanded[r]
            if move_count > count:
                continue
            
            expanded[r][0] = EMPTY
            expanded[l][1] -= move_count
            expanded.insert(l, [move_file_id, move_count])
            r -= 1
            break
        else:
            break
        r -= 1
    return checksum(convert(expanded))

def parse():
    with open(filename) as f:
        inp = f.read()
    return list(map(int, list(inp)))

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    disk_map = parse()

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))