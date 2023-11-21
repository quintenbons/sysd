#!/bin/bash

# Liste des nœuds réservés
NODES=$(oarprint hostnames)

# Nettoyage
for NODE in $NODES; do
    ssh jubourseau@$NODE 'killall celery'
    # Autres commandes de nettoyage si nécessaire
done