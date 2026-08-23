# Evidence index

| File | Context | What it proves | What it does not prove |
|---|---|---|---|
| `01-topology.png` | Packet Tracer logical view | Devices and physical/logical links visible in the lab | Interface configs or security policy |
| `02-vlan-configuration.png` | `show vlan brief` | VLAN IDs/names and Fa0/1–Fa0/5 membership | Shutdown state, port security, or management VLAN |
| `03-trunk-verification.png` | `show interfaces trunk` | Fa0/24 trunk is forwarding active VLANs | Hardened native VLAN or restricted allow-list; evidence shows the opposite |
| `04-router-subinterfaces.png` | `show ip interface brief` | Gateways `.10`–`.50` are up/up | Encapsulation details, DHCP, DNS, or routing beyond connected VLANs |
| `05-acl-rules.png` | `show access-lists` | ACL order, rules, and some hit counters | Complete protocol coverage or current counters after later changes |
| `06-students-acl-verification.png` | `show ip interface g0/0.20` | `STUDENTS-IN` is inbound | All student policy outcomes |
| `07-guest-acl-verification.png` | `show ip interface g0/0.40` | `GUEST-IN` is inbound | All guest policy outcomes |
| `08-student-access-test.png` | Student-PC pings | Server allowed; Admin and IT blocked for captured ICMP | Student-to-Guest, other servers, TCP/UDP, or later state |
| `09-guest-access-test.png` | Guest-PC pings | Server allowed; Admin/Student/IT blocked for captured ICMP | TCP/UDP behavior or internet isolation |

The `.docx` report embeds these same screenshots and is a historical test narrative, not a separate runtime source.
