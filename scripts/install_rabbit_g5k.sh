# Add Erlang repository
echo "deb https://deb.erlang-solutions.com/debian bullseye contrib" | sudo tee /etc/apt/sources.list.d/erlang.list
wget -O- https://packages.erlang-solutions.com/ubuntu/erlang_solutions.asc | sudo apt-key add -

# Add RabbitMQ repository
echo "deb https://dl.bintray.com/rabbitmq/debian bullseye main" | sudo tee /etc/apt/sources.list.d/rabbitmq.list
wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -

# Update package lists
sudo apt-get update

# Install Erlang
sudo apt-get install -y erlang

# Install RabbitMQ Server
sudo apt-get install -y rabbitmq-server