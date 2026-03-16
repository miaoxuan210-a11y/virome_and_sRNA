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
    parser = argparse.ArgumentParser(description="Mock DEmiRNA and enrichment analysis")
    parser.add_argument("--sample", required=True)
    parser.add_argument("--quant-files", nargs="+", required=True)
    parser.add_argument("--group-table", required=True)
    parser.add_argument("--de", required=True)
    parser.add_argument("--targets", required=True)
    parser.add_argument("--target-anno", required=True)
    parser.add_argument("--enrichment", required=True)
    parser.add_argument("--correlation", required=True)
    args = parser.parse_args()

    write(args.de, ["mirna_id", "log2FC", "padj"], [(f"miR-{i}", round((i - 5) / 2, 2), 0.01 * i) for i in range(1, 8)])
    write(args.targets, ["mirna_id", "gene_id", "score"], [(f"miR-{i}", f"gene_{i}", round(0.95 - i * 0.05, 2)) for i in range(1, 8)])
    write(args.target_anno, ["gene_id", "annotation"], [(f"gene_{i}", f"function_{i}") for i in range(1, 8)])
    write(args.enrichment, ["pathway", "pvalue", "source"], [("Immune response", 0.004, "GO"), ("MAPK signaling", 0.011, "KEGG")])
    write(args.correlation, ["sample_a", "sample_b", "pearson_r"], [(args.sample, args.sample, 1.0)])


if __name__ == "__main__":
    main()
