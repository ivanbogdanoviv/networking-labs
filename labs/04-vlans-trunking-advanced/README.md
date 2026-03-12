# Lab 04 — Implement VLANs and Trunking (3.6.2)

**Course:** CCNA Enterprise Networking, Security and Automation (CCNAv7)
**Platform:** NDG NETLAB+ / Cisco Packet Tracer
**Completed:** 2025-10-30
**Difficulty:** ⭐⭐⭐

## Objective
Build on basic VLAN and trunking skills by configuring allowed VLANs on trunk links, enabling STP PortFast on access ports, and troubleshooting VLAN mismatches. Verify that only permitted VLANs cross trunk links.

## Topology
```
       PC-A (VLAN 20)    PC-B (VLAN 30)
           |                   |
         F0/6               F0/18
           |                   |
         [S1]====F0/1 trunk=====[S2]
                                 |
                              PC-C (VLAN 10)
                              PC-D (VLAN 30)
```

## Addressing Table
| Device | Interface | IP Address | Subnet Mask | Default Gateway |
|--------|-----------|------------|-------------|-----------------|
| S1 | VLAN 99 | 192.168.99.11 | 255.255.255.0 | 192.168.99.1 |
| S2 | VLAN 99 | 192.168.99.12 | 255.255.255.0 | 192.168.99.1 |
| PC-A | NIC | 192.168.20.3 | 255.255.255.0 | 192.168.20.1 |
| PC-B | NIC | 192.168.30.3 | 255.255.255.0 | 192.168.30.1 |
| PC-C | NIC | 192.168.10.3 | 255.255.255.0 | 192.168.10.1 |
| PC-D | NIC | 192.168.30.4 | 255.255.255.0 | 192.168.30.1 |

## Key Configurations
### S1 — Advanced Trunking
```
! Restrict which VLANs can cross the trunk
S1(config)# interface f0/1
S1(config-if)# switchport trunk allowed vlan 10,20,30,99
S1(config-if)# switchport nonegotiate

! PortFast on access ports (skips STP listening/learning)
S1(config)# interface range f0/6, f0/18
S1(config-if-range)# spanning-tree portfast
S1(config-if-range)# spanning-tree bpduguard enable

! VLAN pruning — remove VLAN 1 from trunk
S1(config)# interface f0/1
S1(config-if)# switchport trunk allowed vlan remove 1
```

### S2 — Mirror config
```
S2(config)# interface f0/1
S2(config-if)# switchport trunk allowed vlan 10,20,30,99
S2(config-if)# switchport nonegotiate

S2(config)# interface range f0/6, f0/18
S2(config-if-range)# spanning-tree portfast
S2(config-if-range)# spanning-tree bpduguard enable
```

## Verification Commands
```
show vlan brief
show interfaces trunk
show spanning-tree
show interfaces f0/1 switchport
show running-config | section interface
```

## What I Learned
- `switchport trunk allowed vlan` limits trunk to only necessary VLANs — reduces broadcast and improves security
- PortFast allows access ports to go straight to forwarding — critical for fast PC connectivity
- BPDUGuard shuts down a PortFast port if a switch is accidentally connected — prevents topology loops
- `switchport nonegotiate` disables DTP — hard-codes trunk mode without negotiation
- VLAN 1 on trunk links is a security risk — best practice is to remove it

## Troubleshooting Notes
- VLAN traffic not passing on trunk: check `show interfaces trunk` — VLAN must appear in "VLANs allowed and active" column
- Port not coming up fast after link up: PortFast not configured — STP is delaying forwarding
- BPDUGuard err-disabled port: a switch was connected to an access port — `no spanning-tree bpduguard enable` and investigate
