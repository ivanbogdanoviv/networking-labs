# networking-labs

Hands-on CCNA-style lab configurations, topologies, and automation scripts built while pursuing my **CompTIA Network+/CCNA** studies and directly supporting the **Home & Lab Network Design** project in my [portfolio](https://ivanbiv.lovable.app).

---

## Purpose

This repo documents real lab work: configuring VLANs, routing protocols, access control lists, and more — using Cisco Packet Tracer and GNS3. Each lab folder contains topology diagrams, device configs, and notes on what was learned.

The `scripts/` folder holds Python and Bash tools for automating repetitive tasks like backing up configs over SSH and verifying connectivity.

---

## Lab Index

| # | Topic | Tools | Status |
|---|-------|-------|--------|
| 01 | Basic VLAN Segmentation | Packet Tracer | In progress |
| 02 | OSPF Single-Area Routing | Packet Tracer / GNS3 | Planned |
| 03 | ACL Basics (Standard & Extended) | Packet Tracer | Planned |

---

## Folder Structure

```
networking-labs/
├── labs/
│   ├── 01-basic-vlan/          # VLAN configs, topology diagram
│   ├── 02-ospf-single-area/    # OSPF configs across multiple routers
│   └── 03-acl-basics/          # ACL permit/deny examples
├── scripts/
│   ├── backup_configs.py       # SSH into devices and dump running configs
│   └── verify_connectivity.sh  # Automated ping sweep for reachability tests
└── topologies/                 # .pkt and .gns3 topology save files
```

---

## How to Use

1. Open `.pkt` files in **Cisco Packet Tracer 8.x** or `.gns3` files in **GNS3 2.x**.
2. Device configs in each `labs/` subfolder mirror what's applied inside the topology.
3. To run automation scripts:

```bash
pip install netmiko
python scripts/backup_configs.py
```

---

## Key Commands Cheatsheet

```
# Show VLANs
show vlan brief

# Verify OSPF neighbors
show ip ospf neighbor

# Check ACL hits
show ip access-lists

# Backup running config via SSH (netmiko)
python scripts/backup_configs.py --host 192.168.1.1 --user admin
```

---

## Tech Stack

- Cisco IOS (Packet Tracer / GNS3)
- Python 3 + [netmiko](https://github.com/ktbyers/netmiko) for SSH automation
- Bash for connectivity testing
- Git for versioning configs

---

## Portfolio Connection

This repo supports the **Home & Lab Network Design** project on my [portfolio site](https://ivanbiv.lovable.app), which covers VLAN segmentation, inter-VLAN routing, and a layered home network topology built for study and real-world use.
