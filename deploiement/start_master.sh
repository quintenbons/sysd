#!/bin/bash
REPO_PATH=$HOME/sysd
source $REPO_PATH/deploiement/setenv.sh
source $REPO_PATH/deploiement/rabbitmq_install.sh

# Launch the master

# Install rabbit
if ! command -v rabbitmq-server &> /dev/null
then
  install_rabbit_g5k
else
  echo "=== RabbitMQ is already installed"
fi

# If rabbit is running, stop it
if rabbitmqctl status > /dev/null 2>&1; then
    echo "=== Stopping existing RabbitMQ server"
    rabbitmqctl stop
    if [ $? -ne 0 ]; then
        echo "Failed to stop RabbitMQ server"
        exit 1
    else
        echo "RabbitMQ server stopped"
    fi
fi

# Start rabbit
echo "=== Starting RabbitMQ server"
rabbitmq-server -detached

# Wait for server to start
echo "=== Waiting for RabbitMQ server to start..."
for i in {1..20}; do
    if rabbitmqctl status > /dev/null 2>&1; then
        break
    fi
    sleep 1
done

if ! rabbitmqctl status; then
    echo "=== RabbitMQ server failed to start"
    exit 1
fi

# Configure rabbit
echo "=== Configuring RabbitMQ server"
python $REPO_PATH/scripts/config_rabbit.py

# Launch flask
mkdir -p /tmp/dist
cd /tmp/dist
nohup python $REPO_PATH/src/flask_server.py > $DEPLOY_INFO_PATH/flask.log 2>&1 &

# Compiling binaries for example makefiles
echo "Compiling premier for current architechture..."
g++ $REPO_PATH/example/premier/premier.c -o $REPO_PATH/bin/premier

echo "Linking sum and multiply..."
ln -s $REPO_PATH/example/matrix/sum $REPO_PATH/bin/sum
ln -s $REPO_PATH/example/matrix/multiply $REPO_PATH/bin/multiply
