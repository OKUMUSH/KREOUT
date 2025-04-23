import subprocess
import time

SCREEN_NAME = "survival"
MC_JAR = "paper.jar"
RAM = "4G"

def is_server_running():
    result = subprocess.run(
        f"screen -ls | grep {SCREEN_NAME}",
        shell=True, capture_output=True, text=True
    )
    return SCREEN_NAME in result.stdout

def start_server():
    if is_server_running():
        return
    subprocess.run(
        f"screen -dmS {SCREEN_NAME} java -Xmx{RAM} -Xms{RAM} -jar {MC_JAR} nogui",
        shell=True
    )

def stop_server():
    if is_server_running():
        send_command("stop")

def restart_server():
    stop_server()
    time.sleep(5)
    start_server()

def send_command(command: str):
    subprocess.run(
        f"screen -S {SCREEN_NAME} -X stuff '{command}^M'",
        shell=True
    )