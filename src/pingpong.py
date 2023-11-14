#!/usr/bin/python3
from celery import Celery
import time

broker_url = 'amqp://sysd:dunno@localhost:5672/sysdvhost'
backend_url = 'rpc://'
app = Celery('pingpong', broker=broker_url, backend=backend_url)

@app.task
def ping():
    print("ping")
    start_time = time.time()
    pong.delay(start_time) # Envoyer un message à pong

@app.task
def pong(start_time):
    print("pong")
    ping.delay(start_time) # Envoyer un message à pong
    print(time.time() - start_time)

# Test du ping-pong
if __name__ == "__main__":
    round_trip_time = ping.delay().get()
    print(f"Temps aller-retour pour la taille: {round_trip_time} secondes", flush=True)
