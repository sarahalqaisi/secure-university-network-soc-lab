# Access-control matrix

This matrix describes the ACL behavior evidenced in [`05-acl-rules.png`](../screenshots/05-acl-rules.png), not an aspirational policy. Both ACLs are applied inbound on their matching router subinterfaces, as shown in screenshots 06 and 07.

| Source zone | Destination zone | Service | Action | Reason / evidence |
|---|---|---|---|---|
| Students (`192.168.20.0/24`) | University Server (`192.168.50.10`) | Any IP | Permit | `STUDENTS-IN` sequence 10; ping success is shown in screenshot 08. |
| Students | Admin (`192.168.10.0/24`) | Any IP | Deny | Sequence 20; ACL hits and failed ping are evidenced. |
| Students | IT (`192.168.30.0/24`) | Any IP | Deny | Sequence 30; ACL hits and failed ping are evidenced. |
| Students | Guest (`192.168.40.0/24`) | Any IP | Deny | Sequence 40; rule is evidenced, but no dedicated traffic screenshot was captured. |
| Students | Other Server VLAN hosts | Any IP | **Permit** | Sequence 50 permits remaining destinations. This is broader than “server only” and is a residual risk. |
| Students | Any other routed destination | Any IP | Permit | Sequence 50. No internet/edge network is present in the topology. |
| Guest (`192.168.40.0/24`) | University Server (`192.168.50.10`) | Any IP | Permit | `GUEST-IN` sequence 10; ping success is shown in screenshot 09. |
| Guest | Admin | Any IP | Deny | Sequence 20; ACL hits and failed ping are evidenced. |
| Guest | Students | Any IP | Deny | Sequence 30; ACL hits and failed ping are evidenced. |
| Guest | IT | Any IP | Deny | Sequence 40; ACL hits and failed ping are evidenced. |
| Guest | Other Server VLAN hosts | Any IP | Deny | Sequence 50, after the host-specific permit. |
| Guest | Any other routed destination | Any IP | Permit | Sequence 60. No internet/edge network is present in the topology. |
| Admin | Internal zones | Any IP | Permit by absence of evidenced inbound ACL | No least-privilege Admin ACL is shown. |
| IT | Internal zones | Any IP | Permit by absence of evidenced inbound ACL | No least-privilege IT/management ACL is shown. |

## Manual hardening target

Before changing the student policy, decide which services are actually required. A least-privilege revision should permit named protocols/ports to `192.168.50.10`, explicitly deny the remainder of VLAN 50 and other internal ranges, and log relevant denies. Do not apply a sample rule set blindly: Packet Tracer service availability and the intended application ports must be verified first.
