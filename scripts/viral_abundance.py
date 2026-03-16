#!/usr/bin/env python3
import argparse
from pathlib import Path


def write(path, header, rows):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for row in rows:
            fh.write("\t".join(map(str, row)) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Mock viral abundance and classification")
    parser.add_argument("--blast", required=True)
    parser.add_argument("--interpro", required=True)
    parser.add_argument("--abundance", required=True)
    parser.add_argument("--classification-abundance", required=True)
    args = parser.parse_args()

    write(args.abundance, ["virus_id", "rpm"], [(f"virus_{i}", 500 - i * 40) for i in range(1, 6)])
    write(args.classification_abundance, ["taxonomy", "abundance"], [(f"Viruses;Family_{i}", 100 - i * 8) for i in range(1, 6)])


if __name__ == "__main__":
    main()
