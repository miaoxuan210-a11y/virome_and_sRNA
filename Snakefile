configfile: "config/config.yaml"

SAMPLES = list(config["samples"].keys())

include: "workflow/rules/preprocess.smk"
include: "workflow/rules/srna.smk"
include: "workflow/rules/viral.smk"

rule all:
    input:
        expand("results/qc/{sample}.clean.fastq.gz", sample=SAMPLES),
        expand("results/srna/{sample}/de_mirna.tsv", sample=SAMPLES),
        expand("results/srna/{sample}/enrichment.tsv", sample=SAMPLES),
        expand("results/srna/{sample}/length_base_distribution.tsv", sample=SAMPLES),
        expand("results/viral/{sample}/classification_abundance.tsv", sample=SAMPLES),
        "results/reports/workflow_summary.md"

rule workflow_summary:
    input:
        de=expand("results/srna/{sample}/de_mirna.tsv", sample=SAMPLES),
        viral=expand("results/viral/{sample}/classification_abundance.tsv", sample=SAMPLES)
    output:
        "results/reports/workflow_summary.md"
    params:
        samples=",".join(SAMPLES)
    shell:
        """
        mkdir -p results/reports
        python scripts/build_summary.py \
            --samples {params.samples} \
            --de-files {input.de} \
            --viral-files {input.viral} \
            --out {output}
        """
