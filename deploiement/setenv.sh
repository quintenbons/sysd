export NODES=3
export WALLTIME="2:00:00"

export REPO_PATH=$HOME/sysd
export DEPLOY_INFO_PATH=$HOME/g5k_deploy
export PYTHONPATH=$REPO_PATH/src:$PYTHONPATH

# This is meant to change to avoid nfs overhead
export WORK_PATH=$REPO_PATH/dist

export PATH=$REPO_PATH/bin:$PATH
export PATH=$HOME/.local/bin:$PATH
export PATH=$HOME/.local/share/rabbitmq/sbin:$PATH
