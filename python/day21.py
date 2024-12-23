import sys
from pathlib import Path
from collections import deque
from itertools import product

NEIGHBOURS = ((1, 0, "v"), (-1, 0, "^"), (0, 1, ">"), (0, -1, "<"))

def solve(string, keypad):
    ROWS, COLS = len(keypad), len(keypad[0])
    
    pos = {}
    for r in range(ROWS):
        for c in range(COLS):
            if keypad[r][c] is not None:
                pos[keypad[r][c]] = (r, c)
    
    # map of every button pair to sequence to move between
    seqs = {}
    q = deque()
    for u in pos:
        for v in pos:
            if u == v:
                seqs[(u, v)] = ["A"]
                continue
            possibilities = []
            q = deque([(pos[u], "")]) # (r, c), sequence_to_get_there
            optimal = float("inf")
            while q:
                (r, c), moves = q.popleft()
                for dr, dc, m in NEIGHBOURS:
                    if (
                        r + dr not in range(ROWS) or
                        c + dc not in range(COLS) or
                        keypad[r + dr][c + dc] is None
                    ):
                        continue
                    
                    if keypad[r + dr][c + dc] == v:
                        if optimal < len(moves) + 1:
                            break
                        optimal = len(moves) + 1
                        possibilities.append(moves + m + "A")
                    else:
                        q.append(((r + dr, c + dc), moves + m))
                else:
                    continue
                break
            seqs[(u, v)] = possibilities
    
    options = [seqs[(u, v)] for u, v in zip("A" + string, string)]
    return ["".join(u) for u in product(*options)]

def part1():
    num_keypad = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [None, "0", "A"]
    ]
    dir_keypad = [
        [None, "^", "A"],
        ["<", "v", ">"]
    ]
    
    codes = parse()
    total = 0
    for code in codes:
        robot1 = solve(code, num_keypad)
        next = robot1
        for _ in range(2):
            possible_next = []
            for seq in next:
                possible_next += solve(seq, dir_keypad)
            minlen = min(map(len, possible_next))
            next = list(filter(lambda u: len(u) == minlen, possible_next))
        length = len(next[0])
        complexity = length * int(code[:-1])
        total += complexity
    return total

def part2():
    return "INCOMPLETE"

def parse():
    with open(filename) as f:
        inp = f.read()
    return inp.split("\n")

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))
