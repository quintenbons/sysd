#!/bin/bash

SOURCE_CODE_PATH="../src"

NODES=$(oarprint hostnames)

for NODE in $NODES; do
    echo "Configuration du nœud $NODE"
    echo "pwd: $(pwd)"
    scp -r $SOURCE_CODE_PATH jubourseau@$NODE:/ # utiliser var d'env

    ssh jubourseau@$NODE 'sudo apt-get update && sudo apt-get install -y python3 python3-pip celery'

    # autre configs?
done
