import subprocess
import datetime
from time import sleep

def run() -> None:
    while True:
        data = str(subprocess.check_output(["coda", "advanced", "telemetry", "-daemon-peers"]))
        with open(f"/home/Francesco/telemetry-data/mina-telemetry-{datetime.datetime.now()}.json".replace(" ", ""), "w") as f:
            f.write(data)
        sleep(30*60)

if __name__ == "__main__":
    run()
