
import statistics
import time

import httpx

URL = "http://127.0.0.1:8000/detect-language"
CORPS = {"text": "Je souhaite reinitialiser mon mot de passe."}

mesures = []
with httpx.Client() as client:
    for i in range(10):
        debut = time.perf_counter()
        r = client.post(URL, json=CORPS)
        total = (time.perf_counter() - debut) * 1000
        r.raise_for_status()
        mesures.append(total)
        print(f"requete {i + 1:2d} : {total:7.1f} ms (serveur : {r.json()['latency_ms']} ms)")

print(f"min     : {min(mesures):.1f} ms")
print(f"mediane : {statistics.median(mesures):.1f} ms")
print(f"max     : {max(mesures):.1f} ms")
print(f"moyenne : {statistics.mean(mesures):.1f} ms")
