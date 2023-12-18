#!/usr/bin/python3
"""
Using directory to create a socket connection between two tasks
"""
import socket
import time
from celery import Celery, Task
from constants import *
import directory
import matplotlib.pyplot as plt
import math

PORT=12345
BUNDLE_SIZE=10000
app = Celery('empty', broker=celery_broker_url, backend=celery_backend_url)

@app.task
def empty() -> int:
    return

if __name__ == "__main__":
    print("Starting pingpong latency test")
    server = empty.get()