#!/usr/bin/env python3
"""Validate local Markdown links and balanced Mermaid code fences."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def validate() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        mermaid_openings = text.count("```mermaid")
        mermaid_blocks = len(re.findall(r"```mermaid\s+.*?```", text, flags=re.DOTALL))
        if mermaid_openings != mermaid_blocks:
            errors.append(f"{path.relative_to(ROOT)}: unbalanced Mermaid fence")
        for raw in re.findall(r"(?<!!)\[[^]]*\]\(([^)]+)\)", text):
            target = raw.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            if not (path.parent / target).resolve().exists():
                errors.append(f"{path.relative_to(ROOT)}: missing {target}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("\n".join(f"[FAIL] {error}" for error in errors))
        return 1
    print("[PASS] Markdown relative links and Mermaid fence structure")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
