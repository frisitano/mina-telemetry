import subprocess
import datetime
from time import sleep

def run() -> None:
    while True:
        data = subprocess.check_output(["coda", "advanced", "telemetry", "-daemon-peers"])
        with open(f"mina-telemetry-{datetime.datetime.now()}.json", "r") as f:
            f.write(data)
            sleep(30*60)
