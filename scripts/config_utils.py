#!/usr/bin/env python3
"""Minimal YAML-like parser for this repository's config/config.yaml structure."""
from __future__ import annotations

from pathlib import Path


def load_config(path: str = "config/config.yaml") -> dict:
    """Parse the specific config format used in this repository.

    This avoids requiring external PyYAML in restricted environments.
    """
    data: dict = {
        "samples": {},
        "threads": {},
        "adapters": {},
        "references": {},
        "design": {},
    }
    section = None
    subsection = None

    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        if indent == 0 and stripped.endswith(":"):
            section = stripped[:-1]
            subsection = None
            continue

        if section == "samples":
            if indent == 2 and stripped.endswith(":"):
                subsection = stripped[:-1]
                data["samples"].setdefault(subsection, {})
                continue
            if indent == 4 and ":" in stripped and subsection:
                k, v = [x.strip() for x in stripped.split(":", 1)]
                data["samples"][subsection][k] = v
                continue

        if section in {"threads", "adapters", "references", "design"} and indent == 2 and ":" in stripped:
            k, v = [x.strip() for x in stripped.split(":", 1)]
            if section == "threads":
                data[section][k] = int(v)
            else:
                data[section][k] = v
            continue

        if section is None and ":" in stripped:
            k, v = [x.strip() for x in stripped.split(":", 1)]
            data[k] = v

    return data
