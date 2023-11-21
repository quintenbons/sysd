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
ITERATIONS=1000000
app = Celery('pingpong', broker=celery_broker_url, backend=celery_backend_url)

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
    while True:
        data = conn.recv(1)
        if len(data) == 0:
            break
        conn.send(b'b')

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
    while(index < ITERATIONS):
        start = time.time()
        index += 1
        s.sendall(b'a')
        data = s.recv(1)
        stop = time.time()
        latency = stop - start
        times.append(latency)

    s.close()

    assert data == b'b', "Server did not respond correctly"
    print("CLIENT - Server responded correctly")
    return times

if __name__ == "__main__":
    server = pong.delay()
    client = ping.delay(server.id)
    times = client.get()

    print(f"CLIENT - Received {len(times)} pings")
    with open("pingpong.txt", "w") as f:
        for t in times:
            f.write(f"{t}\n")
    plt.hist([math.log(t, 10) for t in times], bins=100)
    plt.show()
    input("Press enter to exit...")