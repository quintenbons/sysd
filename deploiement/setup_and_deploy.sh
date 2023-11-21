#!/bin/bash

SOURCE_CODE_PATH="../src"

JOB_ID="2313550"

NODES=$(oarstat -f -j $JOB_ID | grep "assigned_hostnames" | cut -d ' ' -f 3)

for NODE in $NODES; do
    echo "Configuration du nœud $NODE"
    echo "pwd: $(pwd)"
    scp -r $SOURCE_CODE_PATH jubourseau@$NODE:/ # utiliser var d'env

    ssh jubourseau@$NODE 'pip install "celery[librabbitmq,redis,auth,msgpack]" amqp'

    # autre configs?
done
