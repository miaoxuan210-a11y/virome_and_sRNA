#!/usr/bin/env python3
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Mock BLAST annotation")
    parser.add_argument("--contigs", required=True)
    parser.add_argument("--db", required=True)
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        fh.write("contig_id\thit\tevalue\ttaxonomy\n")
        for i in range(1, 6):
            fh.write(f"spades_contig_{i}\tviral_hit_{i}\t1e-{30+i}\tViruses;Family_{i}\n")


if __name__ == "__main__":
    main()
