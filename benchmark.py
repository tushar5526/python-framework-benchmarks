import os
import subprocess
import time
import requests
import socket

from rich import print

RESULT_DIR = "results"
SERVERS_DIR = "servers"

os.makedirs(RESULT_DIR, exist_ok=True)


def wait_for_server(framework):
    while True:
        try:
            requests.get("http://localhost:8000", timeout=1)
            print(f"[bold green]✔️ {framework} server started[/bold green] :rocket:")
            break
        except requests.exceptions.ConnectionError:
            print(f"[yellow]⏳ Waiting for [bold]{framework} server[/bold] to start...[/yellow]")

        time.sleep(1)


def wait_for_cleanup():
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", 8000))
                break
        except socket.error:
            print("[yellow]⏳ [bold]Waiting for cleanup...[/bold][/yellow]")
            time.sleep(1)
            pass


def start_server(framework):
    wait_for_cleanup()
    command = f"make {framework}"
    server_process = subprocess.Popen(
        command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    wait_for_server(framework)
    return server_process


def kill_server(server_process, framework):
    print(f"[bold red]🛑 [red]Killing {framework} server[/red][/bold red]")
    server_process.terminate()


def run_wkr_and_write_results(framework):
    command = "make benchmark"
    print(f"[cyan]🚀 [bold]Running wrk for {framework}[/bold] 🚀[/cyan]")
    result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE)
    output_file_path = os.path.join(RESULT_DIR, f"{framework}.txt")

    print(f"[cyan]📝 [bold]Writing benchmark results for {framework}[/bold] 📝[/cyan]")
    with open(output_file_path, "w") as file:
        file.write(result.stdout)


def load_test(framework):
    server_process = start_server(framework)
    run_wkr_and_write_results(framework)
    kill_server(server_process, framework)


def get_framework_names():
    return os.listdir(SERVERS_DIR)


if __name__ == "__main__":
    for framework in get_framework_names():
        load_test(framework)
