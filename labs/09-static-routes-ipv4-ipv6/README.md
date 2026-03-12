# Lab 09 — Configure IPv4 and IPv6 Static and Default Routes (15.6.2)

**Course:** CCNA Enterprise Networking, Security and Automation (CCNAv7)
**Platform:** NDG NETLAB+ / Cisco Packet Tracer
**Completed:** 2025-11-11 (practiced again 2025-11-19)
**Difficulty:** ⭐⭐⭐

## Objective
Configure IPv4 and IPv6 static routes, default routes, and floating static routes on a multi-router topology. Verify end-to-end reachability across all subnets using both IPv4 and IPv6 addressing.

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
| R3 | G0/0/0 | 192.168.1.1/30 | 2001:db8:acad:3::1/64 | — |
| R3 | G0/0/1 | 192.168.0.1/24 | 2001:db8:acad:4::1/64 | — |
| PC-A | NIC | 172.16.3.10/24 | 2001:db8:acad:2::10/64 | 172.16.3.1 |
| PC-C | NIC | 192.168.0.10/24 | 2001:db8:acad:4::10/64 | 192.168.0.1 |

## Key Configurations
### R1 — IPv4 and IPv6 Static Routes
```
! Enable IPv6 routing
R1(config)# ipv6 unicast-routing

! IPv4 static routes
R1(config)# ip route 192.168.1.0 255.255.255.252 172.16.2.2
R1(config)# ip route 192.168.0.0 255.255.255.0 172.16.2.2
! IPv4 default route
R1(config)# ip route 0.0.0.0 0.0.0.0 172.16.2.2

! IPv6 static routes
R1(config)# ipv6 route 2001:db8:acad:3::/64 2001:db8:acad:1::2
R1(config)# ipv6 route 2001:db8:acad:4::/64 2001:db8:acad:1::2
! IPv6 default route
R1(config)# ipv6 route ::/0 2001:db8:acad:1::2

! Floating static (backup via higher AD)
R1(config)# ip route 0.0.0.0 0.0.0.0 172.16.2.2 5
```

### R3 — Return routes
```
R3(config)# ipv6 unicast-routing
R3(config)# ip route 0.0.0.0 0.0.0.0 192.168.1.2
R3(config)# ipv6 route ::/0 2001:db8:acad:3::2
```

## Verification Commands
```
show ip route
show ipv6 route
show ip route static
ping 192.168.0.10 source 172.16.3.10
traceroute 192.168.0.10
ping ipv6 2001:db8:acad:4::10
```

## What I Learned
- Static routes require the network, mask, and next-hop (or exit interface) — no automatic updates
- Default route `0.0.0.0 0.0.0.0` matches any destination not in the routing table — "gateway of last resort"
- IPv6 requires `ipv6 unicast-routing` command — it's disabled by default on Cisco IOS
- Floating static routes use a higher AD (e.g., AD 5) to serve as backup when the primary route fails
- `traceroute` shows each hop — invaluable for determining where traffic is being dropped

## Troubleshooting Notes
- Route in table but traffic not flowing: check return route exists in the other direction
- IPv6 ping fails: verify `ipv6 unicast-routing` is enabled on all routers
- `show ip route` shows "S" for static, "S*" for default static, "S [1/0]" shows AD/metric
