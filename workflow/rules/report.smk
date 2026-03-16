rule sample_summary:
    input:
        fastp_json="results/qc/{sample}.fastp.json",
        srna="results/srna/{sample}.srna_annotation.tsv",
        viral="results/viral/{sample}.viral_abundance.tsv"
    output:
        "results/report/{sample}.summary.tsv"
    threads: config["threads"]["report"]
    log:
        "logs/report/{sample}.log"
    shell:
        r"""
        mkdir -p results/report logs/report
        python scripts/summarize_results.py \
          --sample {wildcards.sample} \
          --fastp-json {input.fastp_json} \
          --srna {input.srna} \
          --viral {input.viral} \
          --output {output} \
          > {log} 2>&1
        """

rule project_summary:
    input:
        expand("results/report/{sample}.summary.tsv", sample=SAMPLES)
    output:
        "results/report/project_summary.tsv"
    run:
        import csv

        with open(output[0], "w", newline="") as out_handle:
            writer = csv.writer(out_handle, delimiter="\t")
            writer.writerow(["sample", "metric", "value"])
            for sample_file in input:
                with open(sample_file, "r", encoding="utf-8") as in_handle:
                    for line in in_handle:
                        if line.startswith("sample\t"):
                            continue
                        out_handle.write(line)
