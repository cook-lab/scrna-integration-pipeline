#!/bin/bash
#SBATCH --job-name=03e_harmony
#SBATCH --account=def-dcook
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --time=06:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

# Step 03e: Harmony integration (CPU only)
# Requires: preprocessed.h5ad from Step 01

module load StdEnv/2023 python/3.11

source ~/projects/def-dcook/bin/scvi-tools/bin/activate

echo "=========================================="
echo "Job: $SLURM_JOB_NAME"
echo "Job ID: $SLURM_JOB_ID"
echo "Started: $(date)"
echo "=========================================="

python ../scripts/03e_integrate_harmony.py

echo ""
echo "Completed: $(date)"
