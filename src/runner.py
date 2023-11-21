#!/usr/bin/python3
"""
Using directory to create a socket connection between two tasks
"""
import socket
import time
from celery import Celery, Task
from constants import *
import directory

PORT=12345
app = Celery('runner', broker=celery_broker_url, backend=celery_backend_url)

@app.task(bind=True)
def run(self: Task, taskname: str, ):
    # Get needed files from manager
    # TODO (for now it's just in main)

    # Run task
    pass
