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
ITERATIONS=30
BUNDLE_SIZE=1
app = Celery('pingpong_loadtest', broker=celery_broker_url, backend=celery_backend_url)

@app.task(bind=True)
def pong(self: Task):
    print("SERVER - Sending server address to directory...")
    server_address = socket.gethostbyname(socket.gethostname())
    directory.send_message(f"ip_sync_{self.request.id}", server_address)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f"SERVER - Listening on {server_address}:{PORT}")
    s.bind((server_address, PORT)) # Maybe use ipv6?
    s.listen()
    conn, addr = s.accept()

    print(f"SERVER - Connected by {addr}. Waiting for pings...")
    index = 0
    while True:
        for _ in range(BUNDLE_SIZE):
            data = conn.recv(2 ** index)
            if len(data) == 0:
                break
            conn.send(b'b')
        index += 1

    conn.close()

@app.task
def ping(server_id: str) -> int:
    print("CLIENT - Retreiving server address...")
    msgs = directory.get_message(f"ip_sync_{server_id}", timeout=5)
    ipaddr = msgs[0].body

    print(f"CLIENT - Received server address. Sending pings on: {ipaddr}:{PORT}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ipaddr, 12345))

    index = 0
    times = []
    load_factor=0
    while(index < ITERATIONS):
        print(f"CLIENT - Sending ping {index+1}/{ITERATIONS}")
        times.append(0)
        for _ in range(BUNDLE_SIZE):
            start = time.time()
            bytes_sent = 2 ** index
            s.sendall(b'a' * bytes_sent)
            data = s.recv(1)
            stop = time.time()
            latency = stop - start
            times[-1] += latency
        times[-1] /= BUNDLE_SIZE
        index += 1 

    s.close()

    assert data == b'b', "Server did not respond correctly"
    print("CLIENT - Server responded correctly")
    return times

if __name__ == "__main__":
    server = pong.delay()
    client = ping.delay(server.id)
    times = client.get()

    print(f"CLIENT - Received {len(times)} pings")
    with open("pingpong_loadtest.txt", "w") as f:
        for t in times:
            f.write(f"{t}\n")
        f.write(f"timestable: {time.time()}, test: pingpong_loadtest, size: {BUNDLE_SIZE}, iterations: {ITERATIONS}\n")