import sys
import re

def part1():
    pattern = r"mul\((\d+),(\d+)\)"
    matches = re.findall(pattern, lines)
    matches = [tuple(map(int, tup)) for tup in matches]
    print(matches)
    return sum(x * y for x, y in matches)

def part2():
    # Use regular expression to find all instances of "mul(number1,number2)", "do()" and "don't()"
    pattern = r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)"
    matches = [(match.group(), match.start()) for match in re.finditer(pattern, lines)]
    
    # Convert matches to a list of tuples with integers and their indices
    results = []
    for match, index in matches:
        if match.startswith("mul"):
            num1, num2 = re.findall(r'\d+', match)
            results.append(((int(num1), int(num2)), index))
        else:
            results.append((match, index))
    
    res = 0
    do = True
    for val, i in results:
        if val == "don't()":
            do = False
        elif val == "do()":
            do = True
        elif do:
            res += val[0] * val[1]
    return res

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day3.txt"
    with open(filename) as f:
        inp = f.read()

    lines = inp

    print(f"{part1()=}")
    print(f"{part2()=}")