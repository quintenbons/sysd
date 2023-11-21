#!/bin/bash

# Nombre de nœuds à réserver
NODES=5
# Durée de la réservation
WALLTIME="2:00:00"

# Commande de réservation
oarsub -l nodes=$NODES,walltime=$WALLTIME "sleep 3600"