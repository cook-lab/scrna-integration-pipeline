#!/bin/bash
#SBATCH --job-name=02_cellassign
#SBATCH --account=def-dcook
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=4:00:00
#SBATCH --gres=gpu:h100:1
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

# Step 02: CellAssign cell type annotation (GPU)
# Runs on raw.h5ad, produces predictions.csv

module load StdEnv/2023 python/3.11 cuda/12.9

source ~/projects/def-dcook/bin/scvi-tools/bin/activate

echo "=========================================="
echo "Job: $SLURM_JOB_NAME"
echo "Job ID: $SLURM_JOB_ID"
echo "Started: $(date)"
echo "=========================================="

# Verify GPU
echo ""
echo "GPU Status:"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
echo ""

python ../scripts/02_cellassign.py

echo ""
echo "Completed: $(date)"
