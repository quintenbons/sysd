#!/bin/bash
REPO_PATH=$HOME/sysd
source $REPO_PATH/deploiement/setenv.sh

# Environment check
FILESYNC_TYPE=${:-nfs}
if [ -z "$FILE_SERVER" ] && [ "$FILESYNC_TYPE" != "nfs" ]; then
  echo "FILE_SERVER not set. Aborting..."
  exit 1
fi

export FILESYNC_TYPE=$FILESYNC_TYPE
export FILE_SERVER=$FILE_SERVER

# Launch the worker
mkdir $WORK_PATH
cd $WORK_PATH
echo "Worker $HOSTNAME ready"
python -m celery -A runner worker --loglevel=info > $DEPLOY_INFO_PATH/log-worker-$HOSTNAME.txt 2>&1 &
