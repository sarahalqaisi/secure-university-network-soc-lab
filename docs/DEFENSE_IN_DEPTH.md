# Defense-in-depth evidence map

| Control | Layer | Threat addressed | Evidence / status |
|---|---|---|---|
| VLANs 10/20/30/40/50 | Layer 2 segmentation | Unnecessary broadcast-domain sharing | Screenshot 02 — verified |
| Router-on-a-stick subinterfaces | Layer 3 boundary | Centralizes routed policy enforcement | Screenshot 04 — verified |
| Student and Guest ACLs | Layer 3 access control | Unauthorized cross-zone routing | Screenshots 05–09 — verified for documented ICMP tests |
| Restricted trunk VLAN list | Layer 2 hardening | Excess VLAN propagation | Not implemented: observed `1-1005` |
| Non-default native VLAN | Layer 2 hardening | Native-VLAN misuse assumptions | Not implemented: observed VLAN 1 |
| Unused-port shutdown / black-hole VLAN | Access layer | Rogue physical attachment | Not evidenced; manual pending |
| Port security / BPDU Guard / PortFast | Access layer | Rogue MACs / edge STP events | Not evidenced; manual pending |
| SSH-only management and source ACL | Management plane | Credential interception / unauthorized administration | Not evidenced; manual pending |
| Central syslog and ACL logging | Monitoring | Missed deny/auth/config/link events | Offline parser implemented; Packet Tracer forwarding pending |
| Incident scenarios and evidence index | Process | Unrepeatable validation | Two scenarios verified; two pending |

These mappings are educational and do not assert NIST, CIS, or other certification/compliance.
