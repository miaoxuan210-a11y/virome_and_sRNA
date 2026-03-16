# virome_and_sRNA

一个用于 **小RNA（sRNA）分析 + 病毒宏基因组分析** 的 Snakemake 代码库，基于给定流程图实现。

## 先说明两件关键事实

1. **真实分析必须有真实输入文件**（raw FASTQ）和参考数据库（宿主索引、病毒库、BLAST 库等）。
2. 本仓库为了联调，保留了 `scripts/*.py` 的 mock 模板实现；在没有外部工具时可跑通“示例链路”，但这不等于真实生物学结论。

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
- 将 sRNA 映射到已知病毒参考序列
- 小 RNA 长度与碱基分布分析

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
├── config/config.yaml
├── workflow/rules/
├── scripts/
│   ├── check_dependencies.py
│   ├── generate_mock_inputs.py
│   └── run_mock_pipeline.py
├── metadata/groups.tsv
├── envs/snakemake.yaml
└── docs/pipeline_mapping.md
```

## 运行前检查（推荐先执行）

```bash
python scripts/check_dependencies.py
```

该脚本会检查：`snakemake`、`fastp`、`bowtie2` 是否存在。

## 跑真实流程（需要真实输入和工具）

1. 在 `config/config.yaml` 中配置你的真实 `samples.*.raw_fastq` 与参考数据库路径。
2. 安装环境（推荐 conda）：

```bash
conda env create -f envs/snakemake.yaml
conda activate virome_srna
```

3. 先 dry-run：

```bash
snakemake -n --cores 8
```

4. 正式运行：

```bash
snakemake --cores 8
```

## 没有真实输入时：跑 mock 联调链路

> 用于验证“流程是否能从输入走到输出”，不是实际生信结果。

```bash
python scripts/run_mock_pipeline.py
```

它会自动：
- 生成最小 synthetic FASTQ 到 `data/raw/*.fastq.gz`
- 调用模板脚本产出 `results/` 全套中间与汇总结果

关键输出：
- `results/reports/workflow_summary.md`

## 注意事项

- `data/raw/*.fastq.gz` 已被 `.gitignore` 忽略，避免把原始测序数据提交到仓库。
- 你可以在保持当前 I/O 接口不变的前提下，把 `scripts/` 里的 mock 逻辑替换为真实工具调用。
