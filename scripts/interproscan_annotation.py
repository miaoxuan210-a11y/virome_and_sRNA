#!/usr/bin/env python3
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Mock InterProScan annotation")
    parser.add_argument("--fasta", required=True)
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        fh.write("contig_id\tdomain\tdescription\n")
        for i in range(1, 6):
            fh.write(f"trinity_contig_{i}\tIPR00{i:03d}\tMock domain {i}\n")


if __name__ == "__main__":
    main()
