#!/usr/bin/env python3
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Build markdown summary for pipeline outputs")
    parser.add_argument("--samples", required=True)
    parser.add_argument("--de-files", nargs="+", required=True)
    parser.add_argument("--viral-files", nargs="+", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    samples = args.samples.split(",")

    with out.open("w", encoding="utf-8") as fh:
        fh.write("# virome_and_sRNA workflow summary\n\n")
        fh.write("## Samples\n")
        for s in samples:
            fh.write(f"- {s}\n")
        fh.write("\n## Key Outputs\n")
        fh.write("- Differential miRNA tables generated for all samples.\n")
        fh.write("- Viral classification and abundance tables generated for all samples.\n")
        fh.write("\n## Files\n")
        for path in args.de_files + args.viral_files:
            fh.write(f"- {path}\n")


if __name__ == "__main__":
    main()
