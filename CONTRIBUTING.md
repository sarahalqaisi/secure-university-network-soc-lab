# Contributing

Keep Packet Tracer, evidence, static baseline, and documentation synchronized. Never invent CLI output or mark a manual check as verified without a corresponding repository artifact.

Before opening a pull request:

```bash
python scripts/validate_configs.py
python -m unittest discover -s tests -v
python -m compileall -q scripts soc tests
git diff --check
```

Describe whether a change affects the `.pkt` file, the evidence-derived baseline, documentation only, or the offline mini-SOC tool. Redact secrets and personal metadata. CI is static and cannot validate Packet Tracer runtime behavior.
