#!/bin/bash

# Lire le nom d'utilisateur à partir d'un fichier .env
if [ -f ".env" ]; then
    export $(cat .env | xargs)
else
    echo ".env file not found"
    exit 1
fi

echo "user: $USER@access.grid5000.fr"
# Connexion à Grid5000
echo "Connexion à Grid5000"
sudo scp ./to_execute_on_g5k.sh $USER@access.grid5000.fr:/home/$USER/to_execute.sh 
ssh -t $USER@access.grid5000.fr "scp ~/to_execute.sh grenoble:/home/$USER/to_execute.sh"
ssh -t $USER@access.grid5000.fr "ssh grenoble 'bash ~/to_execute.sh'"

