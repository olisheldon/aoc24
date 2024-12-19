import sys
from collections import defaultdict, deque
from functools import cmp_to_key
from pathlib import Path

def valid(page, k_before_v):
    for i, v in enumerate(page):
        for j in range(i + 1, len(page)):
            if v not in k_before_v[page[j]]:
                return False
    return True

def part1():
    k_before_v = defaultdict(set)
    v_before_k = defaultdict(set)
    for X, Y in page_ordering_rules:
        v_before_k[X].add(Y)
        k_before_v[Y].add(X)
    
    valid_pages = []
    for page in pages:
        if valid(page, k_before_v):
            valid_pages.append(page)
    
    res = 0
    for valid_page in valid_pages:
        res += valid_page[len(valid_page) // 2]
    return res

def part2():
    cache = {}
    for x, y in page_ordering_rules:
        cache[(x, y)] = -1
        cache[(y, x)] = 1
    
    def is_ordered(update):
        for i in range(len(update)):
            for j in range(i + 1, len(update)):
                key = (update[i], update[j])
                if key in cache and cache[key] == 1:
                    return False
        return True
    
    modified_pages = []
    for page in pages:
        if is_ordered(page):
            continue
        page.sort(key=cmp_to_key(lambda x, y: cache.get((x, y), 0)))
        modified_pages.append(page)
    
    res = 0
    for valid_page in modified_pages:
        res += valid_page[len(valid_page) // 2]
    return res

def parse():
    
    with open(filename) as f:
        inp = f.read()

    page_ordering_rules, pages = inp.split("\n\n")
    
    page_ordering_rules = list(map(lambda x: x.split("|"), page_ordering_rules.split("\n")))
    for i in range(len(page_ordering_rules)):
        page_ordering_rules[i] = list(map(int, page_ordering_rules[i]))
        
    pages = list(map(lambda x: x.split(","), pages.split("\n")))
    for i in range(len(pages)):
        pages[i] = list(map(int, pages[i]))

    return page_ordering_rules, pages

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    page_ordering_rules, pages = parse()
    
    print("part1=" + str(part1()))
    print("part2=" + str(part2()))