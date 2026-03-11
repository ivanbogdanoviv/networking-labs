#!/usr/bin/env python3
"""
backup_configs.py — SSH into a Cisco device and save the running config to a file.

Usage:
    python backup_configs.py --host <IP> --user <username> [--port 22]

Requirements:
    pip install netmiko

TODO: Replace placeholder credentials with .env or SSH key auth before use.
"""

import argparse
import os
from datetime import datetime

# TODO: Uncomment after running: pip install netmiko
# from netmiko import ConnectHandler


def backup_device(host: str, username: str, password: str, port: int = 22) -> str:
    """Connect to a device and return its running config as a string."""
    device = {
        "device_type": "cisco_ios",
        "host": host,
        "username": username,
        "password": password,
        "port": port,
    }
    # TODO: Uncomment netmiko import above, then enable below:
    # with ConnectHandler(**device) as conn:
    #     return conn.send_command("show running-config")
    raise NotImplementedError("netmiko not yet installed. See setup instructions in README.")


def main():
    parser = argparse.ArgumentParser(description="Backup running config from a Cisco device.")
    parser.add_argument("--host", required=True, help="Device IP or hostname")
    parser.add_argument("--user", required=True, help="SSH username")
    parser.add_argument("--port", type=int, default=22, help="SSH port (default: 22)")
    args = parser.parse_args()

    password = os.environ.get("DEVICE_PASSWORD", "")
    if not password:
        import getpass
        password = getpass.getpass(f"Password for {args.user}@{args.host}: ")

    print(f"[*] Connecting to {args.host}:{args.port} ...")
    config = backup_device(args.host, args.user, password, args.port)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    outfile = f"backup_{args.host}_{timestamp}.txt"
    with open(outfile, "w") as f:
        f.write(config)
    print(f"[+] Config saved to {outfile}")


if __name__ == "__main__":
    main()
