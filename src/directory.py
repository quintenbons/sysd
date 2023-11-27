#!/usr/bin/python3
"""
Abstract communication interface with the directory
"""
from typing import List, Union
import amqp
from constants import *

def _new_connection() -> amqp.Connection:
    return amqp.Connection(
        host=f"{broker_host}:{broker_port}",
        userid=directory_user,
        password=directory_password,
        virtual_host=directory_vhost,
        insist=False
    )

def send_message(queue: str, message: str) -> None:
    """
    Sends a message to the given queue.
    """
    with _new_connection() as connection, connection.channel() as channel:
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_publish(amqp.Message(message), routing_key=queue)

def get_message(queue: str, timeout: Union[int, None] = 30) -> List[amqp.Message]:  # Python 3.9.2 syntax
    """
    Blocks until a message is received on the given queue.
    """
    messages = []

    with _new_connection() as connection, connection.channel() as channel:
        def callback(msg: amqp.Message):
            nonlocal messages
            messages.append(msg)
            channel.basic_ack(msg.delivery_tag)

        channel.queue_declare(queue=queue, durable=True)
        channel.basic_consume(queue=queue, callback=callback)
        while len(messages) == 0:
            connection.drain_events(timeout=timeout)

    return messages

