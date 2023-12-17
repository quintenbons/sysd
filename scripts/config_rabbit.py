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
    print(f"Configuring RabbitMQ for vhost {vhost} and user {user}")
    print(f"Running commands:")
    print(f"rabbitmqctl add_vhost {vhost}")
    subprocess.run(f"rabbitmqctl add_vhost {vhost}", shell=True)
    print(f"rabbitmqctl add_user {user} {password}")
    subprocess.run(f"rabbitmqctl add_user {user} {password}", shell=True)
    print(f"rabbitmqctl set_user_tags {user} {user_tag}")
    subprocess.run(f"rabbitmqctl set_user_tags {user} {user_tag}", shell=True)
    print(f"rabbitmqctl set_permissions -p {vhost} {user} \".*\" \".*\" \".*\"")
    subprocess.run(f"rabbitmqctl set_permissions -p {vhost} {user} \".*\" \".*\" \".*\"", shell=True)

def inject_config(vhost, user, password, user_tag, prefix=""):
    root = os.path.join(os.path.dirname(__file__), "..")
    constants = os.path.realpath(os.path.join(root, "src", "constants.py"))

    with open(constants, 'r') as file:
        content = file.read()

    content = re.sub(fr'^{prefix}vhost = .*\n', f'{prefix}vhost = "{vhost}"\n', content, flags=re.MULTILINE)
    content = re.sub(fr'^{prefix}user = .*\n', f'{prefix}user = "{user}"\n', content, flags=re.MULTILINE)
    content = re.sub(fr'^{prefix}password = .*\n', f'{prefix}password = "{password}"\n', content, flags=re.MULTILINE)
    content = re.sub(fr'^{prefix}user_tag = .*\n', f'{prefix}user_tag = "{user_tag}"\n', content, flags=re.MULTILINE)

    with open(constants, 'w') as file:
        file.write(content)

def main():
    parser = argparse.ArgumentParser(description='Autoconfig RabbitMQ')
    parser.add_argument("--c-vhost", help="vhost name", type=str, default="celery_vhost")
    parser.add_argument("--c-user", help="user name", type=str, default="celery_user")
    parser.add_argument("--c-password", help="password", type=str, default="celery_password")
    parser.add_argument("--c-user-tag", help="user tag", type=str, default="celery_tag")
    parser.add_argument("--d-vhost", help="vhost name", type=str, default="dir_vhost")
    parser.add_argument("--d-user", help="user name", type=str, default="dir_user")
    parser.add_argument("--d-password", help="password", type=str, default="dir_password")
    parser.add_argument("--d-user-tag", help="user tag", type=str, default="dir_tag")
    parser.add_argument("--no-inject", help="do not inject config in src/constants.py", action="store_true")
    parser.add_argument("--no-config", help="do not config rabbitmd", action="store_true")
    args = parser.parse_args()

    if not args.no_config:
        config_rabbit(args.c_vhost, args.c_user, args.c_password, args.c_user_tag)
        config_rabbit(args.d_vhost, args.d_user, args.d_password, args.d_user_tag)

    if not args.no_inject:
        inject_config(args.c_vhost, args.c_user, args.c_password, args.c_user_tag, "celery_")
        inject_config(args.d_vhost, args.d_user, args.d_password, args.d_user_tag, "directory_")

    print()
    print("Configured RabbitMQ with following parameters (injected in src/constants.py):")
    print(f"celery (tasker)")
    print(f"  vhost: {args.c_vhost}")
    print(f"  user: {args.c_user}")
    print(f"  password: {args.c_password}")
    print(f"  user_tag: {args.c_user_tag}")
    print()
    print(f"directory (communication))")
    print(f"  vhost: {args.d_vhost}")
    print(f"  user: {args.d_user}")
    print(f"  password: {args.d_password}")
    print(f"  user_tag: {args.d_user_tag}")

if __name__ == "__main__":
    main()