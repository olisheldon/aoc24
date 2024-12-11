import sys

class Node:

    def __init__(self, val = 0):
        self.next = None
        self.val = val
    
def create_stones(list_stones):
    curr = dummy = Node()
    for stone in list_stones[:]:
        curr.next = Node(stone)
        curr = curr.next
    return dummy.next

# RULES

# 1. If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
# 2. If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
# 3. If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.

def print_ll_stones(head):
    curr = head
    s = []
    while curr:
        s.append(str(curr.val))
        curr = curr.next
    print(", ".join(s))

def part1():
    stones = create_stones(lines[:])
    for i in range(25):
        stones = blink_linked_list(stones)

    # len
    i = 0
    while stones:
        i += 1
        stones = stones.next
    return i

def blink_linked_list(head):
    curr = head
    while curr:
        curr_val_str = str(curr.val)
        if curr.val == 0:
            curr.val = 1
        elif len(curr_val_str) % 2 == 0:
            curr.val = int(curr_val_str[:len(curr_val_str) // 2])
            next_val = int(curr_val_str[len(curr_val_str) // 2:])
            old_next = curr.next
            curr.next = Node(next_val)
            curr.next.next = old_next
            curr = curr.next
        else:
            curr.val *= 2024
        curr = curr.next
    return head

def part2():
    stones = create_stones(lines[:])
    for i in range(75):
        stones = blink_linked_list(stones)
    return len(stones)

def parse():
    with open(filename) as f:
        inp = f.read()
    lines = inp.split()
    return list(map(int, lines))

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "../data/day11.test.txt"
    lines = parse()

    print(part1())
    print(part2())