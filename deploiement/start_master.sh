REPO_PATH=$HOME/sysd
source $REPO_PATH/deploiement/setenv.sh

# Launch RabbitMQ
cd $REPO_PATH
$REPO_PATH/scripts/quick_install_rabbit.sh
python $REPO_PATH/scripts/config_rabbit.py
