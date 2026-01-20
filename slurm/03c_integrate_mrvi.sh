#!/bin/bash
#SBATCH --job-name=03c_mrvi
#SBATCH --account=def-dcook
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=12:00:00
#SBATCH --gres=gpu:h100:1
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

# Step 03c: MrVI integration (GPU)
# Uses PyTorch backend (TorchMRVI) - same environment as scVI/scANVI
# Requires: preprocessed.h5ad from Step 01

module load StdEnv/2023 python/3.11 cuda/12.9

source ~/projects/def-dcook/bin/scvi-tools/bin/activate

echo "=========================================="
echo "Job: $SLURM_JOB_NAME"
echo "Job ID: $SLURM_JOB_ID"
echo "Started: $(date)"
echo "=========================================="

echo ""
echo "GPU Status:"
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv
echo ""

python ../scripts/03c_integrate_mrvi.py

echo ""
echo "Completed: $(date)"
