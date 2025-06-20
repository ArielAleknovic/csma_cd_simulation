import requests
import time
import random
from datetime import datetime

SENDER_ID = "T2"  # Ajuste para cada transmissor
CHANNEL_URL = "http://channel_server:5000"

SLOT_TIME = 0.2
MAX_ATTEMPTS = 10
NUM_FRAMES = 100

def backoff(k):
    return random.randint(0, 2**k - 1) * SLOT_TIME

def log(msg):
    print(f"[{SENDER_ID}] {msg}")

def log_to_file(filename, message):
    with open(f"/app/logs/{filename}", "a") as f:
        f.write(message + "\n")

for frame in range(NUM_FRAMES):
    attempt = 0
    while attempt < MAX_ATTEMPTS:
        resp = requests.get(f"{CHANNEL_URL}/sense").json()
        if not resp["busy"]:
            res = requests.post(f"{CHANNEL_URL}/transmit", json={"sender": SENDER_ID}).json()
            if res["status"] == "ok":
                log(f"Iniciando transmissão do quadro {frame}")
                time.sleep(SLOT_TIME * 2)
                stop_res = requests.post(f"{CHANNEL_URL}/stop", json={"sender": SENDER_ID}).json()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if stop_res["status"] == "collision":
                    log(f"🚨 Colisão detectada no quadro {frame}")
                    log_to_file("collisions.log", f"{timestamp} | {SENDER_ID} | frame {frame} | tentativa {attempt+1}")
                    attempt += 1
                    wait = backoff(attempt)
                    log(f"Backoff de {wait:.2f}s")
                    time.sleep(wait)
                else:
                    log(f"✅ Quadro {frame} enviado com sucesso")
                    log_to_file("success.log", f"{timestamp} | {SENDER_ID} | frame {frame} | tentativas {attempt+1}")
                    break
            else:
                time.sleep(SLOT_TIME)
        else:
            time.sleep(SLOT_TIME)
    if attempt >= MAX_ATTEMPTS:
        log(f"❌ Falha no envio do quadro {frame} após {MAX_ATTEMPTS} tentativas")
