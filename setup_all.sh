#!/bin/bash

SCRIPT_PATH="deploiement"

chmod +x $SCRIPT_PATH/reserve_nodes.sh
chmod +x $SCRIPT_PATH/setup_and_deploy.sh
chmod +x $SCRIPT_PATH/start_workers.sh
chmod +x $SCRIPT_PATH/cleanup.sh

echo "Réservation des nœuds..."
# $SCRIPT_PATH/reserve_nodes.sh
# if [ $? -ne 0 ]; then
#     echo "Erreur lors de la réservation des nœuds."
#     exit 1
# fi

sleep 120

echo "Configuration et déploiement..."
$SCRIPT_PATH/setup_and_deploy.sh
if [ $? -ne 0 ]; then
    echo "Erreur lors de la configuration et du déploiement."
    exit 1
fi

echo "Démarrage des workers Celery..."
$SCRIPT_PATH/start_workers.sh
if [ $? -ne 0 ]; then
    echo "Erreur lors du démarrage des workers."
    exit 1
fi

echo "Déploiement terminé."