rule viral_assembly:
    input:
        "results/qc/{sample}.host_removed.fastq.gz"
    output:
        spades="results/viral/{sample}/spades_contigs.fasta",
        trinity="results/viral/{sample}/trinity_contigs.fasta"
    threads: config["threads"]["viral"]
    log:
        "logs/viral/{sample}.assembly.log"
    shell:
        """
        mkdir -p results/viral/{wildcards.sample} logs/viral
        python scripts/assemble_viral.py \
            --reads {input} \
            --spades-out {output.spades} \
            --trinity-out {output.trinity} \
            --threads {threads} \
            > {log} 2>&1
        """

rule blast_annotation:
    input:
        contigs="results/viral/{sample}/spades_contigs.fasta"
    output:
        "results/viral/{sample}/blast_annotation.tsv"
    params:
        db=config["references"]["blast_viral_db"]
    threads: config["threads"]["viral"]
    log:
        "logs/viral/{sample}.blast.log"
    shell:
        """
        python scripts/blast_annotation.py \
            --contigs {input.contigs} \
            --db {params.db} \
            --threads {threads} \
            --output {output} \
            > {log} 2>&1
        """

rule interproscan_annotation:
    input:
        "results/viral/{sample}/trinity_contigs.fasta"
    output:
        "results/viral/{sample}/interproscan.tsv"
    threads: config["threads"]["viral"]
    log:
        "logs/viral/{sample}.interpro.log"
    shell:
        """
        python scripts/interproscan_annotation.py \
            --fasta {input} \
            --threads {threads} \
            --output {output} \
            > {log} 2>&1
        """

rule viral_abundance:
    input:
        blast="results/viral/{sample}/blast_annotation.tsv",
        interpro="results/viral/{sample}/interproscan.tsv"
    output:
        abundance="results/viral/{sample}/abundance.tsv",
        class_abundance="results/viral/{sample}/classification_abundance.tsv"
    log:
        "logs/viral/{sample}.abundance.log"
    shell:
        """
        python scripts/viral_abundance.py \
            --blast {input.blast} \
            --interpro {input.interpro} \
            --abundance {output.abundance} \
            --classification-abundance {output.class_abundance} \
            > {log} 2>&1
        """
