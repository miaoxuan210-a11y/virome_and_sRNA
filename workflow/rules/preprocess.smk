rule trim_and_qc:
    input:
        lambda wc: config["samples"][wc.sample]["raw_fastq"]
    output:
        "results/qc/{sample}.clean.fastq.gz",
        "results/qc/{sample}.fastp.html",
        "results/qc/{sample}.fastp.json"
    threads: config["threads"]["preprocess"]
    params:
        adapter=config["adapters"]["srna_adapter"]
    log:
        "logs/preprocess/{sample}.log"
    shell:
        """
        mkdir -p results/qc logs/preprocess
        fastp \
            -i {input} \
            -o {output[0]} \
            --adapter_sequence {params.adapter} \
            --html {output[1]} \
            --json {output[2]} \
            --thread {threads} \
            > {log} 2>&1
        """

rule remove_host_reads:
    input:
        "results/qc/{sample}.clean.fastq.gz"
    output:
        "results/qc/{sample}.host_removed.fastq.gz"
    threads: config["threads"]["preprocess"]
    params:
        host_index=config["references"]["host_bowtie_index"]
    log:
        "logs/preprocess/{sample}.host_removal.log"
    shell:
        """
        mkdir -p logs/preprocess
        bowtie2 \
            -x {params.host_index} \
            -U {input} \
            --threads {threads} \
            --un-gz {output} \
            -S /dev/null \
            > {log} 2>&1
        """
