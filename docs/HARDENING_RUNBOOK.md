# Manual Packet Tracer hardening runbook

**Status: proposed and not applied to the `.pkt` file.** Confirm feature support and save a backup before each section. Angle-bracket values are lab placeholders, not credentials or deployable configuration.

## 1. Capture the starting state

Run and export the commands in [CONFIG_EXPORT_GUIDE.md](CONFIG_EXPORT_GUIDE.md). Record current endpoint addresses and test all existing allowed/denied paths before changing policy.

## 2. Trunk and native VLAN

The evidence shows Fa0/24 permits `1-1005` with native VLAN 1. After confirming both ends support the intended settings:

```text
vlan <UNUSED_NATIVE_VLAN_ID>
 name NATIVE-UNUSED
interface FastEthernet0/24
 switchport mode trunk
 switchport trunk native vlan <UNUSED_NATIVE_VLAN_ID>
 switchport trunk allowed vlan 10,20,30,40,50,<MGMT_VLAN_ID>,<UNUSED_NATIVE_VLAN_ID>
 switchport nonegotiate
```

Configure matching 802.1Q native/management handling on Router1. A mismatch can break connectivity, so validate immediately with `show interfaces trunk` and gateway pings.

## 3. Confirm and isolate unused switch ports

The topology uses Fa0/1–Fa0/5 and Fa0/24, but do not assume every other port is unused without `show interfaces status` and physical inspection.

```text
vlan <BLACKHOLE_VLAN_ID>
 name UNUSED-PORTS
interface range <CONFIRMED_UNUSED_PORTS>
 switchport mode access
 switchport access vlan <BLACKHOLE_VLAN_ID>
 shutdown
 description UNUSED-SHUTDOWN
```

## 4. Harden confirmed endpoint ports

Apply only to legitimate single-endpoint access ports; sticky MAC learning can cause support issues when devices move.

```text
interface range FastEthernet0/1-5
 switchport mode access
 switchport nonegotiate
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security
 switchport port-security maximum 1
 switchport port-security violation restrict
```

Use sticky MAC only if the lab intentionally tests that behavior and captures recovery steps.

## 5. Dedicated management plane and SSH

Design a non-overlapping management subnet first. Do not reuse Admin or IT implicitly. Configure local credentials interactively or through non-reusable placeholders; never commit the resulting hashes/keys.

```text
hostname <DEVICE_NAME>
ip domain-name lab.example
enable secret <LAB_ONLY_ENABLE_SECRET>
username <LAB_ADMIN> privilege 15 secret <LAB_ONLY_PASSWORD>
service password-encryption
banner motd ^CAuthorized lab access only.^C
crypto key generate rsa modulus 2048
ip ssh version 2
ip access-list standard MGMT-SOURCES
 permit <MGMT_SUBNET> <WILDCARD>
 deny any log
line vty 0 4
 login local
 transport input ssh
 access-class MGMT-SOURCES in
 exec-timeout 10 0
```

Packet Tracer image support may vary. Verify `show ip ssh`, attempt allowed/denied connections, and capture sanitized output.

## 6. Tighten routed policy

Inventory required server protocols first. Replace broad `permit ip ... host 192.168.50.10` rules with named service permits only when the server actually provides those services. For Students, explicitly deny the remainder of `192.168.50.0/24` before the final egress rule. Decide what “egress” means because this topology has no internet edge.

Admin and IT flows also require a documented least-privilege decision before applying new inbound ACLs. Preserve emergency management access during testing.

## 7. Logging and mini SOC integration

If supported, configure timestamps, buffered logging, and a dedicated syslog endpoint. Add `log` only to selected denies and failed management paths. Validate the collector with a known test, then export sanitized messages for `soc/triage_syslog.py`.

## 8. Acceptance gate

Re-run every row in [VALIDATION.md](VALIDATION.md), update the evidence baseline from new CLI output, replace stale screenshots rather than duplicating them, and document any deviation. A passing static script does not replace this Packet Tracer acceptance gate.
