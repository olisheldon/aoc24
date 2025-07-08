#!/usr/bin/env python3

import requests
import sys
import time

def get_input(day: int) -> str:
    print(f"Getting input for day {day}...")
    url = "https://adventofcode.com/2024/day/"+str(day)+"/input"
    headers = {'Cookie': 'session='+sessionToken}
    r = requests.get(url, headers=headers)
 
    if r.status_code == 200:
        return r.text.strip("\n")
    else:
        sys.exit(f"/api/alerts response: {r.status_code}: {r.reason} \n{r.content}")

def main() -> None:
    for day in range(1, 26):
        text = get_input(day)
        with open(f"data/day{day}.txt", "w") as f:
            f.write(text)
        time.sleep(1)

if __name__ == "__main__":
    sessionToken = input("Enter your session token: ")
    main()