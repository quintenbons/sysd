#!/bin/bash

# Liste des nœuds réservés
NODES=$(oarprint hostnames)

# Commande pour lancer les workers
WORKER_CMD="celery -A your_project worker --loglevel=info"

# Lancer les workers
for NODE in $NODES; do
    ssh jubourseau@$NODE "$WORKER_CMD" &
done