import sys
from pathlib import Path
from collections import Counter
from itertools import chain

def mix(secret_number, mixer):
    return secret_number ^ mixer

def prune(secret_number):
    return secret_number % 16777216

def evolve(secret_number):
    secret_number = mix(secret_number, secret_number * 64)
    secret_number = prune(secret_number)
    
    secret_number = mix(secret_number, int(secret_number / 32))
    secret_number = prune(secret_number)
    
    secret_number = mix(secret_number, secret_number * 2048)
    return prune(secret_number)

def part1():
    secret_numbers = parse()
    
    res = 0
    for secret_number in secret_numbers:
        for _ in range(2000):
            secret_number = evolve(secret_number)
        res += secret_number
    return res

def part2():
    secret_numbers = parse()
    all_price_changes_to_prof = []
    
    for secret_number in secret_numbers:
        prices = []
        price_differences = []
        for _ in range(2000):
            prices.append(int(str(secret_number)[-1]))
            secret_number = evolve(secret_number)
        for (price, next_price) in zip(prices, prices[1:]):
            price_differences.append(next_price - price)
        price_changes_to_prof = {}
        for i in range(len(prices) - 4):
            price_changes = price_differences[i : i + 4]
            if tuple(price_changes) in price_changes_to_prof:
                continue
            price_changes_to_prof[tuple(price_changes)] = prices[i + 4]
        all_price_changes_to_prof.append(price_changes_to_prof)
    counter = Counter()
    for p in chain(all_price_changes_to_prof):
        counter += Counter(p)
    return counter[max(counter, key=counter.get)]

def parse():
    with open(filename) as f:
        inp = f.read()
    return list(map(int, inp.split("\n")))

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))
