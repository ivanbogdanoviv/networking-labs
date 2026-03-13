# Cisco IOS Quick Command Reference

A field-ready reference for the most-used IOS commands across all CCNA topics.
Each entry shows the command, what it does, and example output or context.

---

## Basic Device Setup

| Command | What It Does | Example / Notes |
|---|---|---|
| `hostname <name>` | Sets the device hostname | `hostname SW1` |
| `enable secret <password>` | Sets encrypted privileged mode password | `enable secret Cisco123!` |
| `service password-encryption` | Encrypts all plaintext passwords in config | Applies type 7 encryption to VTY/console passwords |
| `no ip domain-lookup` | Disables DNS lookup on mistyped commands | Prevents 30-second hang on console mistype |
| `banner motd ^ text ^` | Sets a login warning banner | Required by security policy; shown before login |
| `clock set 10:00:00 13 Feb 2026` | Manually sets system clock | Use before enabling logging timestamps |
| `copy running-config startup-config` | Saves config to NVRAM | Short form: `wr` or `write memory` |
| `show running-config` | Displays active configuration | Pipe with `| section <keyword>` to filter |
| `show startup-config` | Displays saved NVRAM config | Useful after reboot to verify save |
| `reload` | Reboots the device | Prompts to save unsaved changes first |

---

## VLAN Configuration

| Command | What It Does | Example / Notes |
|---|---|---|
| `vlan <id>` → `name <name>` | Creates a VLAN and names it | `vlan 10` then `name Sales` |
| `show vlan brief` | Lists all VLANs, status, and assigned ports | First command to run when diagnosing VLAN issues |
| `switchport mode access` | Sets port as access (single VLAN) | Applied per interface |
| `switchport access vlan <id>` | Assigns port to a VLAN | `switchport access vlan 10` |
| `spanning-tree portfast` | Bypasses STP listening/learning on access ports | Safe on ports connected to end devices only |

**Example — show vlan brief:**
```
VLAN Name                             Status    Ports
---- -------------------------------- --------- ---
1    default                          active    Fa0/6, Fa0/7
10   Sales                            active    Fa0/1, Fa0/2
20   IT                               active    Fa0/3, Fa0/4
30   Management                       active    Fa0/5
```

---

## Trunking (802.1Q)

| Command | What It Does | Example / Notes |
|---|---|---|
| `switchport mode trunk` | Forces port into trunk mode | Both ends must agree or use `dynamic desirable` |
| `switchport trunk native vlan <id>` | Sets native VLAN for untagged frames | Must match on both ends — default is VLAN 1 |
| `switchport trunk allowed vlan <list>` | Sets allowed VLANs on trunk | `allowed vlan 10,20,30` or `allowed vlan add 40` |
| `show interfaces trunk` | Shows trunk status, native VLAN, and allowed VLANs | Best command for trunk troubleshooting |
| `show interfaces <if> switchport` | Full switchport detail — mode, VLANs, status | Use when `show trunk` output is unclear |

**Example — show interfaces trunk:**
```
Port        Mode         Encapsulation  Status        Native vlan
Gi0/1       on           802.1q         trunking      99

Port        Vlans allowed on trunk
Gi0/1       10,20,30,99
```

---

## Routing

| Command | What It Does | Example / Notes |
|---|---|---|
| `ip route <network> <mask> <next-hop>` | Adds a static route | `ip route 0.0.0.0 0.0.0.0 10.0.0.1` (default route) |
| `show ip route` | Displays the routing table | `C`=connected, `S`=static, `O`=OSPF, `R`=RIP |
| `show ip interface brief` | Lists all interfaces with IP, status, protocol | Most-used single diagnostic command |
| `interface <if>.<subif>` + `encapsulation dot1Q <vlan>` | Creates ROAS subinterface | Used in Router-on-a-Stick inter-VLAN routing |
| `ip helper-address <server>` | Forwards DHCP broadcasts to a DHCP server | Applied to router interface facing DHCP clients |

**Example — show ip route:**
```
Gateway of last resort is 10.0.0.1 to network 0.0.0.0

C    192.168.10.0/24 is directly connected, Gi0/0.10
O    192.168.20.0/24 [110/2] via 10.0.12.2, Gi0/1
S*   0.0.0.0/0 [1/0] via 10.0.0.1
```

---

## OSPF

