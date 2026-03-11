#!/usr/bin/env bash
# verify_connectivity.sh — Ping sweep to test reachability across lab subnets.
#
# Usage:
#   chmod +x verify_connectivity.sh
#   ./verify_connectivity.sh
#
# TODO: Edit HOSTS array below to match your lab topology.

set -euo pipefail

HOSTS=(
  "192.168.10.1"   # SW1 management
  "192.168.10.2"   # SW2 management
  "10.0.12.1"      # R1 Gi0/0
  "10.0.12.2"      # R2 Gi0/0
)

PASS=0
FAIL=0

echo "=== Connectivity Check — $(date) ==="
echo ""

for host in "${HOSTS[@]}"; do
  if ping -c 2 -W 1 "$host" &>/dev/null; then
    echo "  [OK]   $host"
    ((PASS++))
  else
    echo "  [FAIL] $host — unreachable"
    ((FAIL++))
  fi
done

echo ""
echo "Results: $PASS reachable, $FAIL unreachable"
echo "========================================"

if [[ $FAIL -gt 0 ]]; then
  exit 1
fi
