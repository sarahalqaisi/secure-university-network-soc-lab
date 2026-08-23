# Validation plan and evidence status

Automated checks validate repository intent only. Cisco Packet Tracer runtime checks must be performed manually in the `.pkt` file.

| Area | Command / action | Status | Current evidence or next step |
|---|---|---|---|
| VLAN membership | `show vlan brief` | Verified | Screenshot 02: VLANs 10–50 on Fa0/1–Fa0/5. |
| Trunk status | `show interfaces trunk` | Verified with warnings | Screenshot 03: Fa0/24 is up; native VLAN 1 and allow-list `1-1005` need hardening. |
| Inter-VLAN routing | `show ip interface brief` | Verified | Screenshot 04: five subinterfaces are up/up. |
| ACL definitions/hits | `show access-lists` | Verified | Screenshot 05; broad final permits remain. |
| ACL direction | `show ip interface g0/0.20` and `.40` | Verified | Screenshots 06–07 show inbound placement. |
| Student allowed/denied ICMP | Ping server, Admin, IT | Verified | Screenshot 08. Student-to-Guest and other Server hosts remain untested. |
| Guest allowed/denied ICMP | Ping server, Admin, Student, IT | Verified | Screenshot 09. |
| DHCP | Inspect pools/client leases | Not implemented/evidenced | Endpoints appear statically addressed; verify inside Packet Tracer. |
| DNS | Resolve an intended hostname | Not implemented/evidenced | No DNS service is visible. |
| SSH management | `show ip ssh`, `show run | section line vty` | Manual pending | Implement placeholders, source restriction, and capture results. |
| Management isolation | Attempt management from allowed/denied zones | Manual pending | No dedicated management VLAN is evidenced. |
| Unused ports | `show interfaces status`, `show run interface range ...` | Manual pending | Move to black-hole VLAN and shut down only confirmed-unused ports. |
| Port security / BPDU Guard / PortFast | `show port-security`, `show spanning-tree interface detail` | Manual pending | Apply only to confirmed endpoint ports. |
| Syslog | Generate selected logged deny and inspect collector | Manual pending | Offline parser exists; Packet Tracer collection is not evidenced. |
| Packet Tracer file | Open and save in supported Packet Tracer | Manual pending here | Packet Tracer is unavailable in the Codex environment. |

## Repository checks

```bash
python scripts/validate_configs.py
python -m unittest discover -s tests -v
python -m compileall -q scripts soc tests
python soc/triage_syslog.py soc/fixtures/synthetic-ios-syslog.log --json
git diff --check
```

Warnings from `validate_configs.py` are intentional visibility into hardening gaps. Use `--strict-warnings` when a future hardened export is expected to satisfy every control.
