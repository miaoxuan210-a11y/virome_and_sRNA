#!/usr/bin/env python3
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Mock miRNA prediction and quantification")
    parser.add_argument("--mirna-class", required=True)
    parser.add_argument("--predicted", required=True)
    parser.add_argument("--quant", required=True)
    args = parser.parse_args()

    pred = Path(args.predicted)
    quant = Path(args.quant)
    pred.parent.mkdir(parents=True, exist_ok=True)

    with pred.open("w", encoding="utf-8") as fh:
        fh.write("mirna_id\tstructure_score\tis_novel\n")
        for i in range(1, 11):
            fh.write(f"miR-{i}\t{0.9 - i * 0.03:.2f}\t{'yes' if i % 2 == 0 else 'no'}\n")

    with quant.open("w", encoding="utf-8") as fh:
        fh.write("mirna_id\trpm\n")
        for i in range(1, 11):
            fh.write(f"miR-{i}\t{1000 - i * 50}\n")


if __name__ == "__main__":
    main()
