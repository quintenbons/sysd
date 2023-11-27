export REPO_PATH=$HOME/sysd
export PYTHONPATH=$REPO_PATH/src:$PYTHONPATH
export PATH=$REPO_PATH/bin:$PATH

# This is meant to change to avoid nfs overhead
export WORK_PATH=$REPO_PATH/dist
