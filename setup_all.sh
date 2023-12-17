#!/bin/bash
if [ $# -lt 1 ]; then
    echo "Usage: $0 user [site] [git-branch] [nfs/server]"
    echo "Only user is mandatory"
    exit 1
fi

G5K_USER=$1
G5K_SITE=${2:-grenoble}
G5K_BRANCH=${3:-main}
G5K_FILESYNC=${4:-nfs}
echo "user: $G5K_USER@access.grid5000.fr"

# Configuration locale (~/.ssh/config)
# Permet la connexion à Grid5000 sans mot de passe, et la redirection rapide ssh grenoble.g5k -> grenoble
./deploiement/configure_ssh.sh $G5K_USER

# Connexion à Grid5000 et configuration
ssh -t "$G5K_SITE.g5k" << ENDSSH
    echo "Configuration de l'environnement sur le serveur Grenoble"

    # Vérification de l'existence du répertoire sysd
    if [ ! -d "sysd" ]; then
        git clone https://github.com/quintenbons/sysd.git
    fi

    # Creation forcée d'une branche locale
    echo "Mise à jour du dépôt sysd"
    cd sysd
    git fetch
    git reset --hard "origin/$G5K_BRANCH"
    git clean -fd
    git branch -D g5k-local-branch
    git checkout -b g5k-local-branch "origin/$G5K_BRANCH"
    cd ..

    export FILESYNC_TYPE=$G5K_FILESYNC
    ./sysd/deploiement/to_execute_on_g5k.sh
ENDSSH
