#!/bin/bash

# RUN SOLUTIONS
find ./python -name 'day*.py' | sort -V | while read file; do
  echo "$file"
  python "$file" "$(realpath data/$(basename "$file" .py).txt)"
  echo
done | tee python_answers.txt

known_answers="known_answers.txt"
python_answers="python_answers.txt"

diff $known_answers $python_answers