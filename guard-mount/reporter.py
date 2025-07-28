from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import subprocess

console = Console()


def display_report(scan_summary):
    console.rule("[bold red]USB Guardian - Threat Report[/bold red]")

    console.print(f"[bold cyan]Device:[/bold cyan] {scan_summary['device']}")
    console.print(f"[bold green]Clean Files:[/bold green] {scan_summary['clean_count']}")
    console.print(f"[bold yellow]Suspicious Files:[/bold yellow] {len(scan_summary['suspicious'])}")
    console.print(f"[bold red]Malicious Files:[/bold red] {len(scan_summary['malicious'])}")

    # Malicious Files Table
    if scan_summary['malicious']:
        console.print("\n[bold red]Malicious Files Detected:[/bold red]")
        table = Table(show_header=True, header_style="bold red")
        table.add_column("Path", style="dim", width=70)
        table.add_column("Threat")

        for entry in scan_summary['malicious']:
            table.add_row(entry['path'], entry['threat'])
        console.print(table)

    # Suspicious Files Table
    if scan_summary['suspicious']:
        console.print("\n[bold yellow]Suspicious Files Detected:[/bold yellow]")
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("Path", style="dim", width=70)
        table.add_column("Reason")

        for entry in scan_summary['suspicious']:
            table.add_row(entry['path'], entry['reason'])
        console.print(table)

    # Action Prompt
    console.print("\n[bold]Choose an action:[/bold]")
    console.print(" [1] Allow Access (Read-Only Mode)")
    console.print(" [2] Quarantine Malicious Files")
    console.print(" [3] Eject Device Immediately")

    action = Prompt.ask("\nEnter choice", choices=["1", "2", "3"], default="3")

    # Handle Actions
    if action == "1":
        authenticate_user()
        console.print("[bold green]Device access granted in Read-Only Mode.[/bold green]")
        # Here, you would mount the device for user access
    elif action == "2":
        authenticate_user()
        console.print("[bold yellow]Quarantining malicious files...[/bold yellow]")
        # You can add logic to isolate/delete files here
    elif action == "3":
        console.print("[bold red]Ejecting device...[/bold red]")
        eject_device(scan_summary['device'])


def authenticate_user():
    console.print("\n[bold cyan]Sudo authentication required to proceed.[/bold cyan]")
    try:
        subprocess.run(["sudo", "-v"], check=True)
        console.print("[bold green]Authentication successful.[/bold green]")
    except subprocess.CalledProcessError:
        console.print("[bold red]Authentication failed. Action aborted.[/bold red]")


def eject_device(device_node):
    try:
        subprocess.run(["udisksctl", "power-off", "-b", device_node], check=True)
        console.print("[bold green]Device ejected safely.[/bold green]")
    except subprocess.CalledProcessError:
        console.print("[bold red]Failed to eject device. You can manually remove it.[/bold red]")


if __name__ == "__main__":
    # Test mock data
    sample_summary = {
        'device': '/dev/sdb1',
        'clean_count': 100,
        'malicious': [{'path': '/mnt/usb_guardian/badfile.exe', 'threat': 'Trojan.Agent.Generic'}],
        'suspicious': [{'path': '/mnt/usb_guardian/.hidden_payload', 'reason': 'Hidden File'}]
    }
    display_report(sample_summary)