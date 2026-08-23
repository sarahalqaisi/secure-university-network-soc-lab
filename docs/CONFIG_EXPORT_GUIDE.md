# Packet Tracer configuration export guide

The repository has no authoritative full running-config export. [`configs/evidence-baseline.json`](../configs/evidence-baseline.json) is a narrow transcription of visible screenshots and must not be pasted into a device as configuration.

After every Packet Tracer change, capture text from each applicable device:

```text
show running-config
show vlan brief
show interfaces trunk
show interfaces status
show ip interface brief
show ip route
show access-lists
show ip ssh
show port-security
show spanning-tree interface detail
show logging
```

Save full, redacted exports as `configs/routers/<device>-running-config.txt` and `configs/switches/<device>-running-config.txt`. Remove lab passwords, enable secrets, key material, SNMP communities, and personally identifying banners before committing. Replace sensitive values with explicit placeholders such as `<LAB_ENABLE_SECRET>`; do not use reusable personal credentials.

Reconcile the JSON baseline and documentation only after comparing the export to Packet Tracer runtime output.
