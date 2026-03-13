#!/usr/bin/env python3
"""
vlan_checker.py — Parse Cisco 'show vlan brief' + 'show interfaces trunk' output.
Supports a single file or a directory of .txt switch output files.
Flags: VLANs in trunk allowed list but not active, VLANs with no ports.
Exports results to CSV with -o <file>.

Usage:
  python3 vlan_checker.py show_vlan_brief.txt
  python3 vlan_checker.py ./switch-outputs/
  python3 vlan_checker.py ./switch-outputs/ -o results.csv
"""

import sys
import re
import os
import csv
import argparse
from pathlib import Path

# ── ANSI colors ───────────────────────────────────────────────
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def c(text, code):
    return f"{code}{text}{RESET}"

# ── Parsers ───────────────────────────────────────────────────

def parse_vlan_brief(text):
    """Return dict: {vlan_id: {'name': str, 'status': str, 'ports': [str]}}"""
    vlans = {}
    for line in text.splitlines():
        m = re.match(r'^(\d+)\s+(\S+)\s+(active|act/unsup|suspended)\s*(.*)', line)
        if m:
            vlan_id  = int(m.group(1))
            ports    = [p.strip() for p in m.group(4).split(",") if p.strip()] if m.group(4) else []
            vlans[vlan_id] = {
                "name":   m.group(2),
                "status": m.group(3),
                "ports":  ports,
            }
    return vlans

def parse_trunk_allowed(text):
    """
    Parse 'show interfaces trunk' output.
    Returns dict: {interface: {'allowed': set(int), 'active': set(int)}}
    Very simplified parser — looks for the Vlans-allowed and active blocks.
    """
    trunks = {}
    current_iface = None
    section = None

    for line in text.splitlines():
        # Detect interface line: "Gi0/1   on   802.1q   trunking   1"
        iface_m = re.match(r'^(\S+)\s+(on|auto|desirable|trunk)\s+802\.1q\s+\S+\s+(\d+)', line)
        if iface_m:
            current_iface = iface_m.group(1)
            trunks.setdefault(current_iface, {"allowed": set(), "active": set()})
            continue

        if "Vlans allowed on trunk" in line:
            section = "allowed"
            continue
        if "Vlans allowed and active" in line:
            section = "active"
            continue
        if "Vlans in spanning tree" in line or re.match(r'^Port\s+', line):
            section = None
            continue

        if section and current_iface:
            # Parse comma-separated VLAN ranges like "1-10,20,30,99"
            for part in re.split(r',\s*', line.strip()):
                part = part.strip()
                if not part:
                    continue
                range_m = re.match(r'^(\d+)-(\d+)$', part)
                if range_m:
                    for v in range(int(range_m.group(1)), int(range_m.group(2)) + 1):
                        trunks[current_iface][section].add(v)
                elif re.match(r'^\d+$', part):
                    trunks[current_iface][section].add(int(part))
    return trunks

def analyze(filename, text):
    """
    Run all checks on a single device output file.
    Returns list of result dicts.
    """
    vlans  = parse_vlan_brief(text)
    trunks = parse_trunk_allowed(text)

    # Aggregate all VLAN IDs seen in trunk allowed lists
    all_trunk_allowed = set()
    all_trunk_active  = set()
    for iface_data in trunks.values():
        all_trunk_allowed |= iface_data["allowed"]
        all_trunk_active  |= iface_data["active"]

    results = []

    for vlan_id, info in sorted(vlans.items()):
        if vlan_id == 1:
            continue  # skip default VLAN

        issues = []

        # VLANs with no ports assigned
        if not info["ports"]:
            issues.append("No active ports")

        # VLAN in allowed trunk list but not showing as active
        if all_trunk_allowed and vlan_id in all_trunk_allowed and vlan_id not in all_trunk_active:
            issues.append("In trunk allowed list but NOT active on trunk")

        # VLAN active on trunk but NOT in allowed list (pruned or misconfigured)
        if all_trunk_allowed and vlan_id not in all_trunk_allowed and vlan_id in all_trunk_active:
            issues.append("Active on trunk but NOT in allowed list")

        results.append({
            "file":    os.path.basename(filename),
            "vlan":    vlan_id,
            "name":    info["name"],
            "status":  info["status"],
            "ports":   ", ".join(info["ports"]) if info["ports"] else "—",
            "issues":  "; ".join(issues) if issues else "OK",
        })

    return results

def print_results(results, filename):
    print(c(f"\n{'='*70}", CYAN))
    print(c(f"  File: {filename}", BOLD))
    print(c(f"{'='*70}", CYAN))
    fmt = f"{'VLAN':<8} {'Name':<20} {'Status':<14} {'Ports':<30} {'Issues'}"
    print(c(fmt, BOLD))
    print("-" * 90)

    for r in results:
        issues = r["issues"]
        if issues == "OK":
            issue_str = c("OK", GREEN)
        elif "allowed list but NOT active" in issues:
            issue_str = c(issues, YELLOW)
        elif "No active ports" in issues and "NOT" not in issues:
            issue_str = c(issues, YELLOW)
        else:
            issue_str = c(issues, RED)

        line = f"{r['vlan']:<8} {r['name']:<20} {r['status']:<14} {r['ports']:<30}"
        print(f"{line} {issue_str}")

    total   = len(results)
    ok      = sum(1 for r in results if r["issues"] == "OK")
    flagged = total - ok
    print()
    print(c(f"  Total VLANs: {total}  |  OK: {ok}  |  Flagged: {flagged}", CYAN))
    print()

def export_csv(all_results, outfile):
    fieldnames = ["file", "vlan", "name", "status", "ports", "issues"]
    with open(outfile, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)
    print(c(f"\n  Results exported to: {outfile}", GREEN))

# ── Main ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Check Cisco VLAN configuration from show vlan brief output files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 vlan_checker.py show_vlan_brief.txt
  python3 vlan_checker.py ./switch-outputs/
  python3 vlan_checker.py ./switch-outputs/ -o results.csv
        """
    )
    parser.add_argument("path", help="Single .txt file or directory of .txt files")
    parser.add_argument("-o", "--output", metavar="CSV_FILE",
                        help="Export results to a CSV file")
    args = parser.parse_args()

    target = Path(args.path)
    files  = []

    if target.is_dir():
        files = sorted(target.glob("*.txt"))
        if not files:
            print(c(f"  No .txt files found in {target}", RED))
            sys.exit(1)
    elif target.is_file():
        files = [target]
    else:
        print(c(f"  Path not found: {target}", RED))
        sys.exit(1)

    all_results = []

    for fpath in files:
        try:
            text = fpath.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            print(c(f"  Could not read {fpath}: {e}", RED))
            continue

        results = analyze(str(fpath), text)
        if results:
            print_results(results, fpath.name)
            all_results.extend(results)
        else:
            print(c(f"\n  {fpath.name}: no VLAN data found (check file format)", YELLOW))

    if args.output and all_results:
        export_csv(all_results, args.output)
    elif args.output and not all_results:
        print(c("  No results to export.", YELLOW))

if __name__ == "__main__":
    main()
