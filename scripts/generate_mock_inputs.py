#!/usr/bin/env python3
"""Generate tiny synthetic FASTQ.gz inputs for configured samples."""
from __future__ import annotations

import argparse
import gzip
from pathlib import Path

from config_utils import load_config


def write_fastq(path: Path, seq: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt", encoding="utf-8") as fh:
        fh.write("@read_1\n")
        fh.write(seq + "\n")
        fh.write("+\n")
        fh.write("F" * len(seq) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate mock FASTQ.gz files from config samples")
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()

    cfg = load_config(args.config)

    samples = cfg.get("samples", {})
    if not samples:
        raise SystemExit("No samples found in config.")

    base_seq = "ACGTACGTACGTACGTACGT"
    for i, (sample, info) in enumerate(samples.items(), start=1):
        raw = Path(info["raw_fastq"])
        seq = (base_seq[i % 4 :] + base_seq[: i % 4])[:20]
        write_fastq(raw, seq)
        print(f"Generated: {raw}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
