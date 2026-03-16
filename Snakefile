configfile: "config/config.yaml"

SAMPLES = config["samples"]

include: "workflow/rules/qc.smk"
include: "workflow/rules/host_removal.smk"
include: "workflow/rules/srna.smk"
include: "workflow/rules/viral.smk"
include: "workflow/rules/report.smk"

rule all:
    input:
        expand("results/report/{sample}.summary.tsv", sample=SAMPLES),
        "results/report/project_summary.tsv"
