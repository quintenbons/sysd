#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <number_of_calls> <file_path>"
    exit 1
fi

# Extract arguments
num_calls=$1
file_path=$2

# Loop to call the command X times
for ((i=0; i<$num_calls; i++)); do
    ./sysd/src/make.py "$file_path" --no-nfs --perf --index "$i"
done
