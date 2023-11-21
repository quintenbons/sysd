#!/bin/bash

JOB_ID="2313550"
NODES=$(oarstat -f -j $JOB_ID | grep "assigned_hostnames" | awk '{print $3}' | tr '+' '\n')

# Commande pour lancer les workers
WORKER_CMD="export PATH=../:$PATH; celery -A runner worker --loglevel=info"

# Lancer les workers
for NODE in $NODES; do
    ssh jubourseau@$NODE "$WORKER_CMD" &
done