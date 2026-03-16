#!/usr/bin/env python3
"""Run the full repository pipeline in mock mode without external bioinformatics binaries."""
from __future__ import annotations

import subprocess
from pathlib import Path

from config_utils import load_config


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> int:
    cfg = load_config("config/config.yaml")

    samples = list(cfg["samples"].keys())

    Path("results/qc").mkdir(parents=True, exist_ok=True)
    Path("results/reports").mkdir(parents=True, exist_ok=True)

    run(["python", "scripts/generate_mock_inputs.py"])

    for s in samples:
        raw = cfg["samples"][s]["raw_fastq"]
        clean = f"results/qc/{s}.clean.fastq.gz"
        host_removed = f"results/qc/{s}.host_removed.fastq.gz"

        run(["cp", raw, clean])
        Path(f"results/qc/{s}.fastp.html").write_text("<html>mock fastp</html>", encoding="utf-8")
        Path(f"results/qc/{s}.fastp.json").write_text('{"summary":"mock"}', encoding="utf-8")
        run(["cp", clean, host_removed])

        run(["python", "scripts/srna_classify.py", "--input", host_removed, "--sample", s, "--outdir", f"results/srna/{s}"])
        run([
            "python",
            "scripts/mirna_predict_quant.py",
            "--mirna-class",
            f"results/srna/{s}/class_miRNA.tsv",
            "--predicted",
            f"results/srna/{s}/predicted_mirna.tsv",
            "--quant",
            f"results/srna/{s}/mirna_quant.tsv",
        ])
        run([
            "python",
            "scripts/map_to_viral.py",
            "--reads",
            host_removed,
            "--viral-ref",
            cfg["references"]["viral_reference_fasta"],
            "--threads",
            str(cfg["threads"]["srna"]),
            "--output",
            f"results/srna/{s}/map_to_viral.tsv",
        ])
        run([
            "python",
            "scripts/length_base_distribution.py",
            "--reads",
            host_removed,
            "--mapped",
            f"results/srna/{s}/map_to_viral.tsv",
            "--output",
            f"results/srna/{s}/length_base_distribution.tsv",
        ])

        run([
            "python",
            "scripts/assemble_viral.py",
            "--reads",
            host_removed,
            "--spades-out",
            f"results/viral/{s}/spades_contigs.fasta",
            "--trinity-out",
            f"results/viral/{s}/trinity_contigs.fasta",
            "--threads",
            str(cfg["threads"]["viral"]),
        ])
        run([
            "python",
            "scripts/blast_annotation.py",
            "--contigs",
            f"results/viral/{s}/spades_contigs.fasta",
            "--db",
            cfg["references"]["blast_viral_db"],
            "--threads",
            str(cfg["threads"]["viral"]),
            "--output",
            f"results/viral/{s}/blast_annotation.tsv",
        ])
        run([
            "python",
            "scripts/interproscan_annotation.py",
            "--fasta",
            f"results/viral/{s}/trinity_contigs.fasta",
            "--threads",
            str(cfg["threads"]["viral"]),
            "--output",
            f"results/viral/{s}/interproscan.tsv",
        ])
        run([
            "python",
            "scripts/viral_abundance.py",
            "--blast",
            f"results/viral/{s}/blast_annotation.tsv",
            "--interpro",
            f"results/viral/{s}/interproscan.tsv",
            "--abundance",
            f"results/viral/{s}/abundance.tsv",
            "--classification-abundance",
            f"results/viral/{s}/classification_abundance.tsv",
        ])

    quant_files = [f"results/srna/{s}/mirna_quant.tsv" for s in samples]
    for s in samples:
        run([
            "python",
            "scripts/demirna_pipeline.py",
            "--sample",
            s,
            "--quant-files",
            *quant_files,
            "--group-table",
            cfg["design"]["group_table"],
            "--de",
            f"results/srna/{s}/de_mirna.tsv",
            "--targets",
            f"results/srna/{s}/mirna_targets.tsv",
            "--target-anno",
            f"results/srna/{s}/target_annotation.tsv",
            "--enrichment",
            f"results/srna/{s}/enrichment.tsv",
            "--correlation",
            f"results/srna/{s}/sample_correlation.tsv",
        ])

    run([
        "python",
        "scripts/build_summary.py",
        "--samples",
        ",".join(samples),
        "--de-files",
        *[f"results/srna/{s}/de_mirna.tsv" for s in samples],
        "--viral-files",
        *[f"results/viral/{s}/classification_abundance.tsv" for s in samples],
        "--out",
        "results/reports/workflow_summary.md",
    ])

    print("Mock pipeline run completed: results/reports/workflow_summary.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
