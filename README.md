# SYSD

## Quick start

1. Install RabbitMQ server https://www.rabbitmq.com/install-debian.html with the shell script
2. Configure it with the scripts/config_rabbit.py tool (it takes optional arguments, check with -h)
3. Install Celery `pip install "celery[librabbitmq,redis,auth,msgpack]"`
4. Launch a Celery worker on your chosen module (eg. for pinpong, within src/, launch `PYTHONPATH=.:$PYTHONPATH celery -A pingpong worker --loglevel=info`)
5. Go wild (launch `src/pingpong.py` to launch a simple ping pong)
