#!/bin/bash
REPO_PATH=$HOME/sysd
source $REPO_PATH/deploiement/setenv.sh

# Launch the worker
mkdir $WORK_PATH
cd $WORK_PATH
python -m celery -A runner worker --loglevel=info