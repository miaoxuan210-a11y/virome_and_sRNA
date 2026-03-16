# Flowchart -> Workflow mapping

| Flowchart step | Snakemake rule | Output |
|---|---|---|
| Data preprocessing & QC | `trim_and_qc` | `results/qc/{sample}.clean.fastq.gz` |
| Remove host sequence | `remove_host_reads` | `results/qc/{sample}.host_removed.fastq.gz` |
| sRNA classification and annotation | `srna_classification` | `results/srna/{sample}/class_*.tsv` |
| miRNA identification and prediction | `mirna_prediction_quant` | `predicted_mirna.tsv` |
| miRNA quantify | `mirna_prediction_quant` | `mirna_quant.tsv` |
| miRNA expression and samples correlation | `demirna_and_enrichment` | `sample_correlation.tsv` |
| DEmiRNAs analysis | `demirna_and_enrichment` | `de_mirna.tsv` |
| miRNA target gene prediction | `demirna_and_enrichment` | `mirna_targets.tsv` |
| DEmiRNA target genes annotation | `demirna_and_enrichment` | `target_annotation.tsv` |
| Enrichment analysis (GO/KEGG) | `demirna_and_enrichment` | `enrichment.tsv` |
| Map to reference viral sequences | `map_to_viral_reference` | `map_to_viral.tsv` |
| Length and base distribution | `length_base_distribution` | `length_base_distribution.tsv` |
| Spades and Trinity assembly | `viral_assembly` | `spades_contigs.fasta`, `trinity_contigs.fasta` |
| Blast annotation | `blast_annotation` | `blast_annotation.tsv` |
| Interproscan annotation | `interproscan_annotation` | `interproscan.tsv` |
| Abundance analysis | `viral_abundance` | `abundance.tsv` |
| Viral classification and abundance visualization analysis | `viral_abundance` | `classification_abundance.tsv` |
