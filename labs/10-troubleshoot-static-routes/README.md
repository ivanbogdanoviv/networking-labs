# Lab 10 — Troubleshoot IPv4 and IPv6 Static and Default Routes (16.3.2)

**Course:** CCNA Enterprise Networking, Security and Automation (CCNAv7)
**Platform:** NDG NETLAB+ / Cisco Packet Tracer
**Completed:** 2025-11-26
**Difficulty:** ⭐⭐⭐⭐

## Objective
Start with a broken multi-router topology containing intentional misconfigurations and systematically troubleshoot IPv4 and IPv6 static routing issues using the OSI model approach. Document each fault found and the fix applied.

## Topology
```
PC-A           PC-B            PC-C
  |              |                |
G0/0/0        G0/0/0           G0/0/0
[R1]===S0/0/0===S0/0/0===[R2]===G0/0/1===G0/0/1===[R3]
172.16.3.0/24        10.1.1.0/30        172.16.1.0/24
```

## Addressing Table
| Device | Interface | IPv4 Address | IPv6 Address | Default Gateway |
|--------|-----------|--------------|--------------|-----------------|
| R1 | G0/0/0 | 172.16.3.1/24 | 2001:db8:acad:2::1/64 | — |
| R1 | S0/0/0 | 172.16.2.1/30 | 2001:db8:acad:1::1/64 | — |
| R2 | S0/0/0 | 172.16.2.2/30 | 2001:db8:acad:1::2/64 | — |
| R2 | S0/0/1 | 192.168.1.2/30 | 2001:db8:acad:3::2/64 | — |
| R3 | G0/0/1 | 192.168.0.1/24 | 2001:db8:acad:4::1/64 | — |

## Troubleshooting Methodology
```
Step 1: Define the problem
  - Which pings fail?
  - ping 192.168.0.10 from R1 -> FAIL

Step 2: Check Layer 1/2 (physical)
  show ip interface brief    ! look for down/down interfaces
  show interfaces s0/0/0     ! check line and protocol status

Step 3: Check Layer 3 (routing table)
  show ip route              ! is the destination network present?
  show ipv6 route            ! check IPv6 routing table

Step 4: Check configuration
  show running-config        ! look for typos in static routes

Step 5: Test hop by hop
  ping [next-hop-IP]         ! verify each segment individually
  traceroute [destination]   ! identify where packets stop
```

## Faults Found and Fixed
```
! Fault 1: R1 missing route to 192.168.0.0/24
show ip route -> no entry for 192.168.0.0
Fix: ip route 192.168.0.0 255.255.255.0 172.16.2.2

! Fault 2: R2 S0/0/1 shutdown
show ip interface brief -> S0/0/1 administratively down
Fix: interface s0/0/1 -> no shutdown

! Fault 3: R3 return route pointing to wrong next-hop
show ip route -> default route next-hop was 192.168.1.3 (typo)
Fix: no ip route 0.0.0.0 0.0.0.0 192.168.1.3
     ip route 0.0.0.0 0.0.0.0 192.168.1.2

! Fault 4: IPv6 routing not enabled on R2
show ipv6 route -> no routes
Fix: ipv6 unicast-routing
```

## Verification Commands
```
show ip interface brief
show ip route
show ipv6 route
show running-config | section ip route
ping 192.168.0.10 source 172.16.3.10
traceroute 192.168.0.10
ping ipv6 2001:db8:acad:4::10 source 2001:db8:acad:2::10
```

## What I Learned
- Always troubleshoot bottom-up: physical → data link → network
- `show ip interface brief` reveals all interface states in one view — start here
- A route existing in the table doesn't mean traffic flows — return route must exist too
- `traceroute` shows exactly which hop the packet reaches before failing
- IPv6 troubleshooting step 1: verify `ipv6 unicast-routing` is enabled on ALL routers

## Troubleshooting Notes
- One-way communication (can ping TO a host but not FROM it): missing return route
- "Destination host unreachable" vs "Request timed out": unreachable = L3 issue, timed out = L4/firewall
- Always verify both directions of routing — asymmetric routes cause subtle failures
