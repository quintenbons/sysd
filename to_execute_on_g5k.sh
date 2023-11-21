#!/bin/bash
# Configuration de l'environnement
echo "Configuration de l'environnement"
git clone https://github.com/quintenbons/sysd.git
cd sysd
mkdir -p dist

# Installation des dépendances
echo "Installation de Celery et autres dépendances"
pip install "celery[librabbitmq,redis,auth,msgpack]" amqp

# Réservation des nœuds
echo "Réservation des nœuds"
NODES=2
WALLTIME="2:00:00"
oarsub -l nodes=$NODES,walltime=$WALLTIME "sleep 3600"

# Attente que la réservation soit active
while true; do
    STATE=$(oarstat -u | grep "$USER" | awk '{print $5}')
    if [ "$STATE" == "R" ]; then
        echo "Réservation active."
        break
    fi
    sleep 60  # Attente de 60 secondes avant de vérifier à nouveau
done

# Récupération des noms d'hôte assignés
JOB_ID=$(oarstat -u | grep "$USER" | awk '{print $1}')
NODES=$(oarstat -f -j $JOB_ID | grep "assigned_hostnames" | awk '{print $3}' | tr '+' '\n')

# Commande pour lancer les workers
WORKER_CMD="export PATH=../:$PATH; celery -A runner worker --loglevel=info"

# Lancer les workers
for NODE in $NODES; do
    ssh $USER@$NODE "$WORKER_CMD" &
done

echo "Déploiement terminé."
