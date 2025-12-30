# scRNA-seq Integration Pipeline

A modular pipeline for large-scale single-cell RNA-seq integration using multiple methods (scVI, scANVI, MrVI, sysVI, Harmony) on HPC clusters.

## Features

- 🔬 **Multi-method integration**: Compare scVI, scANVI, MrVI, sysVI, and Harmony
- 🚀 **Optimized for scale**: Tested on 2M+ cells, 450+ samples
- ⚡ **GPU-accelerated**: Efficient use of cluster GPU resources
- 📊 **Automated benchmarking**: Built-in metrics and visualization
- 🔄 **SLURM integration**: Job dependencies and parallel execution
- 🧬 **Cell type annotation**: Integrated CellAssign workflow

## Pipeline Overview

```
01_preprocess ──────────┬──► 03a_scvi ──────┬──► 03b_scanvi ──┐
                        │                    │                 │
02_cellassign ──────────┼──► 03c_mrvi ──────┼─────────────────┼──► 04_benchmark ──► 05_finalize
                        │                    │                 │
                        └──► 03d_sysvi ─────┴─────────────────┘
                        └──► 03e_harmony ───────────────────────┘

Steps 03a, 03c, 03d, 03e run in PARALLEL
Step 03b (scANVI) requires 03a (scVI) to complete first
```

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/[your-username]/scrna-integration-pipeline.git
cd scrna-integration-pipeline

# Install dependencies
pip install scanpy scvi-tools anndata pandas numpy scipy matplotlib seaborn scikit-learn harmonypy
pip install scib scib-metrics  # Optional, for integration benchmarking
```
Alternatively, set up a virtual environment as described in [DRAC_SETUP.md](DRAC_SETUP.md)

### Running on DRAC/Nibi Cluster

```bash
# Make scripts executable
chmod +x *.sh

Job submission scripts are expected to be submitted from the `slurm/` directory. They will use the relative path to access the appropriate python scripts.

Currently, file paths are hardcoded into the individual python scripts in `scripts/`. Modify these according to your specific design.

# Submit entire pipeline with automatic dependencies
./submit_pipeline.sh

# Or submit individual steps
sbatch 01_preprocess.sh
sbatch 02_cellassign.sh
# ... etc
```

See [USAGE.md](USAGE.md) for detailed instructions and [DRAC_SETUP.md](DRAC_SETUP.md) for cluster-specific setup.

## Input Requirements

Your starting data should be an AnnData object (`raw.h5ad`) with:
- Raw counts in `.X` (sparse matrix preferred)
- `sample_id` column in `.obs` identifying each sample
- Gene names in `.var_names`

Interactive/custom preprocessing can be done to bypass 01_preprocess.sh as long as the general structure is preserved:
- Raw counts are stored in `.layers['counts']`
- `sample_id` column in `.obs` identifying each sample
- The anndata object is subset to the appropriate features (eg. HVGs) for subsequent embeddings

## Output

Each integration method produces:
- Trained model in `output/models/{method}/`
- Low-dimensional embedding in `output/embeddings/{method}/`
- Final integrated object in `output/anndata/integrated_{method}.h5ad`

The final `.h5ad` file includes:
- Original counts, normalized data
- Integration embeddings
- UMAP coordinates
- Leiden clusters
- Cell type predictions (from CellAssign)

## Resource Requirements

| Step | Type | CPUs | Memory | Time | GPU |
|------|------|------|--------|------|-----|
| 01_preprocess | CPU | 8 | 128GB | 4h | - |
| 02_cellassign | GPU | 8 | 64GB | 4h | 1x H100 |
| 03a-d (integration) | GPU | 8 | 64GB | 12h | 1x H100 |
| 03e (Harmony) | CPU | 8 | 64GB | 4h | - |
| 04_benchmark | CPU | 8 | 64GB | 2h | - |
| 05_finalize | CPU | 8 | 128GB | 4h | - |

*Adjust based on your dataset size*

## Methods Included

- **scVI**: Variational inference for scRNA-seq
- **scANVI**: Semi-supervised variant with cell type labels
- **MrVI**: Multi-resolution variational inference
- **sysVI**: System-aware integration
- **Harmony**: Fast batch correction (CPU-based)

## Documentation

- [USAGE.md](USAGE.md) - Detailed usage guide and examples
- [DRAC_SETUP.md](DRAC_SETUP.md) - Cluster-specific setup instructions

## Citation

If you use this pipeline, please cite the methods you employ:

- **scVI/scANVI**: Lopez et al. (2018), Xu et al. (2021)
- **MrVI**: Boyeau et al. (2023)
- **sysVI**: Heumos et al. (2023)
- **Harmony**: Korsunsky et al. (2019)

See the [references](docs/references.md) for full citations.

## Support

- 📖 Check [USAGE.md](USAGE.md) for common issues
- 🐛 Open an [issue](https://github.com/[your-username]/scrna-integration-pipeline/issues) for bugs
- 💬 Discuss with lab members via [issues](https://github.com/[your-username]/scrna-integration-pipeline/issues) or Slack

## License

MIT License - see [LICENSE](LICENSE) file for details.

