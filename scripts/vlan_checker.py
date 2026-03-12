#!/usr/bin/env python3
"""
vlan_checker.py — Parse a Cisco 'show vlan brief' output file and summarize
Usage: python3 vlan_checker.py show_vlan_brief.txt
"""
import sys, re

def parse_vlan(filepath):
    with open(filepath) as f:
        lines = f.readlines()
    print(f"\n{'VLAN':<8} {'Name':<20} {'Status':<12} {'Ports'}")
    print("-" * 60)
    for line in lines:
        m = re.match(r'^(\d+)\s+(\S+)\s+(active|act/unsup)\s*(.*)', line)
        if m:
            print(f"{m.group(1):<8} {m.group(2):<20} {m.group(3):<12} {m.group(4)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 vlan_checker.py <show_vlan_brief.txt>")
        sys.exit(1)
    parse_vlan(sys.argv[1])
