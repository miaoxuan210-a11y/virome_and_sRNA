#!/usr/bin/env python3
import argparse
from pathlib import Path


def write_fasta(path, prefix):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as fh:
        for i in range(1, 6):
            fh.write(f">{prefix}_contig_{i}\n")
            fh.write("ATGCGT" * (10 + i) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Mock SPAdes/Trinity assembly")
    parser.add_argument("--reads", required=True)
    parser.add_argument("--spades-out", required=True)
    parser.add_argument("--trinity-out", required=True)
    parser.add_argument("--threads", type=int, default=1)
    args = parser.parse_args()

    write_fasta(args.spades_out, "spades")
    write_fasta(args.trinity_out, "trinity")


if __name__ == "__main__":
    main()
