import os
import subprocess
import time
import requests
import socket

from rich import print
from rich.table import Table


RESULT_DIR = "results"
SERVERS_DIR = "servers"
results = []

os.makedirs(RESULT_DIR, exist_ok=True)


def wait_for_server(framework):
    while True:
        try:
            requests.get("http://localhost:8000", timeout=1)
            print(f"[bold green]✔️ {framework} server started[/bold green] :rocket:")
            break
        except requests.exceptions.ConnectionError:
            print(
                f"[yellow]⏳ Waiting for [bold]{framework} server[/bold] to start...[/yellow]"
            )

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


def run_wkr(framework):
    command = "make benchmark"
    print(f"[cyan]🚀 [bold]Running wrk for {framework}[/bold] 🚀[/cyan]")
    return subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE)


def write_and_add_results(benchmark_result, framework):
    stdout_text = benchmark_result.stdout
    output_file_path = os.path.join(RESULT_DIR, f"{framework}.txt")
    with open(output_file_path, "w") as f:
        f.write(stdout_text)

    # Extract relevant data from the 'wrk' result and store it
    result_lines = stdout_text.strip().split("\n")
    result_data = {}

    for line in result_lines:
        parts = line.strip().split(": ")
        if len(parts) == 2:
            key, value = parts
            result_data[key] = value

    # Append the result data to the results list
    results.append(
        {
            "Framework": framework,
            "Requests/sec": result_data.get("Requests/sec", 0),
            "Transfer/sec": result_data.get("Transfer/sec", 0),
        }
    )


def load_test(framework):
    server_process = start_server(framework)
    benchmark_result = run_wkr(framework)
    kill_server(server_process, framework)
    write_and_add_results(benchmark_result, framework)


def get_framework_names():
    return os.listdir(SERVERS_DIR)


if __name__ == "__main__":
    for framework_name in get_framework_names():
        load_test(framework_name)

    # Create a rich Table to display the results
    table = Table(title="Benchmark Results using wrk with 12 threads and 400 connections for 10s")
    table.add_column("Framework", style="bold green")
    table.add_column("Requests/sec", style="bold blue")
    table.add_column("Transfer/sec", style="bold blue")

    results.sort(key=lambda x: x["Requests/sec"], reverse=True)
    # Add data to the table
    for result in results:
        table.add_row(
            f"[bold]{result['Framework']}[/bold]",  # Apply style to Framework column values
            result["Requests/sec"],
            result["Transfer/sec"],
        )

    # Print the table using rich
    print()
    print(table)
