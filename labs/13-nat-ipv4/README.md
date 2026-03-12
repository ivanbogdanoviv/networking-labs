# Lab 13 — Configure NAT for IPv4 (6.8.2)

**Course:** CCNA Enterprise Networking, Security and Automation (CCNAv7)
**Platform:** NDG NETLAB+ / Cisco Packet Tracer
**Completed:** 2026-02-19
**Difficulty:** ⭐⭐⭐⭐

## Objective
Configure three forms of IPv4 NAT on a Cisco router: static NAT (one-to-one), dynamic NAT (pool), and PAT/overload (many-to-one). Verify that inside hosts can communicate with outside hosts using translated addresses.

## Topology
```
PC-A (192.168.1.10)
     |
  G0/0/1 (NAT inside)
  [R1 NAT Router]
  G0/0/0 (NAT outside)
     |
  [R2 simulates Internet]
  Loopback: 209.165.200.225/30
```

## Addressing Table
| Device | Interface | IP Address | Subnet Mask | Default Gateway |
|--------|-----------|------------|-------------|-----------------|
| R1 | G0/0/0 | 209.165.200.226 | 255.255.255.252 | — |
| R1 | G0/0/1 | 192.168.1.1 | 255.255.255.0 | — |
| R2 | G0/0/0 | 209.165.200.225 | 255.255.255.252 | — |
| R2 | Loopback0 | 209.165.200.225 | 255.255.255.252 | — |
| PC-A | NIC | 192.168.1.10 | 255.255.255.0 | 192.168.1.1 |
| PC-B | NIC | 192.168.1.11 | 255.255.255.0 | 192.168.1.1 |

## Key Configurations
### R1 — NAT Configuration
```
! Define inside and outside interfaces
R1(config)# interface g0/0/0
R1(config-if)# ip nat outside

R1(config)# interface g0/0/1
R1(config-if)# ip nat inside

! --- Static NAT: map PC-A to a fixed public IP ---
R1(config)# ip nat inside source static 192.168.1.2 209.165.200.229

! --- Dynamic NAT: pool of public addresses ---
R1(config)# access-list 1 permit 192.168.1.0 0.0.0.255
R1(config)# ip nat pool PUBLIC-ACCESS 209.165.200.226 209.165.200.240 netmask 255.255.255.224
R1(config)# ip nat inside source list 1 pool PUBLIC-ACCESS

! --- PAT / Overload: many-to-one using outside interface IP ---
R1(config)# ip nat inside source list 1 interface g0/0/0 overload
```

## Verification Commands
```
show ip nat translations
show ip nat statistics
debug ip nat
! Clear translations for testing:
clear ip nat translation *
! Test:
ping 209.165.200.225 source 192.168.1.10
```

## What I Learned
- NAT requires exactly two declarations: `ip nat inside` and `ip nat outside` on correct interfaces
- Static NAT: one inside IP → one outside IP, always the same mapping (used for servers)
- Dynamic NAT: pool of public IPs assigned first-come-first-served; pool can be exhausted
- PAT (overload): all inside hosts share ONE public IP, differentiated by port number — most common in homes/SMBs
- `show ip nat translations` shows all active NAT entries including protocol/port for PAT entries

## Troubleshooting Notes
- NAT not translating: verify ACL matches the correct inside network
- `debug ip nat` shows real-time translations — use carefully in production (CPU intensive)
- Static NAT conflict: can't have same inside/outside IP used in both static and dynamic NAT
- `clear ip nat translation *` removes all dynamic entries — useful for testing
- Pool exhausted: `show ip nat statistics` shows "miss" count — consider PAT overload instead
