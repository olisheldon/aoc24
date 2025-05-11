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
    files = {}
    blanks = []
    
    file_id = 0
    position = 0
    
    for i, count in enumerate(disk_map):
        if i % 2 == 0:
            files[file_id] = (position, count)
            file_id += 1
        else:
            blanks.append((position, count))
        position += count
    
    for fid in range(file_id - 1, -1, -1):
        pos, size = files[fid]
        
        best_pos = -1
        best_blank_idx = -1
        
        for i, (blank_pos, blank_len) in enumerate(blanks):
            if blank_pos >= pos:
                break
                
            if blank_len >= size:
                best_pos = blank_pos
                best_blank_idx = i
                break
        
        if best_pos != -1:
            files[fid] = (best_pos, size)
            
            if size == blanks[best_blank_idx][1]:
                blanks.pop(best_blank_idx)
            else:
                blanks[best_blank_idx] = (best_pos + size, blanks[best_blank_idx][1] - size)
    
    total = 0
    for fid, (pos, size) in files.items():
        for x in range(pos, pos + size):
            total += fid * x
            
    return total

def parse():
    with open(filename) as f:
        inp = f.read()
    return list(map(int, list(inp)))

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    disk_map = parse()

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))