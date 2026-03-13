# Cisco IOS Quick Reference

Field-ready cheat sheet for CCNA lab work. Covers the 20 most-used IOS commands, the most common student mistakes, and a subnetting reference table.

---

## Most Used IOS Commands

### Basic Setup

| Command | Syntax | What It Does |
|---|---|---|
| Set hostname | `hostname <name>` | Names the device — appears in the prompt and CDP |
| Set encrypted enable password | `enable secret <password>` | Sets privileged EXEC password using MD5 hash (preferred over `enable password`) |
| Disable DNS lookup | `no ip domain-lookup` | Stops IOS from trying to resolve mistyped commands as hostnames — eliminates 30-second hangs |
| Set login banner | `banner motd # <text> #` | Displays a warning message before login — required in most security policies |
| Save configuration | `copy running-config startup-config` | Writes active config to NVRAM; survives reboot. Short form: `wr` |
| Show active config | `show running-config` | Displays the full current configuration. Pipe with `| section <keyword>` to filter |

### VLANs

| Command | Syntax | What It Does |
|---|---|---|
| Create a VLAN | `vlan <id>` then `name <name>` | Adds VLAN to the VLAN database and assigns a human-readable name |
| Assign port to VLAN | `switchport access vlan <id>` | Places an access port into the specified VLAN (run under the interface) |
| Configure trunk port | `switchport mode trunk` | Forces the port to carry traffic for multiple VLANs using 802.1Q tagging |
| Set allowed VLANs on trunk | `switchport trunk allowed vlan <list>` | Restricts which VLANs are forwarded across the trunk link |
| Set native VLAN | `switchport trunk native vlan <id>` | Defines the VLAN for untagged frames — must match on both ends of the trunk |
| Verify trunk status | `show interfaces trunk` | Shows trunk mode, encapsulation, native VLAN, and allowed/active VLAN lists |

### Routing

| Command | Syntax | What It Does |
|---|---|---|
| Add static route | `ip route <network> <mask> <next-hop>` | Manually defines a path to a remote network. Use `0.0.0.0 0.0.0.0` for a default route |
| Create subinterface (ROAS) | `interface gi0/0.10` then `encapsulation dot1Q 10` | Creates a logical subinterface for Router-on-a-Stick inter-VLAN routing |
| Enable OSPF | `router ospf <pid>` then `network <ip> <wildcard> area <n>` | Starts OSPF process and enables it on matching interfaces |
| Set OSPF router ID | `router-id <A.B.C.D>` | Manually assigns a stable router ID — best practice is to match a loopback IP |
| Show routing table | `show ip route` | Displays all known routes with codes: C=connected, S=static, O=OSPF |

### ACLs

| Command | Syntax | What It Does |
|---|---|---|
| Create named extended ACL | `ip access-list extended <name>` | Enters ACL config mode for a named ACL — preferred over numbered for readability |
| Add a deny/permit rule | `deny tcp <src> <wildcard> any eq 23` | Adds an entry to the ACL — rules are matched top-down, first match wins |
| Apply ACL to interface | `ip access-group <name> in` | Activates the ACL on an interface. `in` = inbound traffic, `out` = outbound |

### Troubleshooting

| Command | Syntax | What It Does |
|---|---|---|
| Check interface status | `show ip interface brief` | One-line summary of all interfaces: IP, status (up/down), protocol — the first command to run |
| Check OSPF neighbors | `show ip ospf neighbor` | Lists OSPF adjacencies and their state — should show `FULL` for healthy neighbors |
| Check ACL hit counts | `show ip access-lists` | Shows each ACL entry with match counters — zero hits means traffic isn't reaching the ACL |
| Check DHCP bindings | `show ip dhcp binding` | Lists active IP-to-MAC lease assignments — empty means clients aren't receiving addresses |

---

## Common Mistakes

### 1. Native VLAN mismatch on trunk links

**Mistake:** Configuring native VLAN 1 on one switch and native VLAN 99 on the other end of the trunk.

