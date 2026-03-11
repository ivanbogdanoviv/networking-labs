# Contributing — How to Add a Lab

This guide explains the conventions for adding a new lab to this repo so everything stays consistent and easy to navigate.

---

## Lab Folder Naming

Labs live under `labs/` and follow this naming pattern:

```
labs/<number>-<short-slug>/
```

Examples:
- `labs/04-stp-basics/`
- `labs/05-dhcp-server/`
- `labs/06-nat-overload/`

Use two-digit numbers so they sort correctly. Keep the slug lowercase with hyphens.

---

## Required Files per Lab

Every lab folder must contain at minimum:

```
labs/<number>-<slug>/
├── README.md           # Lab objectives, topology description, commands, notes
└── config-<device>.txt # One file per device (e.g. config-r1.txt, config-sw1.txt)
```

Optional but encouraged:
```
├── topology.png        # Screenshot or export from Packet Tracer / GNS3 / draw.io
└── verification.txt    # Output of show commands confirming the lab worked
```

---

## README.md Template for a Lab

Copy this into your new lab's `README.md`:

```markdown
# Lab XX — <Title>

## Objective
One or two sentences on what this lab demonstrates.

## Topology
_(Add topology.png or describe the device connections here)_

## Devices
| Device | Role |
|--------|------|
| R1 | ... |
| SW1 | ... |

## Key Configs
- `config-r1.txt` — ...

## Verification
Commands used to confirm the lab is working:
- `show ...`
- `ping ...`

## Notes
Anything worth remembering about this topic.
```

---

## Config File Conventions

- Use `show running-config` output (copy-paste from Packet Tracer terminal or GNS3).
- Add a comment header at the top with the device hostname and a brief description.
- Strip passwords before committing (replace with `<password>` placeholder).

---

## Topology Files

- `.pkt` and `.gns3` files are listed in `.gitignore` and **not committed** — they can be large and binary.
- Instead, export a `topology.png` and commit that alongside the text configs.

---

## Scripts

If your lab includes an automation script (e.g. a netmiko backup or a ping sweep), place it in `scripts/` at the repo root, not inside the lab folder.

---

## Commit Message Style

```
lab: add 04-stp-basics configs and topology
fix: correct OSPF network statement in lab-02
docs: add verification steps to lab-01 README
```

---

## Checklist Before Committing

- [ ] Lab folder follows the `NN-slug` naming convention
- [ ] `README.md` present with objective, devices, and key configs listed
- [ ] At least one `config-*.txt` file present
- [ ] No plaintext passwords in config files
- [ ] Topology image added or noted as "planned"
