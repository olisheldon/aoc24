#!/bin/bash

# Usage: ./integration.sh [python|cpp|both]
# Default is both if no argument is given
MODE=${1:-both}

known_answers="known_answers.txt"
python_answers="python_answers.txt"
cpp_answers="cpp_answers.txt"

run_python() {
  echo "Running Python solutions..."
  find ./python -name 'day*.py' | sort -V | while read file; do
    echo "$(basename $file .py)"
    python "$file" "$(realpath data/$(basename "$file" .py).txt)"
    echo
  done | tee "$python_answers"
}

run_cpp() {
  echo "Running C++ solutions..."
  find ./cpp -maxdepth 1 -name 'day*.cpp' | sort -V | while read cppfile; do
    exe="${cppfile%.cpp}"
    echo "$(basename $cppfile .cpp)"
    g++ -std=c++17 -O2 -o "$exe" "$cppfile"
    if [ $? -eq 0 ]; then
      "$exe" "$(realpath data/$(basename "$cppfile" .cpp).txt)"
    else
      echo "Compilation failed for $cppfile"
    fi
    echo
  done | tee "$cpp_answers"
}

case "$MODE" in
  python)
    run_python
    diff "$known_answers" "$python_answers"
    ;;
  cpp)
    run_cpp
    diff "$known_answers" "$cpp_answers"
    ;;
  both)
    run_python
    run_cpp
    echo "\nDiff for Python:"
    diff "$known_answers" "$python_answers"
    echo "\nDiff for C++:"
    diff "$known_answers" "$cpp_answers"
    ;;
  *)
    echo "Usage: $0 [python|cpp|both]"
    exit 1
    ;;
esac