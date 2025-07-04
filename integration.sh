#!/bin/bash

# Usage: ./integration.sh [python|cpp|both] [day]
# Default is both if no argument is given
MODE=${1:-both}
DAY_ARG="$2"

known_answers="known_answers.txt"
python_answers="python_answers.txt"
cpp_answers="cpp_answers.txt"

run_python() {
  echo "Running Python solutions..."
  if [ -n "$DAY_ARG" ]; then
    DAY_NUM=$(printf "%d" "$DAY_ARG" 2>/dev/null)
    pyfile="./python/day$DAY_NUM.py"
    data_file="$(realpath data/day$DAY_NUM.txt)"
    if [ -f "$pyfile" ]; then
      python "$pyfile" "$data_file" | tee "$python_answers"
    else
      echo "Python file $pyfile not found"
    fi
  else
    find ./python -name 'day*.py' | sort -V | while read file; do
      exe_name="$(basename $file .py)"
      echo "$exe_name"
      python "$file" "$(realpath data/$(basename "$file" .py).txt)"
      echo
    done | tee "$python_answers"
  fi
}

run_cpp() {
  echo "Building and running C++ solutions..."
  make -C ./cpp > /dev/null
  if [ -n "$DAY_ARG" ]; then
    DAY_NUM=$(printf "%d" "$DAY_ARG" 2>/dev/null)
    exe="./cpp/bin/day$DAY_NUM"
    data_file="$(realpath data/day$DAY_NUM.txt)"
    if [ -x "$exe" ]; then
      "$exe" "$data_file" | tee "$cpp_answers"
    else
      echo "Executable $exe not found or not executable"
    fi
  else
    find ./cpp -maxdepth 1 -name 'day*.cpp' | sort -V | while read cppfile; do
      exe="./cpp/bin/$(basename ${cppfile%.cpp})"
      echo "$(basename $exe)"
      if [ -x "$exe" ]; then
        "$exe" "$(realpath data/$(basename "$exe").txt)"
      else
        echo "Executable $exe not found or not executable"
      fi
      echo
    done | tee "$cpp_answers"
  fi
}

case "$MODE" in
  python)
    run_python
    if [ -n "$DAY_ARG" ]; then
      DAY_NUM=$(printf "%d" "$DAY_ARG" 2>/dev/null)
      PART1_LINE=$((4 * (DAY_NUM - 1) + 2))
      PART2_LINE=$((4 * (DAY_NUM - 1) + 3))
      expected=$(sed -n -e "${PART1_LINE}p" -e "${PART2_LINE}p" "$known_answers")
      actual=$(awk 'NF' "$python_answers" | head -n 2)
      if diff <(echo "$expected") <(echo "$actual") > /dev/null; then
        echo ""
        echo "✅ Python day$DAY_NUM: Correct!"
      else
        echo ""
        echo "❌ Python day$DAY_NUM: Incorrect. Diff below:"
        diff <(echo "$expected") <(echo "$actual")
      fi
    else
      diff "$known_answers" "$python_answers"
    fi
    ;;
  cpp)
    run_cpp
    if [ -n "$DAY_ARG" ]; then
      DAY_NUM=$(printf "%d" "$DAY_ARG" 2>/dev/null)
      PART1_LINE=$((4 * (DAY_NUM - 1) + 2))
      PART2_LINE=$((4 * (DAY_NUM - 1) + 3))
      expected=$(sed -n -e "${PART1_LINE}p" -e "${PART2_LINE}p" "$known_answers")
      actual=$(awk 'NF' "$cpp_answers" | head -n 2)
      if diff <(echo "$expected") <(echo "$actual") > /dev/null; then
        echo ""
        echo "✅ C++ day$DAY_NUM: Correct!"
      else
        echo ""
        echo "❌ C++ day$DAY_NUM: Incorrect. Diff below:"
        diff <(echo "$expected") <(echo "$actual")
      fi
    else
      diff "$known_answers" "$cpp_answers"
    fi
    ;;
  both)
    run_python
    run_cpp
    echo "Diff for Python:"
    diff "$known_answers" "$python_answers"
    echo "Diff for C++:"
    diff "$known_answers" "$cpp_answers"
    ;;
  *)
    echo "Usage: $0 [python|cpp|both] [day]"
    exit 1
    ;;
esac