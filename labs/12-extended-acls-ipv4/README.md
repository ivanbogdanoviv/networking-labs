# Lab 12 — Configure and Verify Extended IPv4 ACLs (5.5.2)

**Course:** CCNA Enterprise Networking, Security and Automation (CCNAv7)
**Platform:** NDG NETLAB+ / Cisco Packet Tracer
**Completed:** 2026-02-06 (practiced 3 times: Feb 6, Feb 12, Feb 19)
**Difficulty:** ⭐⭐⭐⭐

## Objective
Design and implement extended IPv4 ACLs to enforce network security policies. Block SSH from Sales VLAN to Management VLAN while permitting all other traffic. Block ICMP echo between Operations and Sales VLANs. Apply ACLs close to the source.

## Topology
```
PC-A (VLAN 20/Sales)      PC-B (VLAN 30/Operations)
        |                         |
      G0/0/1.20               G0/0/1.30
              \               /
               [R1 ISR4321]
               G0/0/1.40 (Mgmt)
                    |
               PC-C (VLAN 40/Management)
```

## Addressing Table
| Device | Interface | IP Address | Subnet Mask | Default Gateway |
|--------|-----------|------------|-------------|-----------------|
| R1 | G0/0/1.20 | 10.20.0.1 | 255.255.255.0 | — |
| R1 | G0/0/1.30 | 10.30.0.1 | 255.255.255.0 | — |
| R1 | G0/0/1.40 | 10.40.0.1 | 255.255.255.0 | — |
| PC-A | NIC | 10.20.0.10 | 255.255.255.0 | 10.20.0.1 |
| PC-B | NIC | 10.30.0.10 | 255.255.255.0 | 10.30.0.1 |
| PC-C | NIC | 10.40.0.10 | 255.255.255.0 | 10.40.0.1 |

## Security Policies Implemented
| Policy | Action | Source | Destination | Protocol |
|--------|--------|--------|-------------|----------|
| 1 | Deny | 10.40.0.0/24 (Sales) | 10.20.0.0/24 (Mgmt) | SSH (TCP 22) |
| 2 | Permit | Any | Any | IP |
| 3 | Deny | 10.30.0.0/24 (Ops) | 10.40.0.0/24 (Sales) | ICMP echo |
| 4 | Permit | Any | Any | IP |

## Key Configurations
### R1 — Extended ACLs
```
! ACL 101 — Applied to Sales VLAN sub-interface (blocks SSH to Mgmt)
R1(config)# access-list 101 remark ACL 101 fulfills policies 1,2,3
R1(config)# access-list 101 deny tcp 10.40.0.0 0.0.0.255 10.20.0.0 0.0.0.255 eq 22
R1(config)# access-list 101 permit ip any any

! ACL 102 — Applied to Operations VLAN sub-interface (blocks ICMP to Sales)
R1(config)# access-list 102 remark ACL 102 blocks ICMP from Ops to Sales
R1(config)# access-list 102 deny icmp 10.30.0.0 0.0.0.255 10.40.0.0 0.0.0.255 echo
R1(config)# access-list 102 permit ip any any

! Apply ACLs to sub-interfaces (inbound — near the source)
R1(config)# interface g0/0/1.40
R1(config-subif)# ip access-group 101 in

R1(config)# interface g0/0/1.30
R1(config-subif)# ip access-group 102 in
```

## Verification Commands
```
show access-lists
show ip interface g0/0/1.40
show ip interface g0/0/1.30
! Test permit:
ping 10.40.0.10                    ! should succeed
! Test deny:
ssh -l admin 10.20.0.10            ! should fail from Sales VLAN
ping 10.40.0.10 from Ops PC       ! should fail ICMP
```

## What I Learned
- Extended ACLs should be placed **near the source** to prevent unnecessary traffic traversing the network
- ACL syntax order: `access-list [number] [permit|deny] [protocol] [source] [wildcard] [dest] [wildcard] [operator port]`
- Wildcard masks are the inverse of subnet masks: 0.0.0.255 = 255.255.255.0 subnet
- There is always an implicit `deny all` at the end — always include an explicit `permit ip any any` when needed
- `show ip interface` shows which ACL is applied and in which direction

## Troubleshooting Notes
- Traffic being blocked unexpectedly: `show access-lists` shows match counts per ACE — look for unexpected hits
- ACL not matching: verify wildcard mask is correct (inverse of subnet mask)
- Applying ACL in wrong direction: extended ACLs near source = **in** on source-facing interface
- If entire network is blocked: missing `permit ip any any` at end of ACL
