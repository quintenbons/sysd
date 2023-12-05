#!/bin/bash
REPO_PATH=$HOME/sysd
source $REPO_PATH/deploiement/setenv.sh

# Launch the master

# Install rabbit
sudo-g5k
$REPO_PATH/scripts/install_rabbit_g5k.sh

# Enable and start the RabbitMQ service
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server

# Display status
echo
echo "RabbitMQ service status:"
sudo systemctl status rabbitmq-server

echo "Compiling premier for current architechture..."
g++ $REPO_PATH/example/premier/premier.c -o $REPO_PATH/bin/premier

echo "Linking sum and multiply..."
ln -s $REPO_PATH/example/matrix/sum $REPO_PATH/bin/sum
ln -s $REPO_PATH/example/matrix/multiply $REPO_PATH/bin/multiply

python $REPO_PATH/scripts/config_rabbit.py
