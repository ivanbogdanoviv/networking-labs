# Lab 01 – Basic VLAN Configuration

![Network Topology](../../screenshots/03-vlans-trunking.png)

## Objective
Configure and verify VLANs on a single switch. Assign ports to VLANs and verify VLAN database.

## Topology
- S1 (2960 switch)
- PC-A → F0/6 (VLAN 10)
- PC-B → F0/11 (VLAN 20)

## Address Table
| Device | Interface | VLAN | IP Address |
|--------|-----------|------|------------|
| S1 | VLAN 1 | 1 | 192.168.1.1/24 |
| PC-A | NIC | 10 | 192.168.10.3/24 |
| PC-B | NIC | 20 | 192.168.20.3/24 |

## Key Commands
```
vlan 10
 name Student
vlan 20
 name Faculty
interface f0/6
 switchport mode access
 switchport access vlan 10
show vlan brief
```

## Verification
- `show vlan brief` — confirm VLANs exist and ports assigned
- `show interfaces trunk` — confirm no unintended trunking
- PC-A cannot ping PC-B (different VLANs, no routing)

## Learning Outcomes
- Create and name VLANs
- Assign switch ports to VLANs
- Verify VLAN configuration using show commands
