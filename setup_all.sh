#!/bin/bash

USER="jubourseau"

echo "user: $USER@access.grid5000.fr"

# Connexion à Grid5000 et configuration
ssh -t $USER@access.grid5000.fr << 'ENDSSH'
ssh grenoble << 'ENDGRENOBLE'
    echo "Configuration de l'environnement sur le serveur Grenoble"

    # Vérification de l'existence du répertoire sysd
    if [ ! -d "sysd" ]; then
        git clone https://github.com/quintenbons/sysd.git
    else
        echo "Le répertoire 'sysd' existe déjà, mise à jour du dépôt..."
        cd sysd
        git pull
    fi

    cd sysd
    git checkout deploiement
    chmod +x to_execute_on_g5k.sh
    ./to_execute_on_g5k.sh
ENDGRENOBLE
ENDSSH