#!/usr/bin/python3
# rabbitMQ autoconfig
# start server: rabbitmq-server -detached
# check logs: tail -f /var/log/rabbitmq/rabbit@<hostname>
# stop server: rabbitmqctl stop
import argparse
import subprocess
import os
import re

def config_rabbit(vhost, user, password, user_tag):
    subprocess.run(f"sudo rabbitmqctl add_vhost {vhost}", shell=True)
    subprocess.run(f"sudo rabbitmqctl add_user {user} {password}", shell=True)
    subprocess.run(f"sudo rabbitmqctl set_user_tags {user} {user_tag}", shell=True)
    subprocess.run(f"sudo rabbitmqctl set_permissions -p {vhost} {user} \".*\" \".*\" \".*\"", shell=True)

def inject_config(vhost, user, password, user_tag):
    root = os.path.join(os.path.dirname(__file__), "..")
    constants = os.path.realpath(os.path.join(root, "src", "constants.py"))

    with open(constants, 'r') as file:
        content = file.read()

    content = re.sub(r'^password = .*\n', f'password = "{password}"\n', content, flags=re.MULTILINE)
    content = re.sub(r'^user = .*\n', f'user = "{user}"\n', content, flags=re.MULTILINE)

    with open(constants, 'w') as file:
        file.write(content)

def main():
    parser = argparse.ArgumentParser(description='Autoconfig RabbitMQ')
    parser.add_argument("--vhost", help="vhost name", type=str, default="sysdvhost")
    parser.add_argument("--user", help="user name", type=str, default="sysduser")
    parser.add_argument("--password", help="password", type=str, default="password")
    parser.add_argument("--user-tag", help="user tag", type=str, default="sysdtag")
    parser.add_argument("--no-inject", help="do not inject config in src/constants.py", action="store_true")
    args = parser.parse_args()

    config_rabbit(args.vhost, args.user, args.password, args.user_tag)

    if not args.no_inject:
        inject_config(args.vhost, args.user, args.password, args.user_tag)

    print()
    print("Configured RabbitMQ with following parameters (injected in src/constants.py):")
    print(f"vhost: {args.vhost}")
    print(f"user: {args.user}")
    print(f"password: {args.password}")
    print(f"user_tag: {args.user_tag}")


if __name__ == "__main__":
    main()