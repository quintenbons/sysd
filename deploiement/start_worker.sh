#!/bin/bash
REPO_PATH=$HOME/sysd
source $REPO_PATH/deploiement/setenv.sh

# Environment check
FILESYNC_TYPE=${FILESYNC_TYPE:-nfs}
if [ -z "$FILE_SERVER" ] && [ "$FILESYNC_TYPE" != "nfs" ]; then
  echo "FILE_SERVER not set. Aborting..."
  exit 1
fi

export FILESYNC_TYPE=$FILESYNC_TYPE
export FILE_SERVER=$FILE_SERVER

# Launch the worker
if [ "$FILESYNC_TYPE" == "nfs" ]; then
  echo "=== Starting NFS worker $HOSTNAME"
  WORK_PATH=$HOME/make_dist
else
  echo "=== Starting server (non-nfs) worker $HOSTNAME"
  WORK_PATH=/tmp/dist
fi
mkdir -p $WORK_PATH
cd $WORK_PATH
python -m celery -A pingpong_loadtest worker --loglevel=info > $DEPLOY_INFO_PATH/worker-$HOSTNAME.log 2>&1 &
echo "Worker $HOSTNAME ready"
