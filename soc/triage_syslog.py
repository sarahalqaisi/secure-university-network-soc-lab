#!/usr/bin/env python3
"""Deterministic offline triage for a small subset of Cisco IOS syslog events."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

EVENTS = (
    (re.compile(r"%SEC-6-IPACCESSLOGP: list (?P<acl>\S+) denied (?P<protocol>\w+) (?P<src>[\d.]+)\((?P<src_port>\d+)\) -> (?P<dst>[\d.]+)\((?P<dst_port>\d+)\)"), "acl_deny", "medium"),
    (re.compile(r"%SEC_LOGIN-4-LOGIN_FAILED: Login failed.*\[Source: (?P<src>[\d.]+)\]"), "login_failure", "high"),
    (re.compile(r"%SYS-5-CONFIG_I: Configured from (?P<source>.+)"), "configuration_change", "medium"),
    (re.compile(r"%LINK-3-UPDOWN: Interface (?P<interface>[^,]+), changed state to (?P<state>\w+)"), "link_state", "low"),
)


def triage(lines: list[str]) -> dict:
    events = []
    for number, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line:
            continue
        for pattern, category, severity in EVENTS:
            match = pattern.search(line)
            if match:
                events.append({"line": number, "category": category, "severity": severity, "fields": match.groupdict()})
                break
    counts = Counter(event["category"] for event in events)
    return {"source": "offline_syslog_export", "events": events, "summary": dict(sorted(counts.items())), "unmatched_lines": len([line for line in lines if line.strip()]) - len(events)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="exported Cisco IOS syslog text")
    parser.add_argument("--json", action="store_true", help="emit structured JSON")
    args = parser.parse_args()
    result = triage(args.input.read_text(encoding="utf-8", errors="replace").splitlines())
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for event in result["events"]:
            print(f"[{event['severity'].upper()}] line {event['line']} {event['category']}: {event['fields']}")
        print(f"Matched {len(result['events'])} event(s); unmatched {result['unmatched_lines']} line(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
