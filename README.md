# SYSD

## Quick start

1. Install RabbitMQ server https://www.rabbitmq.com/install-debian.html with the shell script
2. Install Celery and PyAmqp `pip install "celery[librabbitmq,redis,auth,msgpack]" amqp`
3. Configure it with the `scripts/config_rabbit.py` tool (it takes optional arguments, check with -h)
4. Launch a Celery worker on your chosen module (eg. for pinpong, within src/, launch `PYTHONPATH=.:$PYTHONPATH celery -A pingpong worker --loglevel=info`)
5. Go wild (launch `src/pingpong.py` to launch a simple ping pong)

## RabbitMQ Broker

Two vhosts are needed, one for celery (tasks), one for the directory, which is needed for general communication between workers.

`scripts/config_rabbit.py` will configure both hosts automatically. To use the directory, use `src/directory.py`. Keep all amqp communications in that file so that it becomes the abstraction for the amqp interface.
