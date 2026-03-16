rule remove_host:
    input:
        "results/qc/{sample}.clean.fastq.gz"
    output:
        host_removed="results/host_removed/{sample}.host_removed.fastq.gz",
        sam="results/host_removed/{sample}.host_mapped.sam"
    params:
        host_index=config["host_index_prefix"]
    threads: config["threads"]["bowtie2"]
    log:
        "logs/bowtie2/{sample}.log"
    shell:
        r"""
        mkdir -p results/host_removed logs/bowtie2
        bowtie2 \
          -x {params.host_index} \
          -U {input} \
          --very-sensitive \
          --threads {threads} \
          --un-gz {output.host_removed} \
          -S {output.sam} \
          > {log} 2>&1
        """
