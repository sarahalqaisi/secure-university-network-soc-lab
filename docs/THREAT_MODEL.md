# Threat model

Scope: one router, one Layer 2 switch, four user endpoints, one server, and an offline mini-SOC parser in a simulated lab. No internet edge, wireless, high availability, NAC, production identity, or real SIEM is present.

| Threat | Asset | Existing control | Residual risk | Validation |
|---|---|---|---|---|
| Student reaches Admin network | Admin-PC / VLAN 10 | Inbound `STUDENTS-IN` deny | Only evidenced for ICMP; ACL permits other destinations broadly | Screenshot 08 and ACL counter |
| Student reaches unintended server host | Server VLAN | Host permit followed by final permit-any | Other VLAN 50 hosts are not denied | Manual negative test required; revise ACL intentionally |
| Guest lateral movement | Internal endpoints | Ordered `GUEST-IN` internal denies | Final permit-any assumes a future outside path that does not exist | Screenshot 09; test any added routed zones |
| Compromised Admin or IT endpoint | All internal zones | VLAN separation only | No inbound least-privilege ACL evidenced for Admin/IT | Design flows and test manually |
| VLAN hopping / trunk misuse | All VLANs | Static trunk mode is evidenced | Native VLAN 1 and allow-list `1-1005`; DTP status not evidenced | Harden trunk, then `show interfaces trunk` |
| Rogue endpoint on unused port | Campus segments | None evidenced | Unused ports remain in VLAN 1; shutdown/port security absent from evidence | Inspect and harden confirmed-unused ports |
| Insecure device administration | Router/switch configuration | None evidenced | Telnet/weak VTY exposure cannot be ruled out | Verify SSH, VTY ACL, secrets, banner |
| Exposed server services | University Server | Network location in VLAN 50; guest host-specific permit | Student policy is broad; service ports are not constrained | Inventory enabled services and use port-specific ACLs |
| Insufficient logging | Incident evidence | ACL counters and offline parser | No centralized Packet Tracer collection or time synchronization evidenced | Complete SOC integration scenario |
| Misleading automated assurance | Portfolio claims | Static validator prints explicit scope | JSON intent can drift from `.pkt` runtime | Re-export CLI evidence after every topology change |

Controls reduce specific routed risks; they do not establish zero trust, compliance, production readiness, or guaranteed detection.
