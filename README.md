# virome_and_sRNA

一个用于 **小RNA（sRNA）分析 + 病毒宏基因组分析** 的 Snakemake 代码库，基于你给出的流程图实现。

## 流程覆盖

### 1) 数据预处理与质控
- fastp 去接头、质控
- bowtie2 去宿主序列

### 2) sRNA 分析（Host focus）
- sRNA 分类注释（rRNA/tRNA/miRNA/snRNA/snoRNA）
- miRNA 识别与定量
- 样本相关性分析
- DEmiRNA 分析
- miRNA 靶基因预测
- DEmiRNA 靶基因注释
- GO/KEGG 富集分析
- 将sRNA映射到已知病毒参考序列
- 小RNA长度与碱基分布分析

### 3) 病毒宏基因组分析
- SPAdes + Trinity 组装
- BLAST 注释
- InterProScan 注释
- 丰度分析
- 病毒分类与丰度可视化输入表生成

## 项目结构

```text
.
├── Snakefile
├── config/
│   └── config.yaml
├── workflow/rules/
│   ├── preprocess.smk
│   ├── srna.smk
│   └── viral.smk
├── scripts/
├── metadata/groups.tsv
├── envs/snakemake.yaml
└── results/
```

## 快速开始

1. 准备输入数据（`config/config.yaml` 的 `samples.*.raw_fastq`）
2. 准备参考数据库路径（`references`）
3. 建议使用 conda 环境：

```bash
conda env create -f envs/snakemake.yaml
conda activate virome_srna
```

4. 预览流程图（DAG）

```bash
snakemake -n --dag | dot -Tpng > docs/dag.png
```

5. 运行流程

```bash
snakemake --cores 8
```

## 说明

- `scripts/` 下目前提供的是**可运行的模板脚本（mock实现）**，便于你快速搭建和联调流程。
- 你可以逐个替换为真实分析工具调用（例如 miRDeep2、ShortStack、featureCounts、DESeq2、TargetScan、clusterProfiler 等）。
- 当前结果文件命名和目录组织已经按流程图各步骤对应好，便于后续扩展和复现。
