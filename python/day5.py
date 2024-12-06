import sys
from collections import defaultdict, deque

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
    k_before_v = defaultdict(set)
    v_before_k = defaultdict(set)
    for X, Y in page_ordering_rules:
        v_before_k[X].add(Y)
        k_before_v[Y].add(X)
    
    valid_pages = []
    invalid_pages = []
    for page in pages:
        if valid(page, k_before_v):
            valid_pages.append(page)
        else:
            invalid_pages.append(page)

    def findOrder(nums: list[int], prerequisites):
        indegree = defaultdict(int)
        adj = defaultdict(list)
        for src, dst in prerequisites:
            indegree[dst] += 1
            adj[src].append(dst)

        q = deque()
        for n in nums:
            if indegree[n] == 0:
                q.append(n)
        
        finish, output = 0, []
        while q:
            node = q.popleft()
            output.append(node)
            finish += 1
            for nei in adj[node]:
                indegree[nei] -= 1
                if indegree[nei] == 0:
                    q.append(nei)
        
        return output[::-1]
    
    
    corrected_pages = []
    
    for invalid_page in invalid_pages:
        corrected_pages.append(findOrder(invalid_page, page_ordering_rules))
    print(corrected_pages)
      
    res = 0
    for valid_page in corrected_pages:
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

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day5.test.txt"
    page_ordering_rules, pages = parse()
    
    print(f"{part1()=}")
    print(f"{part2()=}")