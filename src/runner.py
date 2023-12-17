#!/usr/bin/python3
"""
Using directory to create a socket connection between two tasks
"""
import os
import time
from typing import List
from celery import Celery
from constants import *
import subprocess
from flask_wrapper import APIWrapper

app = Celery('runner', broker=celery_broker_url, backend=celery_backend_url)

filesync_type = os.environ.get('FILESYNC_TYPE', 'nfs')
file_server = os.environ.get('FILE_SERVER', 'http://localhost:5000')

file_wrapper = APIWrapper(file_server)

def sync_dependencies(dependencies: List[str]) -> None:
    if filesync_type == 'nfs':
        return

    for dep in dependencies:
        if not os.path.exists(dep):
            while not file_wrapper.get_file(dep):
                print(f"Failed to get file {dep}")
                time.sleep(1)
            else:
                print(f"Got file {dep}")

def send_created(filename: str) -> None:
    if filesync_type == 'nfs':
        return

    if not file_wrapper.upload_file(open(filename, 'rb')):
        print(f"Failed to upload file {filename}")

@app.task()
def run(taskname: str, task_cmd: str, dependencies: List[str]) -> bool:
    # Get needed files from manager
    sync_dependencies(dependencies)

    # Run task
    newmsg = f"Running task {taskname} with command {task_cmd}"
    print(newmsg)
    subprocess.run(task_cmd, shell=True)

    send_created(taskname)

    return True
