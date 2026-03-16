#!/usr/bin/env python3
"""Create sample-level summary table from module outputs."""

from __future__ import annotations

import argparse
import csv
import json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize per-sample outputs")
    parser.add_argument("--sample", required=True)
    parser.add_argument("--fastp-json", required=True)
    parser.add_argument("--srna", required=True)
    parser.add_argument("--viral", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def read_fastp_total_reads(path: str) -> int:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return int(data["summary"]["before_filtering"]["total_reads"])
    except (OSError, KeyError, ValueError, json.JSONDecodeError, TypeError):
        return -1


def count_rows(path: str) -> int:
    with open(path, "r", encoding="utf-8") as handle:
        return max(sum(1 for _ in handle) - 1, 0)


def main() -> None:
    args = parse_args()

    total_reads = read_fastp_total_reads(args.fastp_json)
    srna_features = count_rows(args.srna)
    viral_taxa = count_rows(args.viral)

    with open(args.output, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["sample", "metric", "value"])
        writer.writerow([args.sample, "fastp_total_reads", total_reads])
        writer.writerow([args.sample, "srna_feature_rows", srna_features])
        writer.writerow([args.sample, "viral_taxa_rows", viral_taxa])


if __name__ == "__main__":
    main()
