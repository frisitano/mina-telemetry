import subprocess
import datetime
from time import sleep, strftime

def run() -> None:
    while True:
        data = subprocess.check_output(["coda", "advanced", "telemetry", "-daemon-peers"]).decode("utf-8")
        with open(f"/home/Francesco/telemetry-data/mina-telemetry-{strftime('%Y%m%d-%H%M%S')}.json", "w") as f:
            f.write(data)
        sleep(30*60)

if __name__ == "__main__":
    run()
