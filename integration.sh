#!/bin/bash

# RUN SOLUTIONS
find ./python/**/*.py -exec bash -c 'echo {}; python3 {} $(realpath data/$(basename "{}" .py).txt)' \; > python_answers.txt
find ./cpp/**/*.cpp -exec bash -c 'echo {}; g++ {} -o $(basename {} .cpp).o && ./$(basename {} .cpp).o $(realpath data/$(basename "{}" .cpp).txt)' \; > cpp_answers.txt

# Function to extract and compare sections
compare_sections() {
    local file1="$1"
    local file2="$2"
    local tmp1=$(mktemp)
    local tmp2=$(mktemp)

    awk '/^day|^\.\/cpp|^\.\/python/ {if (NR>1) print "---"} {print}' $file1 | \
    awk 'BEGIN{RS="---"} {print substr($0, index($0, "\n") + 1) > "'$tmp1'"}' > /dev/null

    awk '/^day|^\.\/cpp|^\.\/python/ {if (NR>1) print "---"} {print}' $file2 | \
    awk 'BEGIN{RS="---"} {print substr($0, index($0, "\n") + 1) > "'$tmp2'"}' > /dev/null

    diff_result=$(diff $tmp1 $tmp2)
    if [ -n "$diff_result" ]; then
        echo "Differences found in" ${file2}
        echo "$diff_result"
    else
        echo "No differences found in" ${file2}
    fi

    rm $tmp1 $tmp2
}


known_answers="known_answers.txt"
python_answers="python_answers.txt"
cpp_answers="cpp_answers.txt"

compare_sections "$known_answers" "$python_answers"
# compare_sections "$known_answers" "$cpp_answers"

