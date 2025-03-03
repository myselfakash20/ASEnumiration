import os
import json
import subprocess
import time
import signal
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.panel import Panel
from rich import print as rprint

console = Console()

# Banner
def print_banner():
    banner = """
    ███████╗██╗   ██╗██████╗  ██████╗ ██████╗  █████╗ ███╗   ███╗
    ██╔════╝██║   ██║██╔══██╗██╔════╝ ██╔══██╗██╔══██╗████╗ ████║
    █████╗  ██║   ██║██████╔╝██║  ███╗██████╔╝███████║██╔████╔██║
    ██╔══╝  ██║   ██║██╔═══╝ ██║   ██║██╔═══╝ ██╔══██║██║╚██╔╝██║
    ██║     ╚██████╔╝██║     ╚██████╔╝██║     ██║  ██║██║ ╚═╝ ██║
    ╚═╝      ╚═════╝ ╚═╝      ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝
    Enumiration By Akash
    """
    console.print(Panel(banner, style="bold magenta"))

# Check and install missing tools
def check_and_install(tool, install_cmd):
    if subprocess.run(f"which {tool}", shell=True, capture_output=True).returncode != 0:
        console.print(f"[bold red]{tool} not found! Installing...[/bold red]")
        run_command(install_cmd)
        console.print(f"[bold green]{tool} installed successfully![/bold green]")

# Run a command and return output
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"[red]Error executing command:[/red] {e}"]

# Subdomain Enumeration
def subdomain_enum(domain):
    console.print(f"\n[bold cyan]Running all enumeration tools for {domain}...[/bold cyan]")
    
    # Check and install missing tools
    check_and_install("subfinder", "sudo apt install subfinder -y")
    check_and_install("amass", "sudo apt install amass -y")
    check_and_install("dnsx", "go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest")
    check_and_install("findomain", "wget https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux -O findomain && chmod +x findomain && sudo mv findomain /usr/local/bin/")
    check_and_install("assetfinder", "go install github.com/tomnomnom/assetfinder@latest")
    check_and_install("httpx", "go install github.com/projectdiscovery/httpx/cmd/httpx@latest")
    
    tools = {
        "Subfinder": f"subfinder -d {domain} -silent -o subfinder.txt",
        "Amass": f"amass enum -passive -d {domain} -o amass.txt",
        "DNSx": f"echo {domain} | dnsx -silent -o dnsx.txt",
        "Findomain": f"findomain -t {domain} -q -o findomain.txt",
        "Assetfinder": f"assetfinder --subs-only {domain} > assetfinder.txt",
        "Crt.sh": f"curl -s https://crt.sh/?q=%25.{domain}&output=json | jq -r '.[].name_value' | sed 's/\\*\\.//g' | sort -u > crtsh.txt"

    }
    
    for tool, cmd in tools.items():
        console.print(f"[bold yellow]Running {tool}...[/bold yellow]")
        run_command(cmd)
    
    # Merge and sort unique subdomains
    console.print("\n[bold green]Merging results and sorting unique subdomains...[/bold green]")
    run_command("cat *.txt | sort -u > all_subdomains.txt")
    
    # Validate live subdomains using httpx
    console.print("[bold cyan]Checking for live subdomains with httpx...[/bold cyan]")
    run_command("cat all_subdomains.txt | httpx-toolkit -silent -o live_subdomains.txt")
    
    console.print("[bold green]Live subdomains saved to live_subdomains.txt[/bold green]")
    
     # Cleanup temporary files
    #console.print("[bold red]Cleaning up temporary files...[/bold red]")
    #run_command("rm -f subfinder.txt amass.txt dnsx.txt findomain.txt assetfinder.txt crtsh.txt all_subdomains.txt")

# Handle script termination
def signal_handler(sig, frame):
    console.print("\n[bold magenta]Bye, my friend! Have a nice day! 😊[/bold magenta]")
    exit(0)

# Main function
def main():
    print_banner()
    signal.signal(signal.SIGINT, signal_handler)  # Capture Ctrl+C
    domain = console.input("\n[bold cyan]Enter the target domain:[/bold cyan] ")
    subdomain_enum(domain)

if __name__ == "__main__":
    main()
