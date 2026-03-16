#!/usr/bin/env python3
import argparse
from pathlib import Path


def write_table(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        fh.write("feature_id\tcount\n")
        for feature_id, count in rows:
            fh.write(f"{feature_id}\t{count}\n")


def main():
    parser = argparse.ArgumentParser(description="Mock sRNA classification")
    parser.add_argument("--input", required=True)
    parser.add_argument("--sample", required=True)
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    outdir = Path(args.outdir)
    categories = ["rRNA", "tRNA", "miRNA", "snRNA", "snoRNA"]
    for idx, cat in enumerate(categories, start=1):
        rows = [(f"{args.sample}_{cat}_{i}", 100 - i * idx) for i in range(1, 6)]
        write_table(outdir / f"class_{cat}.tsv", rows)


if __name__ == "__main__":
    main()
