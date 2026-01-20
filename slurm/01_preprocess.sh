#!/bin/bash
#SBATCH --job-name=01_preprocess
#SBATCH --account=def-dcook
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --time=4:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

# Step 01: Preprocessing (CPU)
# Identifies HVGs and creates preprocessed.h5ad

module load StdEnv/2023 python/3.11

source ~/projects/def-dcook/bin/scvi-tools/bin/activate

echo "=========================================="
echo "Job: $SLURM_JOB_NAME"
echo "Job ID: $SLURM_JOB_ID"
echo "Started: $(date)"
echo "=========================================="

python ../scripts/01_preprocess.py

echo ""
echo "Completed: $(date)"
