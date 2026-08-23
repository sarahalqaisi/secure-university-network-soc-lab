# Defensive incident scenarios

Statuses mean: **Verified** has repository evidence; **Manual pending** requires a new Packet Tracer run and screenshot.

## Scenario 1 — Student attempts Admin access (Verified)

- **Objective:** Confirm student-to-admin isolation.
- **Source:** Student-PC (`192.168.20.10`).
- **Destination:** Admin-PC (`192.168.10.10`).
- **Expected control:** `STUDENTS-IN` sequence 20, inbound on `GigabitEthernet0/0.20`.
- **Action:** `ping 192.168.10.10` from Student-PC.
- **Expected result:** Router gateway returns destination unreachable; ACL deny counter increases.
- **Actual evidence:** [`08-student-access-test.png`](../screenshots/08-student-access-test.png) shows failed pings; screenshots [05](../screenshots/05-acl-rules.png) and [06](../screenshots/06-students-acl-verification.png) show the rule, counter, and placement.
- **Interpretation:** The router blocks routed student access to the Admin subnet. This does not validate application-layer controls or traffic not covered by the ACL.

## Scenario 2 — Guest policy permits one server and blocks internal zones (Verified)

- **Objective:** Validate controlled guest access.
- **Source:** Guest-PC (`192.168.40.10`).
- **Destinations:** University Server (`192.168.50.10`), Admin-PC, Student-PC, IT-PC.
- **Expected control:** Host permit at `GUEST-IN` sequence 10 followed by internal subnet denies.
- **Action:** Ping each destination from Guest-PC.
- **Expected result:** Server replies; internal endpoint tests fail at gateway.
- **Actual evidence:** [`09-guest-access-test.png`](../screenshots/09-guest-access-test.png), plus ACL screenshots 05 and 07.
- **Interpretation:** The evidenced ICMP flows match ACL order. This does not prove isolation for every protocol or verify a true internet-only guest design.

## Scenario 3 — Unauthorized SSH management attempt (Manual pending)

- **Objective:** Confirm only a dedicated management source can reach device SSH.
- **Prerequisite:** Implement and verify SSH-only management plus a management-plane ACL; neither exists in current evidence.
- **Action:** Attempt SSH from Student-PC and the approved management endpoint.
- **Expected result:** Student denied and logged; management endpoint succeeds.
- **Evidence to capture:** VTY/SSH configuration with placeholders, management ACL and counters, failed/successful client attempts, centralized log event if supported.

## Scenario 4 — Denied flow enters mini-SOC triage (Manual pending)

- **Objective:** Trace a denied connection from ACL event to analyst classification.
- **Prerequisite:** Implement Packet Tracer syslog forwarding and selected ACL logging.
- **Action:** Repeat Scenario 1 using a logged protocol/port, export the resulting IOS message, then run `soc/triage_syslog.py`.
- **Expected result:** A provider-independent `acl_deny` event with medium triage priority.
- **Evidence to capture:** Original device log, collector view, parser JSON, ACL counter before/after, and analyst disposition.

Never substitute the synthetic fixture for runtime evidence.
