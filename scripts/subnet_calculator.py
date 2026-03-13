#!/usr/bin/env python3
"""
subnet_calculator.py — CCNA Subnet Calculator
Supports CIDR notation (192.168.1.0/24) or IP + mask (192.168.1.0 255.255.255.0).
Shows network, broadcast, first/last host, wildcard mask, total hosts.
Use --split N to divide the network into N equal subnets.

Usage:
  python3 subnet_calculator.py 192.168.1.0/24
  python3 subnet_calculator.py 192.168.1.0 255.255.255.0
  python3 subnet_calculator.py 10.0.0.0/8 --split 4
"""

import ipaddress
import sys
import math

# ── ANSI color codes (no external deps) ──────────────────────
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def color(text, code):
    return f"{code}{text}{RESET}"

def print_network(net, label=None):
    hosts     = list(net.hosts())
    total     = net.num_addresses
    usable    = len(hosts)
    wildcard  = ipaddress.IPv4Address(int(net.hostmask))

    header = label if label else f"Network: {net}"
    print(color(f"\n{'='*50}", CYAN))
    print(color(f"  {header}", BOLD))
    print(color(f"{'='*50}", CYAN))
    print(f"  {'Network Address':<22} {color(str(net.network_address) + '/' + str(net.prefixlen), GREEN)}")
    print(f"  {'Subnet Mask':<22} {color(str(net.netmask), GREEN)}")
    print(f"  {'Wildcard Mask':<22} {color(str(wildcard), YELLOW)}")
    print(f"  {'Broadcast':<22} {color(str(net.broadcast_address), RED)}")
    if usable > 0:
        print(f"  {'First Usable Host':<22} {color(str(hosts[0]), GREEN)}")
        print(f"  {'Last Usable Host':<22} {color(str(hosts[-1]), GREEN)}")
    else:
        print(f"  {'First Usable Host':<22} {color('N/A (host route)', YELLOW)}")
        print(f"  {'Last Usable Host':<22} {color('N/A (host route)', YELLOW)}")
    print(f"  {'Usable Hosts':<22} {color(str(usable), GREEN)}")
    print(f"  {'Total Addresses':<22} {color(str(total), CYAN)}")
    print(color(f"{'='*50}", CYAN))

def split_network(net, n):
    """Divide net into n equal subnets."""
    if n < 2:
        print(color("  --split requires N >= 2", RED))
        sys.exit(1)

    bits_needed = math.ceil(math.log2(n))
    new_prefix  = net.prefixlen + bits_needed

    if new_prefix > 32:
        print(color(f"  Cannot split /{net.prefixlen} into {n} subnets — not enough host bits.", RED))
        sys.exit(1)

    subnets = list(net.subnets(new_prefix=new_prefix))
    actual  = len(subnets)

    print(color(f"\n  Splitting {net} into {actual} subnets (/{new_prefix}):", BOLD))

    for i, subnet in enumerate(subnets[:n], 1):
        print_network(subnet, label=f"Subnet {i} of {n}: {subnet}")

    if actual > n:
        print(color(f"\n  Note: {actual - n} extra subnet(s) available in the address space.", YELLOW))

def parse_input(args):
    """Return an IPv4Network from either 'IP/prefix' or 'IP mask' args."""
    if len(args) == 1:
        # CIDR notation
        return ipaddress.IPv4Network(args[0], strict=False)
    elif len(args) == 2 and not args[1].startswith("--"):
        # IP + dotted mask
        ip, mask = args[0], args[1]
        prefix = ipaddress.IPv4Network(f"0.0.0.0/{mask}", strict=False).prefixlen
        return ipaddress.IPv4Network(f"{ip}/{prefix}", strict=False)
    else:
        return None

def usage():
    print(f"""
{color('subnet_calculator.py', BOLD)} — CCNA Subnet Calculator

{color('Usage:', CYAN)}
  python3 subnet_calculator.py <IP/CIDR>
  python3 subnet_calculator.py <IP> <SubnetMask>
  python3 subnet_calculator.py <IP/CIDR> --split <N>

{color('Examples:', CYAN)}
  python3 subnet_calculator.py 192.168.1.0/24
  python3 subnet_calculator.py 192.168.1.0 255.255.255.0
  python3 subnet_calculator.py 10.0.0.0/8 --split 4
  python3 subnet_calculator.py 172.16.0.0/16 --split 8
""")

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        usage()
        sys.exit(1)

    # Pull out --split N if present
    split_n = None
    clean_args = []
    i = 0
    while i < len(args):
        if args[i] == "--split":
            if i + 1 >= len(args):
                print(color("  --split requires a number argument", RED))
                sys.exit(1)
            try:
                split_n = int(args[i + 1])
            except ValueError:
                print(color(f"  Invalid split count: {args[i+1]}", RED))
                sys.exit(1)
            i += 2
        else:
            clean_args.append(args[i])
            i += 1

    net = parse_input(clean_args)
    if net is None:
        usage()
        sys.exit(1)

    try:
        print_network(net)
        if split_n:
            split_network(net, split_n)
        print()
    except ValueError as e:
        print(color(f"  Error: {e}", RED))
        sys.exit(1)
