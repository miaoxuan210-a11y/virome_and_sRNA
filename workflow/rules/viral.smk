rule viral_analysis:
    input:
        "results/host_removed/{sample}.host_removed.fastq.gz"
    output:
        contigs="results/viral/{sample}.contigs.fa",
        annotation="results/viral/{sample}.viral_annotation.tsv",
        abundance="results/viral/{sample}.viral_abundance.tsv"
    params:
        reference=config["viral_reference_fasta"]
    threads: config["threads"]["viral"]
    log:
        "logs/viral/{sample}.log"
    shell:
        r"""
        mkdir -p results/viral logs/viral
        python scripts/viral_analysis.py \
          --input {input} \
          --reference {params.reference} \
          --contigs {output.contigs} \
          --annotation {output.annotation} \
          --abundance {output.abundance} \
          > {log} 2>&1
        """
