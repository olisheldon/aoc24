## Advent of Code 2024 — Python solutions

This repository contains my solutions for Advent of Code 2024.
Read the write-ups, problem breakdowns, and solution discussions on my site: [Advent of Code 2024 write-ups](https://olisheldon.github.io/projects/advent_of_code24.html).

### What’s in this repo
- **Python solutions (`python/`)**: `day1.py` … `day25.py`.
- **C++ solutions (`cpp/`)**: `day1.cpp` … `day25.cpp`.
- **Inputs (`data/`)**: `dayN.txt` puzzle inputs (one per day).
- **Integration and verification**:
  - `integration.sh`: helper script to run solutions and compare outputs to `known_answers.txt`.
  - `known_answers.txt`: canonical expected outputs (part1/part2) for each day.
  - `python_answers.txt`: outputs captured from recent Python runs.
  - `differences.txt`: any known deltas discovered during development.
- **Input fetcher**: `scrape.py` — fetches your personal AoC inputs into `data/` using your session cookie.

### Getting puzzle inputs
Your AoC input is tied to your account. To populate `data/dayN.txt` for all days:

```bash
python scrape.py
# When prompted, paste your Advent of Code session token (from your browser cookies)
```

This will create `data/day1.txt` … `data/day25.txt`. You can also supply your own input files manually.

### Running solutions
- **Run all Python days and capture answers**
```bash
./integration.sh python
```
- **Run a single Python day (e.g., day 5)**
```bash
./integration.sh python 5
# or run directly
python python/day5.py data/day5.txt
```

### Verifying correctness
`integration.sh` compares recent run outputs to `known_answers.txt`:

- When running a single day, it prints ✅/❌ with a diff if mismatched.
- When running all days, it diffs `python_answers.txt` against `known_answers.txt`.

### Project structure
```
aoc24/
  data/
    dayN.txt          # puzzle inputs
  python/
    dayN.py           # original Python implementations
  cpp/
    dayN.cpp          # cpp translations of Python solutions completed through AI agents
  integration.sh      # run-and-verify helper
  known_answers.txt   # expected outputs
  python_answers.txt  # last Python run outputs
  differences.txt     # any noted diffs during development
  scrape.py           # fetches inputs with AoC session token
  README.md
```

### AI Agents
After finishing the Python work and the write-ups, I experimented with the usefulness of automatically translating the Python solutions into C++ using AI agents. The C++ code lives in `cpp/` and can be built. claude-3-5-sonnet 20241022 was used and, together with MCP for automatic github issue and PR creation, managed to one-shot ~90% of them.
