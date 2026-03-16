rule fastp_qc:
    input:
        lambda wc: f"{config['raw_dir']}/{wc.sample}.fastq"
    output:
        cleaned="results/qc/{sample}.clean.fastq.gz",
        html="results/qc/{sample}.fastp.html",
        json="results/qc/{sample}.fastp.json"
    threads: config["threads"]["fastp"]
    log:
        "logs/fastp/{sample}.log"
    shell:
        r"""
        mkdir -p results/qc logs/fastp
        fastp \
          --in1 {input} \
          --out1 {output.cleaned} \
          --html {output.html} \
          --json {output.json} \
          --thread {threads} \
          > {log} 2>&1
        """
