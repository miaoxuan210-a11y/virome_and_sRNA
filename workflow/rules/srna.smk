rule srna_analysis:
    input:
        "results/host_removed/{sample}.host_removed.fastq.gz"
    output:
        annotation="results/srna/{sample}.srna_annotation.tsv",
        length_dist="results/srna/{sample}.length_distribution.tsv"
    params:
        reference=config["srna_reference"]
    threads: config["threads"]["srna"]
    log:
        "logs/srna/{sample}.log"
    shell:
        r"""
        mkdir -p results/srna logs/srna
        python scripts/srna_analysis.py \
          --input {input} \
          --reference {params.reference} \
          --annotation {output.annotation} \
          --length-dist {output.length_dist} \
          > {log} 2>&1
        """