| Command | What It Does | Example / Notes |
|---|---|---|
| `router ospf <pid>` | Enters OSPF configuration mode | Process ID is local — does not need to match peers |
| `router-id <A.B.C.D>` | Manually sets router ID | Best practice: use loopback IP; set before `network` stmts |
| `network <ip> <wildcard> area <n>` | Enables OSPF on matching interfaces | `network 10.0.12.0 0.0.0.3 area 0` |
| `passive-interface <if>` | Stops OSPF hellos on an interface (still advertises) | Use on LAN-facing and loopback interfaces |
| `show ip ospf neighbor` | Shows OSPF adjacency table | State should be `FULL` for a healthy neighbor |
| `show ip ospf interface brief` | Shows OSPF-enabled interfaces, cost, DR/BDR state | Quick OSPF health check |

**Example — show ip ospf neighbor:**
```
Neighbor ID     Pri   State           Dead Time   Address         Interface
2.2.2.2           0   FULL/  -        00:00:38    10.0.12.2       GigabitEthernet0/1
```

---

## ACLs

| Command | What It Does | Example / Notes |
|---|---|---|
| `ip access-list extended <name>` | Creates a named extended ACL | Enter ACL config mode — add `permit`/`deny` lines |
| `deny tcp <src> <wild> any eq 23` | Deny Telnet from source | Ports: 23=Telnet, 22=SSH, 80=HTTP, 443=HTTPS |
| `permit ip any any` | Explicit permit-all (prevents implicit deny drop) | Always add at the end of an ACL unless full block intended |
| `ip access-group <name> in\|out` | Applies ACL to interface in a direction | `in` = traffic arriving; `out` = traffic leaving |
| `show ip access-lists` | Shows ACLs with hit counts | Zero hits = ACL not being reached by traffic |

---

## NAT

| Command | What It Does | Example / Notes |
|---|---|---|
| `ip nat inside` | Marks interface as inside (private) | Applied to LAN-facing interface |
| `ip nat outside` | Marks interface as outside (public) | Applied to WAN/ISP-facing interface |
| `ip nat pool <name> <start> <end> netmask <mask>` | Defines a NAT address pool | For dynamic NAT with a range of public IPs |
| `ip nat inside source list <acl> pool <name> overload` | Dynamic NAT with PAT | `overload` = PAT; remove for 1:1 NAT |
| `ip nat inside source static <private> <public>` | Static NAT entry | For servers that need a fixed public IP |
| `show ip nat translations` | Shows active NAT translation table | Use to verify hosts are being translated |
| `show ip nat statistics` | Shows hit/miss counts and pool usage | Check "misses" for troubleshooting |
| `clear ip nat translation *` | Clears all dynamic NAT entries | Use when testing or after config changes |

---

## DHCP

| Command | What It Does | Example / Notes |
|---|---|---|
| `ip dhcp excluded-address <start> <end>` | Reserves IPs from DHCP assignment | Always exclude gateway, DNS, servers |
| `ip dhcp pool <name>` | Creates a DHCP pool | Enter pool config submode |
| `network <ip> <mask>` | Defines scope for the pool | `network 192.168.10.0 255.255.255.0` |
| `default-router <ip>` | Sets default gateway sent to clients | `default-router 192.168.10.1` |
| `dns-server <ip>` | Sets DNS server sent to clients | |
| `show ip dhcp binding` | Lists current IP-to-MAC lease assignments | Empty = no clients received addresses |
| `show ip dhcp pool` | Shows pool utilization | |

---

## Troubleshooting — Top 10 Show Commands

| # | Command | Why You Run It |
|---|---|---|
| 1 | `show ip interface brief` | First check — interface IPs, up/down status at a glance |
| 2 | `show running-config` | See the full active config — pipe with `\| section <keyword>` |
| 3 | `show vlan brief` | Verify VLANs exist and ports are assigned correctly |
| 4 | `show interfaces trunk` | Check trunk mode, native VLAN, and allowed VLAN list |
| 5 | `show ip route` | Verify routing table — is the destination reachable? |
| 6 | `show ip ospf neighbor` | OSPF adjacency state — should be FULL |
| 7 | `show ip access-lists` | Check ACL hit counts — which rules are matching? |
| 8 | `show ip nat translations` | Verify hosts are being NATted |
| 9 | `show ip dhcp binding` | Confirm DHCP leases are being assigned |
| 10 | `show etherchannel summary` | Check port-channel bundle state (P=bundled, I=standalone) |

---

## Useful Filtering Techniques

```
! Filter show output to a section
show running-config | section ospf
show running-config | section interface

! Find a specific line
show running-config | include ip address
show running-config | include access-group

! Show from a keyword onward
show running-config | begin router ospf

! Exclude lines matching a pattern
show ip interface brief | exclude down
```

---

## Debug Commands (use carefully in production)

```
debug ip ospf hello          ! Show OSPF hello packet issues
debug ip dhcp server events  ! Show DHCP discover/offer/request/ack
debug ip nat                 ! Show NAT translation activity
undebug all                  ! ALWAYS run this when done debugging
```
