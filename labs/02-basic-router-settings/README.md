# Lab 02 — Basic Router Settings (1.6.2)

**Course:** CCNA Enterprise Networking, Security and Automation (CCNAv7)
**Platform:** NDG NETLAB+ / Cisco Packet Tracer
**Completed:** 2025-10-30
**Difficulty:** ⭐⭐

## Objective
Configure basic settings on a Cisco router including hostname, interface IP addressing, SSH, and default routing. Verify end-to-end connectivity between two PC subnets through the router.

## Topology
```
PC-A (192.168.0.10)
     |
   G0/0/0 (192.168.0.1)
   [R1 ISR4321]
   G0/0/1 (192.168.1.1)
     |
   [S1]
     |
   PC-B (192.168.1.10)
```

## Addressing Table
| Device | Interface | IP Address | Subnet Mask | Default Gateway |
|--------|-----------|------------|-------------|-----------------|
| R1 | G0/0/0 | 192.168.0.1 | 255.255.255.0 | — |
| R1 | G0/0/1 | 192.168.1.1 | 255.255.255.0 | — |
| S1 | VLAN 1 | 192.168.1.2 | 255.255.255.0 | 192.168.1.1 |
| PC-A | NIC | 192.168.0.10 | 255.255.255.0 | 192.168.0.1 |
| PC-B | NIC | 192.168.1.10 | 255.255.255.0 | 192.168.1.1 |

## Key Configurations
### R1 — Interface and Basic Config
```
Router> enable
Router# configure terminal
Router(config)# hostname R1
R1(config)# enable secret class
R1(config)# no ip domain-lookup
R1(config)# service password-encryption

! Interface G0/0/0
R1(config)# interface g0/0/0
R1(config-if)# description Link to PC-A LAN
R1(config-if)# ip address 192.168.0.1 255.255.255.0
R1(config-if)# no shutdown

! Interface G0/0/1
R1(config)# interface g0/0/1
R1(config-if)# description Link to S1/PC-B LAN
R1(config-if)# ip address 192.168.1.1 255.255.255.0
R1(config-if)# no shutdown

! SSH
R1(config)# ip domain-name ccna-lab.com
R1(config)# crypto key generate rsa modulus 2048
R1(config)# username admin secret adminpass
R1(config)# line vty 0 4
R1(config-line)# transport input ssh
R1(config-line)# login local

R1# copy running-config startup-config
```

## Verification Commands
```
show ip interface brief
show running-config
show interfaces g0/0/0
show version
ping 192.168.1.10
```

## What I Learned
- Interfaces on routers are shutdown by default — always `no shutdown`
- Each router interface connects a different subnet; the router knows both networks automatically
- SSH requires: `ip domain-name`, RSA keys, a local user account, and `transport input ssh`
- `show ip interface brief` is the fastest way to verify all interface states at once
- Router does not need a default gateway — it routes between networks itself

## Troubleshooting Notes
- Interface shows "down/down": physically disconnected cable or other end is off
- Interface shows "up/down" (line protocol): Layer 2 problem — encapsulation mismatch or far end down
- Can't SSH: verify domain-name is set and RSA key was generated with sufficient modulus (2048+)
