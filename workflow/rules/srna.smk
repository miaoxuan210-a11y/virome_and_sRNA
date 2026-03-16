rule srna_classification:
    input:
        "results/qc/{sample}.host_removed.fastq.gz"
    output:
        rRNA="results/srna/{sample}/class_rRNA.tsv",
        tRNA="results/srna/{sample}/class_tRNA.tsv",
        miRNA="results/srna/{sample}/class_miRNA.tsv",
        snRNA="results/srna/{sample}/class_snRNA.tsv",
        snoRNA="results/srna/{sample}/class_snoRNA.tsv"
    threads: config["threads"]["srna"]
    log:
        "logs/srna/{sample}.classification.log"
    shell:
        """
        mkdir -p results/srna/{wildcards.sample} logs/srna
        python scripts/srna_classify.py \
            --input {input} \
            --sample {wildcards.sample} \
            --outdir results/srna/{wildcards.sample} \
            > {log} 2>&1
        """

rule mirna_prediction_quant:
    input:
        "results/srna/{sample}/class_miRNA.tsv"
    output:
        predicted="results/srna/{sample}/predicted_mirna.tsv",
        quant="results/srna/{sample}/mirna_quant.tsv"
    log:
        "logs/srna/{sample}.mirna_prediction.log"
    shell:
        """
        python scripts/mirna_predict_quant.py \
            --mirna-class {input} \
            --predicted {output.predicted} \
            --quant {output.quant} \
            > {log} 2>&1
        """

rule map_to_viral_reference:
    input:
        reads="results/qc/{sample}.host_removed.fastq.gz"
    output:
        "results/srna/{sample}/map_to_viral.tsv"
    threads: config["threads"]["srna"]
    params:
        viral_ref=config["references"]["viral_reference_fasta"]
    log:
        "logs/srna/{sample}.map_viral.log"
    shell:
        """
        python scripts/map_to_viral.py \
            --reads {input.reads} \
            --viral-ref {params.viral_ref} \
            --threads {threads} \
            --output {output} \
            > {log} 2>&1
        """

rule length_base_distribution:
    input:
        reads="results/qc/{sample}.host_removed.fastq.gz",
        mapped="results/srna/{sample}/map_to_viral.tsv"
    output:
        "results/srna/{sample}/length_base_distribution.tsv"
    log:
        "logs/srna/{sample}.length_base.log"
    shell:
        """
        python scripts/length_base_distribution.py \
            --reads {input.reads} \
            --mapped {input.mapped} \
            --output {output} \
            > {log} 2>&1
        """

rule demirna_and_enrichment:
    input:
        quant=lambda wc: expand("results/srna/{sample}/mirna_quant.tsv", sample=SAMPLES)
    output:
        de="results/srna/{sample}/de_mirna.tsv",
        targets="results/srna/{sample}/mirna_targets.tsv",
        target_anno="results/srna/{sample}/target_annotation.tsv",
        enrichment="results/srna/{sample}/enrichment.tsv",
        correlation="results/srna/{sample}/sample_correlation.tsv"
    params:
        group_table=config["design"]["group_table"]
    log:
        "logs/srna/{sample}.demirna.log"
    shell:
        """
        python scripts/demirna_pipeline.py \
            --sample {wildcards.sample} \
            --quant-files {input.quant} \
            --group-table {params.group_table} \
            --de {output.de} \
            --targets {output.targets} \
            --target-anno {output.target_anno} \
            --enrichment {output.enrichment} \
            --correlation {output.correlation} \
            > {log} 2>&1
        """
