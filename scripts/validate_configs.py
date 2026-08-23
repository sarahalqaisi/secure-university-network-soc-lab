#!/usr/bin/env python3
"""Static validation for the screenshot-derived network intent baseline.

This does not open or execute Cisco Packet Tracer and cannot prove runtime state.
"""
from __future__ import annotations

import argparse
import ipaddress
import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASELINE = ROOT / "configs" / "evidence-baseline.json"


@dataclass(frozen=True)
class Check:
    level: str
    name: str
    detail: str


def validate(data: dict) -> list[Check]:
    checks: list[Check] = []
    vlans = data.get("vlans", [])
    ids = [item.get("id") for item in vlans]
    expected = {10, 20, 30, 40, 50}
    checks.append(Check("PASS" if set(ids) == expected else "FAIL", "expected VLAN IDs", f"observed {sorted(ids)}"))
    checks.append(Check("PASS" if len(ids) == len(set(ids)) else "FAIL", "unique VLAN IDs", "no duplicate IDs"))

    networks = []
    for item in vlans:
        try:
            network = ipaddress.ip_network(item["subnet"], strict=True)
            gateway = ipaddress.ip_address(item["gateway"])
            if gateway not in network:
                checks.append(Check("FAIL", f"VLAN {item['id']} gateway", "gateway is outside its subnet"))
            networks.append((item["id"], network))
        except (KeyError, ValueError) as exc:
            checks.append(Check("FAIL", f"VLAN {item.get('id', '?')} addressing", f"invalid network data: {type(exc).__name__}"))
    overlaps = [(a, b) for i, (a, left) in enumerate(networks) for b, right in networks[i + 1 :] if left.overlaps(right)]
    checks.append(Check("PASS" if not overlaps else "FAIL", "non-overlapping subnets", f"overlaps: {overlaps}" if overlaps else "five distinct /24 networks"))

    subinterfaces = data.get("router_subinterfaces", [])
    routed = {item.get("vlan") for item in subinterfaces if item.get("status") == "up/up"}
    checks.append(Check("PASS" if routed == expected else "FAIL", "router subinterfaces", f"up/up VLANs {sorted(routed)}"))

    trunk = data.get("trunk", {})
    active = set(trunk.get("active_vlans_observed", []))
    checks.append(Check("PASS" if expected <= active else "FAIL", "trunk carries required VLANs", f"active VLANs {sorted(active)}"))
    checks.append(Check("WARN" if trunk.get("native_vlan") == 1 else "PASS", "native VLAN hardening", f"observed native VLAN {trunk.get('native_vlan')}"))
    checks.append(Check("WARN" if trunk.get("allowed_vlans_observed") == "1-1005" else "PASS", "restricted trunk allow-list", f"observed {trunk.get('allowed_vlans_observed')}"))

    acls = data.get("acls", {})
    for name in ("STUDENTS-IN", "GUEST-IN"):
        rules = acls.get(name, [])
        sequences = [rule.get("sequence") for rule in rules]
        checks.append(Check("PASS" if sequences == sorted(set(sequences)) and rules else "FAIL", f"{name} ordering", f"sequences {sequences}"))
        broad = [rule for rule in rules if rule.get("action") == "permit" and rule.get("destination") == "any"]
        checks.append(Check("WARN" if broad else "PASS", f"{name} broad egress permit", "documented permit-to-any remains" if broad else "none"))
    placements = {item.get("inbound_acl") for item in subinterfaces if item.get("inbound_acl")}
    checks.append(Check("PASS" if {"STUDENTS-IN", "GUEST-IN"} <= placements else "FAIL", "inbound ACL placement", f"observed {sorted(placements)}"))

    checks.append(Check("WARN", "dedicated management VLAN", "not evidenced in the current Packet Tracer baseline"))
    checks.append(Check("WARN", "unused-port isolation", "unused ports are shown in VLAN 1; shutdown state is not evidenced"))
    checks.append(Check("WARN", "SSH-only management", "device management configuration is not evidenced"))
    checks.append(Check("WARN", "centralized syslog", "Packet Tracer forwarding is not evidenced; offline triage is repository-only"))
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", nargs="?", type=Path, default=DEFAULT_BASELINE)
    parser.add_argument("--strict-warnings", action="store_true", help="treat WARN results as a nonzero exit")
    args = parser.parse_args()
    data = json.loads(args.baseline.read_text(encoding="utf-8"))
    checks = validate(data)
    for check in checks:
        print(f"[{check.level}] {check.name}: {check.detail}")
    summary = {level: sum(check.level == level for check in checks) for level in ("PASS", "WARN", "FAIL")}
    print(f"Summary: {summary['PASS']} PASS, {summary['WARN']} WARN, {summary['FAIL']} FAIL")
    print("Scope: static evidence-baseline validation only; Packet Tracer runtime remains manual.")
    return 1 if summary["FAIL"] or (args.strict_warnings and summary["WARN"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
