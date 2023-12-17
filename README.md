# SYSD

## Quick start

1. Install RabbitMQ server https://www.rabbitmq.com/install-debian.html with the shell script
2. Install Celery and PyAmqp `pip install "celery[librabbitmq,redis,auth,msgpack]" amqp`
3. Configure it with the `scripts/config_rabbit.py` tool (it takes optional arguments, check with -h)
4. Launch a Celery worker on your chosen module (eg. for pinpong, within src/, launch `PYTHONPATH=.:$PYTHONPATH celery -A pingpong worker --loglevel=info`)
5. Go wild (launch `src/pingpong.py` to launch a simple ping pong)

## Quick start g5k

1. Deploy everything with `./setup_all.sh [G5K_USER]`
2. Connect to grenoble.g5k `ssh grenoble.g5k`
3. Use the parralel makefile: `cd ~/sysd/dist && python ~/sysd/src/make.py [/path/to/Makefile]`
4. Destroy with `ssh grenobel.g5k "~/sysd/deploiement/hard_cleanup.sh"`

### More details:

`setup_all.sh` will launch some workers for some time (specifics are in `deploiement/setenv.sh`). Local ssh configuration is also changed, so you won't need your password anymore.

To check the current deployment, check out the info.json file:

`ssh grenoble.g5k "cat ~/g5k_deploy/info.json"`

Note that currently, NFS is used to sync files, so you will find all artifacts in `~/sysd/dist`

## RabbitMQ Broker

Two vhosts are needed, one for celery (tasks), one for the directory, which is needed for general communication between workers.

`scripts/config_rabbit.py` will configure both hosts automatically. To use the directory, use `src/directory.py`. Keep all amqp communications in that file so that it becomes the abstraction for the amqp interface.
