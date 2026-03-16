#!/usr/bin/env python3
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Mock length/base distribution of small RNAs")
    parser.add_argument("--reads", required=True)
    parser.add_argument("--mapped", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        fh.write("length\tA\tC\tG\tT\n")
        for length in range(18, 31):
            fh.write(f"{length}\t{length*3}\t{length*2}\t{length*2+1}\t{length*4}\n")


if __name__ == "__main__":
    main()