**Symptom:** CDP warning: *"Native VLAN mismatch discovered on..."* — untagged traffic ends up in the wrong VLAN.

**Fix:** Set the same native VLAN on both ends.
```
SW1(config-if)# switchport trunk native vlan 99
SW2(config-if)# switchport trunk native vlan 99
```

---

### 2. Applying an extended ACL in the wrong direction

**Mistake:** Applying an ACL outbound (`out`) on the WAN interface when it should be inbound (`in`) on the LAN interface.

**Symptom:** Either the ACL blocks too much traffic or has zero hit counts because traffic never reaches it.

**Fix:** Extended ACLs should be placed **closest to the source** — inbound on the interface where the traffic originates. Always verify with:
```
show ip interface <interface> | include access list
```

---

### 3. Forgetting `ip helper-address` for DHCP across routers

**Mistake:** Configuring a DHCP pool on a router but not adding `ip helper-address` on the router interface facing the clients.

**Symptom:** Hosts get APIPA (169.254.x.x) addresses. `show ip dhcp binding` is empty.

**Fix:** Add the helper address on the interface connected to the client subnet, pointing to the DHCP server:
```
R1(config-if)# ip helper-address 192.168.10.1
```

---

### 4. OSPF neighbors not forming due to timer mismatch

**Mistake:** Manually changing the dead-interval on one router but not the other, causing hellos to be rejected.

**Symptom:** `show ip ospf neighbor` shows no entries or stuck in `INIT` state.

**Fix:** Ensure Hello and Dead intervals match on both ends of every OSPF link. Verify with:
```
show ip ospf interface <interface>
```
Then align the timers:
```
R1(config-if)# ip ospf dead-interval 40
```

---

### 5. EtherChannel not bundling due to mixed negotiation modes

**Mistake:** Configuring one switch with `channel-group 1 mode active` (LACP) and the other with `channel-group 1 mode on` (static). Static mode does not send or respond to LACP PDUs.

**Symptom:** `show etherchannel summary` shows ports as `(I)` — stand-alone, not bundled.

**Fix:** Both ends must use compatible modes. Either both use LACP (`active`/`passive`) or both use static (`on`):
```
SW1(config-if-range)# channel-group 1 mode active
SW2(config-if-range)# channel-group 1 mode passive
```

---

## Subnetting Cheat Sheet

Subnets derived from a single **192.168.1.0/24** parent block.

| CIDR | Subnet Mask | Wildcard Mask | Subnets from /24 | Hosts per Subnet | Usable Host Range Example |
|---|---|---|---|---|---|
| /24 | 255.255.255.0 | 0.0.0.255 | 1 | 254 | .1 – .254 |
| /25 | 255.255.255.128 | 0.0.0.127 | 2 | 126 | .1 – .126 / .129 – .254 |
| /26 | 255.255.255.192 | 0.0.0.63 | 4 | 62 | .1 – .62 / .65 – .126 / ... |
| /27 | 255.255.255.224 | 0.0.0.31 | 8 | 30 | .1 – .30 / .33 – .62 / ... |
| /28 | 255.255.255.240 | 0.0.0.15 | 16 | 14 | .1 – .14 / .17 – .30 / ... |

**Quick memory rule:** Each time you add one bit to the prefix, you double the number of subnets and halve the hosts per subnet.

| Prefix | Block size | First subnet increment |
|---|---|---|
| /24 | 256 | 256 |
| /25 | 128 | 128 |
| /26 | 64 | 64 |
| /27 | 32 | 32 |
| /28 | 16 | 16 |

**Formula:**
- **Subnets from a /24:** `2^(new_prefix - 24)`
- **Hosts per subnet:** `2^(32 - prefix) - 2`
- **Network address:** first IP in the block (all host bits = 0)
- **Broadcast:** last IP in the block (all host bits = 1)
- **Usable range:** network + 1 through broadcast - 1
