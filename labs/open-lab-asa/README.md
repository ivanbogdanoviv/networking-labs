# Open Lab — ASA Pod (Multi-Purpose Academy)

**Course:** CCNA Enterprise Networking, Security and Automation (CCNAv7)
**Platform:** NDG NETLAB+ / Cisco ASA
**Completed:** 2025-10-08, 2025-10-23
**Difficulty:** ⭐⭐⭐

## Objective
Open-ended exploration of the Cisco ASA (Adaptive Security Appliance) firewall platform. Configure basic ASA settings, assign security zones to interfaces, and understand the fundamental difference between stateful firewall policy and router ACLs.

## Topology
```
     [Internet/Outside]
            |
         Outside (Gi0/0) — Security Level 0
         [ASA 5505/5506]
         Inside  (Gi0/1) — Security Level 100
            |
       [Inside LAN]
            |
         DMZ (Gi0/2) — Security Level 50
            |
       [DMZ Servers]
```

## Addressing Table
| Device | Interface | IP Address | Subnet Mask | Security Level |
|--------|-----------|------------|-------------|----------------|
| ASA | Outside (Gi0/0) | 209.165.200.226 | 255.255.255.248 | 0 |
| ASA | Inside (Gi0/1) | 192.168.1.1 | 255.255.255.0 | 100 |
| ASA | DMZ (Gi0/2) | 192.168.2.1 | 255.255.255.0 | 50 |

## Key Configurations
### ASA — Basic Setup
```
! Hostname and domain
ciscoasa(config)# hostname ASA
ASA(config)# domain-name ccna-lab.com

! Interface config — Outside
ASA(config)# interface gigabitethernet 0/0
ASA(config-if)# nameif outside
ASA(config-if)# security-level 0
ASA(config-if)# ip address 209.165.200.226 255.255.255.248
ASA(config-if)# no shutdown

! Interface config — Inside
ASA(config)# interface gigabitethernet 0/1
ASA(config-if)# nameif inside
ASA(config-if)# security-level 100
ASA(config-if)# ip address 192.168.1.1 255.255.255.0
ASA(config-if)# no shutdown

! Interface config — DMZ
ASA(config)# interface gigabitethernet 0/2
ASA(config-if)# nameif dmz
ASA(config-if)# security-level 50
ASA(config-if)# ip address 192.168.2.1 255.255.255.0
ASA(config-if)# no shutdown

! Default route
ASA(config)# route outside 0.0.0.0 0.0.0.0 209.165.200.225

! SSH access from inside
ASA(config)# crypto key generate rsa modulus 2048
ASA(config)# username admin password adminpass privilege 15
ASA(config)# aaa authentication ssh console LOCAL
ASA(config)# ssh 192.168.1.0 255.255.255.0 inside
```

## Saved Configs Reference
| Date | Config Name | Notes |
|------|-------------|-------|
| 2025-10-08 | S1 | Initial basic ASA setup |
| 2025-10-08 | S2 | After interface configuration |
| 2025-10-08 | S3 | After routing and SSH config |
| 2025-10-23 | Review | Second session — revisited configs |

## What I Learned
- ASA security levels (0-100) control traffic flow: higher security can initiate to lower, not the reverse by default
- `nameif` is required on ASA interfaces — without it, the interface is inactive
- ASA is stateful: return traffic for inside-initiated connections is automatically allowed
- Unlike router ACLs, ASA requires explicit policy (ACL) to allow traffic from lower to higher security zones
- `show conn` shows all active connections through the ASA — stateful inspection in action

## Troubleshooting Notes
- Interface inactive: missing `nameif` command
- Traffic blocked from DMZ to Inside: need an ACL `access-group` applied to DMZ interface
- Can't SSH to ASA: verify `aaa authentication ssh console LOCAL` and user exists with correct privilege
- `show interface ip brief` on ASA shows all interface states and security levels
