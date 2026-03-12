#!/usr/bin/env python3
"""
subnet_calculator.py — Ivan Ivanov's CCNA Lab Utility
Given an IP and CIDR, outputs: network, broadcast, first/last usable, # of hosts
Usage: python3 subnet_calculator.py 192.168.1.0/24
"""
import ipaddress, sys

def calculate(cidr):
    net = ipaddress.IPv4Network(cidr, strict=False)
    hosts = list(net.hosts())
    print(f"\n{'='*45}")
    print(f"  Network:        {net.network_address}/{net.prefixlen}")
    print(f"  Subnet Mask:    {net.netmask}")
    print(f"  Broadcast:      {net.broadcast_address}")
    print(f"  First Usable:   {hosts[0] if hosts else 'N/A'}")
    print(f"  Last Usable:    {hosts[-1] if hosts else 'N/A'}")
    print(f"  Usable Hosts:   {len(hosts)}")
    print(f"  Total IPs:      {net.num_addresses}")
    print(f"{'='*45}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 subnet_calculator.py <IP/CIDR>")
        print("Example: python3 subnet_calculator.py 192.168.1.0/24")
        sys.exit(1)
    calculate(sys.argv[1])
