import sys
from pathlib import Path
from collections import deque
from itertools import product
from functools import cache

NEIGHBOURS = ((1, 0, "v"), (-1, 0, "^"), (0, 1, ">"), (0, -1, "<"))
NUM_KEYPAD = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", "A"]
]
DIR_KEYPAD = [
    [None, "^", "A"],
    ["<", "v", ">"]
]

def compute_seqs(keypad):
    
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
    return seqs

def solve(string, seqs):
    options = [seqs[(u, v)] for u, v in zip("A" + string, string)]
    return ["".join(u) for u in product(*options)]

def part1():
    
    codes = parse()
    total = 0
    for code in codes:
        robot1 = solve(code, compute_seqs(NUM_KEYPAD))
        next = robot1
        for _ in range(2):
            possible_next = []
            for seq in next:
                possible_next += solve(seq, compute_seqs(DIR_KEYPAD))
            minlen = min(map(len, possible_next))
            next = list(filter(lambda u: len(u) == minlen, possible_next))
        length = len(next[0])
        complexity = length * int(code[:-1])
        total += complexity
    return total


def part2():
    
    dir_seqs = compute_seqs(DIR_KEYPAD)
    dir_lens = {key : len(value[0]) for key, value in dir_seqs.items()}
    num_seqs = compute_seqs(NUM_KEYPAD)
    
    @cache
    def compute_length(seq, depth=25):
        if depth == 1:
            return sum(dir_lens[(u, v)] for u, v in zip("A" + seq, seq))
        length = 0
        for x, y in zip("A" + seq, seq):
            length += min(compute_length(subseq, depth -1) for subseq in dir_seqs[(x, y)])
        return length
    
    codes = parse()
    total = 0
    for code in codes:
        inputs = solve(code, num_seqs)
        optimal_length = min(map(compute_length, inputs))
        total += optimal_length * int(code[:-1])
    return total


def parse():
    with open(filename) as f:
        inp = f.read()
    return inp.split("\n")

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))
