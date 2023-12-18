#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <number_of_calls> <file_path>"
    exit 1
fi

WORKER_NODES=$(jq -r '.workerNodes | join(" ")' $HOME/g5k_deploy/info.json)
MASTER_NODE=$(jq -r '.masterNode' $HOME/g5k_deploy/info.json)
WORK_PATH="/tmp/dist"

function del_tmp_dist {
    # Remote delete the tmp dist with ssh
    for node in $WORKER_NODES; do
        ssh $node "rm -rf $WORK_PATH/*"
    done
    ssh $MASTER_NODE "rm -rf $WORK_PATH/*"
}

# Extract arguments
num_calls=$1
file_path=$2

# Loop to call the command X times
for ((i=0; i<$num_calls; i++)); do
    del_tmp_dist
    ./sysd/src/make.py "$file_path" --no-nfs --perf --index "$i"
done
