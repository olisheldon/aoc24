import sys
from pathlib import Path

def find_min_tokens(a_dx, a_dy, b_dx, b_dy, prize_x, prize_y):
    min_tokens = float('inf')
    is_possible = False
    
    for a_presses in range(101):
        for b_presses in range(101):
            final_x = a_presses * a_dx + b_presses * b_dx
            final_y = a_presses * a_dy + b_presses * b_dy
            
            if final_x == prize_x and final_y == prize_y:
                tokens = a_presses * 3 + b_presses * 1
                min_tokens = min(min_tokens, tokens)
                is_possible = True
    
    return (min_tokens, is_possible)

def solve_linear_equation(a_dx, a_dy, b_dx, b_dy, prize_x, prize_y):
    det = a_dx * b_dy - a_dy * b_dx
    if det == 0:
        return None
        
    x = (prize_x * b_dy - prize_y * b_dx) / det
    y = (a_dx * prize_y - a_dy * prize_x) / det
    
    if x >= 0 and y >= 0 and x.is_integer() and y.is_integer():
        return (int(x), int(y))
    return None

def part1():
    machines = parse()
    total_tokens = 0
    
    for machine in machines:
        a_dx, a_dy, b_dx, b_dy, prize_x, prize_y = machine
        min_tokens, is_possible = find_min_tokens(a_dx, a_dy, b_dx, b_dy, prize_x, prize_y)
        if is_possible:
            total_tokens += min_tokens
    
    return total_tokens
    
def part2():
    machines = parse()
    total_tokens = 0
    
    for machine in machines:
        a_dx, a_dy, b_dx, b_dy, prize_x, prize_y = machine
        prize_x += 10000000000000
        prize_y += 10000000000000
        
        solution = solve_linear_equation(a_dx, a_dy, b_dx, b_dy, prize_x, prize_y)
        if solution:
            a_presses, b_presses = solution
            tokens = a_presses * 3 + b_presses * 1
            total_tokens += tokens
    
    return total_tokens

def parse():
    with open(filename) as f:
        inp = f.read().strip()
    
    machines = [m for m in inp.split("\n\n") if m.strip()]
    res = [] # [(a_dx, a_dy, b_dx, b_dy, x, y)]
    for machine in machines:
        lines = [line for line in machine.split("\n") if line.strip()]
        if len(lines) != 3:
            continue
            
        button_a, button_b, prize = lines
        a_dx = int(button_a.split(": ")[1][2:].split(",")[0])
        a_dy = int(button_a.split(", Y+")[-1])
        b_dx = int(button_b.split(": ")[1][2:].split(",")[0])
        b_dy = int(button_b.split(", Y+")[-1])
        x = int(prize.split(": ")[1][2:].split(",")[0])
        y = int(prize.split(", Y=")[-1])
        res.append((a_dx, a_dy, b_dx, b_dy, x, y))
    return res

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    print("part1=" + str(part1()))
    print("part2=" + str(part2()))