# Lab 01 — Basic Switch Configuration (1.1.7)

**Course:** CCNA Enterprise Networking, Security and Automation (CCNAv7)
**Platform:** NDG NETLAB+ / Cisco Packet Tracer
**Completed:** 2025-10-30
**Difficulty:** ⭐⭐

## Objective
Configure basic security and management settings on a Cisco switch. Apply hostname, passwords, banners, and SSH preparation to harden an unconfigured switch. Save the configuration to NVRAM.

## Topology
```
   PC-A           PC-B
    |               |
  F0/6            F0/18
    |               |
  [S1 - 2960 Switch]
    |
  Console/Mgmt (VLAN 1: 192.168.1.2/24)
```

## Addressing Table
| Device | Interface | IP Address | Subnet Mask | Default Gateway |
|--------|-----------|------------|-------------|-----------------|
| S1 | VLAN 1 | 192.168.1.2 | 255.255.255.0 | 192.168.1.1 |
| PC-A | NIC | 192.168.1.10 | 255.255.255.0 | 192.168.1.1 |
| PC-B | NIC | 192.168.1.11 | 255.255.255.0 | 192.168.1.1 |

## Key Configurations
### S1 — Initial Hardening
```
Switch> enable
Switch# configure terminal
Switch(config)# hostname S1
S1(config)# enable secret class
S1(config)# no ip domain-lookup
S1(config)# service password-encryption
S1(config)# banner motd # Authorized Access Only #

! Console password
S1(config)# line console 0
S1(config-line)# password cisco
S1(config-line)# login
S1(config-line)# logging synchronous

! VTY password
S1(config)# line vty 0 15
S1(config-line)# password cisco
S1(config-line)# login

! Management IP
S1(config)# interface vlan 1
S1(config-if)# ip address 192.168.1.2 255.255.255.0
S1(config-if)# no shutdown

! Save
S1# copy running-config startup-config
```

## Verification Commands
```
show running-config
show version
show interfaces vlan 1
show ip interface brief
```

## What I Learned
- Every network device needs a minimum baseline config before deployment
- `enable secret` is hashed (MD5), much stronger than `enable password`
- `service password-encryption` encrypts all plaintext passwords in running-config
- `no ip domain-lookup` prevents the switch from trying DNS when you mistype a command
- `copy run start` saves to NVRAM — without this, a reload wipes your config

## Troubleshooting Notes
- If console password doesn't work: check `login` is set on line console 0
- If VLAN 1 interface shows administratively down: `no shutdown` was missed
- Banner shows up before login prompt — verify with `show running-config | section banner`
