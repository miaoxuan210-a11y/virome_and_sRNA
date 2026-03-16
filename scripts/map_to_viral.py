#!/usr/bin/env python3
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Mock mapping small RNA to viral reference")
    parser.add_argument("--reads", required=True)
    parser.add_argument("--viral-ref", required=True)
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        fh.write("read_id\tvirus_id\talignment_score\n")
        for i in range(1, 21):
            fh.write(f"read_{i}\tvirus_{(i % 5) + 1}\t{80 + i}\n")


if __name__ == "__main__":
    main()
