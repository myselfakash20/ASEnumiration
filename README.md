# ASEnumiration

ASEnumiration is an advanced subdomain enumeration tool designed for bug bounty hunters and penetration testers. It automates subdomain discovery using multiple enumeration tools, merges results, validates live subdomains, and presents a clean output.

Features

✅ Runs multiple subdomain enumeration tools automatically
✅ Merges and filters unique subdomains
✅ Validates live subdomains using httpx
✅ Automatically installs missing tools
✅ Saves the final results to live_subdomains.txt
✅ Provides a clean and interactive terminal UI with rich

Installation

Ensure you have the required dependencies installed before running ASEnumiration:

```
sudo apt update && sudo apt install -y amass subfinder
wget https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux -O findomain && chmod +x findomain && sudo mv findomain /usr/local/bin/
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install github.com/tomnomnom/assetfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
pip install rich
```

Usage

Run ASEnumiration with the following command:

`python3 subdomain_enum.py`

Enter the target domain when prompted. The tool will execute all enumeration processes, validate live subdomains, and save the final results in live_subdomains.txt.

Output

The final list of live subdomains will be saved at:

live_subdomains.txt

If interrupted (Ctrl+C), a friendly exit message will be displayed.

Contribution

Feel free to fork and contribute by submitting pull requests!
