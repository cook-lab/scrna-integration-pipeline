#!/bin/bash
#SBATCH --job-name=05_finalize
#SBATCH --account=def-dcook
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --time=4:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

# Step 05: Finalize integrated object (CPU)
# Requires: raw.h5ad, cellassign predictions, selected embedding
#
# Usage: sbatch 05_finalize.sh <method>
#   method: scvi, scanvi, mrvi, or sysvi
#
# Example: sbatch 05_finalize.sh scanvi

METHOD=${1:-scanvi}

module load StdEnv/2023 python/3.11

source ~/projects/def-dcook/bin/scvi-tools/bin/activate

echo "=========================================="
echo "Job: $SLURM_JOB_NAME"
echo "Job ID: $SLURM_JOB_ID"
echo "Method: $METHOD"
echo "Started: $(date)"
echo "=========================================="

python ../scripts/05_finalize.py --method $METHOD

echo ""
echo "Completed: $(date)"
