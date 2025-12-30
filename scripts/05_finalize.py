#!/usr/bin/env python

# =========================
# CONFIG
# =========================
RAW_H5AD = "/home/dcook/projects/def-dcook/active/rare_ov/output/anndata/raw.h5ad"
CELLASSIGN_PREDICTIONS = "/home/dcook/projects/def-dcook/active/rare_ov/output/cellassign/predictions.csv"
EMBEDDINGS_DIR = "/home/dcook/projects/def-dcook/active/rare_ov/output/embeddings"
OUTPUT_DIR = "/home/dcook/projects/def-dcook/active/rare_ov/output/anndata"
# Analysis parameters
UMAP_MIN_DIST = 0.3
LEIDEN_RESOLUTION = 0.2
# =========================

import scanpy as sc
import pandas as pd
import numpy as np
import scipy.sparse as sp
import argparse
import os

print("=" * 60)
print("STEP 05: FINALIZE INTEGRATED OBJECT")
print("=" * 60)

# Parse command line arguments
parser = argparse.ArgumentParser(description='Assemble final integrated object')
parser.add_argument('--method', type=str, required=True, 
                    choices=['scvi', 'scanvi', 'mrvi', 'sysvi', 'harmony'],
                    help='Integration method to use')
parser.add_argument('--leiden-res', type=float, default=LEIDEN_RESOLUTION,
                    help=f'Leiden clustering resolution (default: {LEIDEN_RESOLUTION})')
parser.add_argument('--umap-min-dist', type=float, default=UMAP_MIN_DIST,
                    help=f'UMAP min_dist parameter (default: {UMAP_MIN_DIST})')

args = parser.parse_args()

METHOD = args.method
LEIDEN_RESOLUTION = args.leiden_res
UMAP_MIN_DIST = args.umap_min_dist
OUTPUT_H5AD = f"{OUTPUT_DIR}/integrated_{METHOD}.h5ad"

print(f"\nâš™ï¸  Configuration:")
print(f"   Method: {METHOD}")
print(f"   Leiden resolution: {LEIDEN_RESOLUTION}")
print(f"   UMAP min_dist: {UMAP_MIN_DIST}")

# Load raw data (immutable base)
print(f"\nðŸ“‚ Loading raw data: {RAW_H5AD}")
adata = sc.read_h5ad(RAW_H5AD)
print(f"   Cells: {adata.n_obs:,}")
print(f"   Genes: {adata.n_vars:,}")

# Add CellAssign annotations
print(f"\nðŸ“‹ Loading CellAssign annotations: {CELLASSIGN_PREDICTIONS}")
predictions = pd.read_csv(CELLASSIGN_PREDICTIONS, index_col='cell_id')
adata.obs['celltype_pred'] = predictions['celltype_pred'].reindex(adata.obs_names)
adata.obs['celltype_probability'] = predictions['max_probability'].reindex(adata.obs_names)
adata.obs['celltype_confident'] = predictions['confident'].reindex(adata.obs_names)

print(f"   Cell types: {adata.obs['celltype_pred'].nunique()}")
print(adata.obs['celltype_pred'].value_counts())

# Load selected embedding
embedding_path = f"{EMBEDDINGS_DIR}/{METHOD}/embedding.npz"
print(f"\nðŸ§¬ Loading {METHOD} embedding: {embedding_path}")

if not os.path.exists(embedding_path):
    raise FileNotFoundError(f"Embedding not found: {embedding_path}\nRun 03x_integrate_{METHOD}.py first!")

embedding_data = np.load(embedding_path, allow_pickle=True)
X_embed = embedding_data['embedding']
print(f"   Shape: {X_embed.shape}")

# Verify cell order matches
obs_names_embed = embedding_data['obs_names']
if not np.array_equal(obs_names_embed, adata.obs_names.to_numpy()):
    print("   âš ï¸  Warning: Cell order mismatch, reindexing...")
    # Create temporary DataFrame for proper reindexing
    embed_df = pd.DataFrame(X_embed, index=obs_names_embed)
    X_embed = embed_df.reindex(adata.obs_names).values

adata.obsm[f'X_{METHOD}'] = X_embed

# Normalize X for visualization (preserve counts in layer)
print("\nðŸ”¬ Normalizing for visualization...")
print("   Creating counts layer...")
adata.layers['counts'] = adata.X.copy()

# Ensure sparse format
if not sp.issparse(adata.X):
    adata.X = sp.csr_matrix(adata.X)

print("   Normalizing to 10,000 counts per cell...")
sc.pp.normalize_total(adata, target_sum=1e4)

print("   Log-transforming (base 2)...")
sc.pp.log1p(adata, base=2)

# Compute neighbors on the embedding
print(f"\nðŸ”— Computing neighborhood graph on {METHOD} embedding...")
sc.pp.neighbors(adata, use_rep=f'X_{METHOD}')

# Compute UMAP
print(f"\nðŸ—ºï¸  Computing UMAP (min_dist={UMAP_MIN_DIST})...")
sc.tl.umap(adata, min_dist=UMAP_MIN_DIST)

# Compute Leiden clustering
print(f"\nðŸŽ¯ Computing Leiden clustering (resolution={LEIDEN_RESOLUTION})...")
sc.tl.leiden(adata, resolution=LEIDEN_RESOLUTION, key_added='leiden')

n_clusters = adata.obs['leiden'].nunique()
print(f"   Found {n_clusters} clusters")
print("\n   Cluster sizes:")
print(adata.obs['leiden'].value_counts().sort_index())

# Save final integrated object
print(f"\nðŸ’¾ Saving integrated object: {OUTPUT_H5AD}")
adata.write_h5ad(OUTPUT_H5AD, compression="gzip")

# Summary
print("\n" + "=" * 60)
print("FINAL OBJECT SUMMARY")
print("=" * 60)
print(f"âœ… Created: {OUTPUT_H5AD}")
print(f"\nContents:")
print(f"   â€¢ X: Normalized, log-transformed counts ({adata.n_obs:,} Ã— {adata.n_vars:,})")
print(f"   â€¢ layers['counts']: Raw integer counts")
print(f"   â€¢ obsm['X_{METHOD}']: Integration embedding ({X_embed.shape[1]}D)")
print(f"   â€¢ obsm['X_umap']: UMAP coordinates")
print(f"   â€¢ obs['celltype_pred']: CellAssign annotations ({adata.obs['celltype_pred'].nunique()} types)")
print(f"   â€¢ obs['leiden']: Leiden clusters ({n_clusters} clusters)")
print(f"   â€¢ obs['sample_id']: Batch information ({adata.obs['sample_id'].nunique()} samples)")

print(f"\nðŸ’¡ Next steps:")
print(f"   â€¢ Visualize: scanpy.pl.umap(adata, color=['celltype_pred', 'leiden', 'sample_id'])")
print(f"   â€¢ Explore: Use Jupyter notebook or scanpy for downstream analysis")
print(f"   â€¢ Re-cluster: Run with different --leiden-res if needed")

print("\nâœ… Pipeline complete!")
