#!/usr/bin/env python3
"""Reject stale embedded datasets and fixture drift in SKILL.md files."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEYS = ("data_as_of", "valid_through", "source_version")
FAIL_BEFORE_DAYS = 30


def metadata(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}
    lines = match.group(1).splitlines()
    result: dict[str, str] = {}
    in_metadata = False
    for line in lines:
        if line == "metadata:":
            in_metadata = True
            continue
        if in_metadata and line and not line.startswith((" ", "\t")):
            break
        if in_metadata:
            item = re.match(r"^\s{2}([a-z_]+):\s*(.*?)\s*$", line)
            if item:
                result[item.group(1)] = item.group(2).strip('"\'')
    return result


def main() -> int:
    today = dt.date.fromisoformat(os.environ.get("STATIC_DATA_TODAY", dt.date.today().isoformat()))
    errors: list[str] = []
    checked = 0

    for path in sorted(ROOT.glob("*/SKILL.md")):
        meta = metadata(path)
        present = [key for key in KEYS if key in meta]
        if not present:
            continue
        checked += 1
        missing = [key for key in KEYS if key not in meta]
        if missing:
            errors.append(f"{path.relative_to(ROOT)}: partial static-data metadata; missing {', '.join(missing)}")
            continue
        try:
            data_as_of = dt.date.fromisoformat(meta["data_as_of"])
            valid_through = dt.date.fromisoformat(meta["valid_through"])
        except ValueError as exc:
            errors.append(f"{path.relative_to(ROOT)}: dates must use YYYY-MM-DD ({exc})")
            continue
        if data_as_of > today:
            errors.append(f"{path.relative_to(ROOT)}: data_as_of {data_as_of} is in the future")
        if valid_through < data_as_of:
            errors.append(f"{path.relative_to(ROOT)}: valid_through precedes data_as_of")
        days_left = (valid_through - today).days
        if days_left < 0:
            errors.append(f"{path.relative_to(ROOT)}: static data expired {abs(days_left)} day(s) ago on {valid_through}")
        elif days_left <= FAIL_BEFORE_DAYS:
            errors.append(f"{path.relative_to(ROOT)}: static data expires in {days_left} day(s) on {valid_through}; refresh now")
        else:
            print(f"OK    {path.relative_to(ROOT)}: valid through {valid_through} ({days_left} days left)")
        if not meta["source_version"].strip():
            errors.append(f"{path.relative_to(ROOT)}: source_version is empty")

    fixture_path = ROOT / "fixtures/static-data.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    for name, spec in fixture["datasets"].items():
        skill = ROOT / spec["skill"]
        text = skill.read_text(encoding="utf-8")
        for row in spec.get("required_rows", []):
            if row not in text:
                errors.append(f"{spec['skill']}: fixture '{name}' row changed or disappeared: {row}")
        for expected in spec.get("required_text", []):
            if expected not in text:
                errors.append(f"{spec['skill']}: fixture '{name}' marker changed or disappeared: {expected}")
        for url in spec.get("source_urls", []):
            if url not in text:
                errors.append(f"{spec['skill']}: official fixture source is not cited: {url}")
        if not spec.get("source_urls"):
            errors.append(f"fixture '{name}': source_urls must not be empty")
        print(f"OK    fixture {name}: {len(spec.get('required_rows', []))} core row(s)")

    if checked == 0:
        errors.append("no skills declare static-data metadata")
    if errors:
        for error in errors:
            print(f"FAIL  {error}", file=sys.stderr)
        return 1
    print(f"Static-data policy passed for {checked} skill(s); expiry window is {FAIL_BEFORE_DAYS} days.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
