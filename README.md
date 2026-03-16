# Virome + sRNA Snakemake Workflow

This repository contains a modular Snakemake workflow scaffold for **raw FASTQ-based virome and small RNA analysis**.

## Workflow overview

1. **Input**: raw single-end FASTQ files in `data/raw/`
2. **QC**: `fastp`
3. **Host removal**: `bowtie2`
4. **Branch A (sRNA module)**: placeholder classification + length distribution output
5. **Branch B (viral module)**: placeholder contig/annotation/abundance output
6. **Summary/report**: per-sample and project-level TSV summary

> The current scripts for sRNA/viral/report are lightweight placeholders so the pipeline structure is complete and can be dry-run immediately. Replace them with your production analysis logic later.

## Directory structure

```text
.
├── Snakefile
├── config/
│   └── config.yaml
├── workflow/
│   └── rules/
│       ├── qc.smk
│       ├── host_removal.smk
│       ├── srna.smk
│       ├── viral.smk
│       └── report.smk
├── scripts/
│   ├── check_dependencies.py
│   ├── srna_analysis.py
│   ├── viral_analysis.py
│   └── summarize_results.py
├── data/raw/
│   └── sample1.fastq
├── refs/
│   ├── host/bowtie2_index/
│   ├── srna/
│   └── viral/
└── results/
```

## Configuration

Edit `config/config.yaml`:

- `samples`: sample IDs without extension
- `raw_dir`: raw FASTQ folder
- `host_index_prefix`: Bowtie2 index prefix
- `viral_reference_fasta`, `srna_reference`: reference paths
- `threads`: thread allocation per module

## Environment setup

At minimum, install:

- `snakemake`
- `fastp`
- `bowtie2`
- Python 3

Check dependencies:

```bash
python scripts/check_dependencies.py
```

## Input requirements

- FASTQ naming convention: `{sample}.fastq`
- Example: `data/raw/sample1.fastq` corresponds to sample `sample1`

## Run

Dry-run:

```bash
snakemake -n
```

Actual run (local cores):

```bash
snakemake --cores 4
```

## Output highlights

- `results/qc/`: cleaned reads + fastp reports
- `results/host_removed/`: host-removed reads and alignment SAM
- `results/srna/`: sRNA module outputs
- `results/viral/`: viral module outputs
- `results/report/`: sample summary + project summary

## Known external prerequisites for real execution

Even though dry-run works, a full run additionally requires:

1. Valid Bowtie2 index files for `host_index_prefix`
2. Real reference files under `refs/viral/` and `refs/srna/`
3. Installed tools in PATH (`fastp`, `bowtie2`)
4. Real sample FASTQ data (replace demo sample as needed)
