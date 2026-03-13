# Lab 02 – OSPF Single Area

![Network Topology](../../screenshots/11-ospfv2-single-area.png)

## Objective
Configure OSPFv2 in a single area (Area 0) across three routers. Verify OSPF neighbor adjacency and routing table entries.

## Topology
- R1 (RID 1.1.1.1) ↔ R2 (RID 2.2.2.2) ↔ R3 (RID 3.3.3.3)
- R1 LAN: 192.168.1.0/24
- R3 LAN: 192.168.3.0/24
- R1–R2 WAN: 10.53.0.0/30
- R2–R3 WAN: 10.54.0.0/30

## Key Commands
```
router ospf 56
 router-id 1.1.1.1
 network 192.168.1.0 0.0.0.255 area 0
 network 10.53.0.0 0.0.0.3 area 0
 passive-interface GigabitEthernet0/0/0
```

## Verification
- `show ip ospf neighbor` — confirm FULL adjacency
- `show ip route ospf` — confirm O routes present
- `show ip ospf interface brief` — check costs
- Ping PC-A → PC-C across OSPF domain

## Learning Outcomes
- Configure OSPFv2 process and router-ID
- Advertise networks into OSPF area 0
- Verify DR/BDR election
- Use passive-interface for LAN segments
