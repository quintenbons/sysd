#!/bin/bash
# Configuration de l'environnement
echo "Configuration de l'environnement"
mkdir -p dist

# Installation des dépendances
echo "Installation de Celery et autres dépendances"
pip install "celery[librabbitmq,redis,auth,msgpack]" amqp

# Réservation des nœuds
echo "Réservation des nœuds"
NODES=2
WALLTIME="2:00:00"
JSON_RESULT=$(oarsub -l nodes=$NODES,walltime=$WALLTIME -J "sleep infinity")
JOB_ID=$(echo $JSON_RESULT | jq -r '.job_id')

# Attente que la réservation soit active
echo "Job en cours de réservation JOB_ID: $JOB_ID..."
while true; do
    STATE=$(oarstat -s -J -j $JOB_ID | jq -r '."'"$JOB_ID"'"')
    if [ "$STATE" == "Running" ]; then
        echo "Réservation active."
        break
    else
        echo "Réservation en attente... (État: $STATE)"
    fi
    sleep 5 # Ease
done

# Récupération des noms d'hôte assignés
NODES=$(oarstat -j $JOB_ID -p | oarprint host -f -)
MASTER_NODE=$(echo $NODES | awk '{print $1}') # 1rst
WORKER_NODES=$(echo $NODES | cut -d' ' -f2-) # all but 1rst

REPO_PATH=$HOME/sysd
MASTER_CMD="source $REPO_PATH/deploiement/start_master.sh"
WORKER_CMD="source $REPO_PATH/deploiement/start_worker.sh"

function announce() {
    echo "JOB_ID: $JOB_ID"
    echo "MASTER_NODE: $MASTER_NODE"
    echo "WORKER_NODES: $WORKER_NODES"
}

if [ "$1" == "PREMATURE_STOP" ]; then
    echo "Stopping before deployment as asked by parameter 1: $1."
    announce
    exit 0
fi

# Must be synchronous
echo "Lancement du noeud maître"
BROKER_HOST=$MASTER_NODE
BROKER_PORT=5672
sed -i "s/^broker_host = .*$/broker_host = \"$BROKER_HOST\"/" $REPO_PATH/src/constants.py
sed -i "s/^broker_port = .*$/broker_port = $BROKER_PORT/" $REPO_PATH/src/constants.py

ssh $USER@$MASTER_NODE "$MASTER_CMD"

sleep 1

# Lancer les workers
for NODE in $WORKER_NODES; do
    ssh $USER@$NODE "$WORKER_CMD" &
done

sleep 1

echo "Déploiement terminé."
announce
