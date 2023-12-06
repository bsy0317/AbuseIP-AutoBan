# 🚫 IP Ban Script

This script automates the process of managing IP addresses to block abusive IPs using `iptables` and `ipset`.

[![Python](https://img.shields.io/badge/Python-3-blue)](https://www.python.org/)
[![Rich](https://img.shields.io/badge/rich-library-green)](https://github.com/willmcgugan/rich)

## Overview

This Python script fetches a list of abusive IP addresses from AbuseIPDB and blocks them using `iptables` and `ipset`. It performs the following actions:

- Checks for command-line arguments (`reset` or `backup`) to restore or backup `iptables` rules respectively.
- Creates an `ipset` named `blockip` if it doesn't exist.
- Adds `blockip` to the `iptables` chain `INPUT` to drop traffic from the listed IPs.
- Fetches the latest IP list from the remote repository.
- Updates the `ipset` with the fetched IP addresses.
- Saves the `ipset` and restarts `iptables`.

## Prerequisites

- Python 3
- [Rich](https://github.com/willmcgugan/rich) library for enhanced console output
- Root or sudo privileges to execute `iptables` and `ipset` commands

## Usage

To execute the script, run the Python file `ban_bulk_ipset.py`. Additionally, you can use the following command-line arguments:

- `reset`: Restores the original `iptables` rules.
- `backup`: Backs up the original `iptables` rules.

**Note**: Exercise caution while using the reset and backup options as they modify the firewall rules.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/borestad/blocklist-abuseipdb.git
    ```

2. Install the required dependencies:

    ```bash
    pip install rich
    ```

3. Execute the script:

    ```bash
    python ban_bulk_ipset.py
    ```

## Contributions

Contributions and suggestions are welcome! Please fork the repository, make changes, and create a pull request.

---

**Disclaimer:** This script manages IP addresses and firewall rules. Use it responsibly and in compliance with your local laws and regulations.
