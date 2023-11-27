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

python $REPO_PATH/scripts/config_rabbit.py
