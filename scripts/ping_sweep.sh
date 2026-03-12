#!/bin/bash
# ping_sweep.sh — Quick /24 host discovery
# Usage: ./ping_sweep.sh 192.168.1
# Pings 192.168.1.1 through 192.168.1.254 and reports live hosts

SUBNET=${1:-"192.168.1"}
echo "Scanning $SUBNET.0/24..."
echo "Live hosts:"
for i in $(seq 1 254); do
    ping -c 1 -W 1 "$SUBNET.$i" &>/dev/null && echo "  UP: $SUBNET.$i" &
done
wait
echo "Scan complete."
