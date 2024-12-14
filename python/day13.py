import sys
sys.setrecursionlimit(2147483647)

def part1():
    
    res = set()
    def dfs(x, y, tokens):
        if x < 0 or y < 0:
            return
        if x == 0 and y == 0:
            res.add(tokens)
            return
        
        dfs(x - a_dx, y - a_dy, tokens - 1)
        dfs(x - b_dx, y - b_dy, tokens - 3)
    
    machines = parse()
    for a_dx, a_dy, b_dx, b_dy, x, y in machines:
        dfs(x, y, 0)
    return min(res)
    

def part2():
    pass

def parse():
    with open(filename) as f:
        inp = f.read()
    
    machines = inp.split("\n\n")
    res = [] # [(a_dx, a_dy, b_dx, b_dy, x, y)]
    for machine in machines:
        button_a, button_b, prize = machine.split("\n")
        a_dx = int(button_a.split(": ")[1][2:].split(",")[0])
        a_dy = int(button_a.split(", Y+")[-1])
        b_dx = int(button_b.split(": ")[1][2:].split(",")[0])
        b_dy = int(button_b.split(", Y+")[-1])
        x = int(prize.split(": ")[1][2:].split(",")[0])
        y = int(prize.split(", Y=")[-1])
        res.append((a_dx, a_dy, b_dx, b_dy, x, y))
    return res

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day13.test.txt"

    print(part1())
    print(part2())