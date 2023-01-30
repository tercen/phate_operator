import pandas as pd
import numpy as np
import phate
import scprep
import os 

download_path = '/home/thiago/Tercen/repos/phate_operator/data/'

sparse=True
T1 = scprep.io.load_10X(os.path.join(download_path, "scRNAseq", "T0_1A"), sparse=sparse, gene_labels='both')
T2 = scprep.io.load_10X(os.path.join(download_path, "scRNAseq", "T2_3B"), sparse=sparse, gene_labels='both')
T3 = scprep.io.load_10X(os.path.join(download_path, "scRNAseq", "T4_5C"), sparse=sparse, gene_labels='both')
T4 = scprep.io.load_10X(os.path.join(download_path, "scRNAseq", "T6_7D"), sparse=sparse, gene_labels='both')
T5 = scprep.io.load_10X(os.path.join(download_path, "scRNAseq", "T8_9E"), sparse=sparse, gene_labels='both')
# T1.head()

filtered_batches = []
for batch in [T1, T2, T3, T4, T5]:
    batch = scprep.filter.filter_library_size(batch, percentile=20, keep_cells='above')
    batch = scprep.filter.filter_library_size(batch, percentile=75, keep_cells='below')

    filtered_batches.append(batch)
del T1, T2, T3, T4, T5 # removes objects from memory


EBT_counts, sample_labels = scprep.utils.combine_batches(
    filtered_batches, 
    ["Day 00-03", "Day 06-09", "Day 12-15", "Day 18-21", "Day 24-27"],
    append_to_cell_names=True
)
del filtered_batches # removes objects from memory
EBT_counts.head()

EBT_counts = scprep.filter.filter_rare_genes(EBT_counts, min_cells=10)
EBT_counts = scprep.normalize.library_size_normalize(EBT_counts)
mito_genes = scprep.select.get_gene_set(EBT_counts, starts_with="MT-") # Get all mitochondrial genes. There are 14, FYI.

EBT_counts, sample_labels = scprep.filter.filter_gene_set_expression(
    EBT_counts, sample_labels, genes=mito_genes, 
    percentile=90, keep_cells='below')

EBT_counts = scprep.transform.sqrt(EBT_counts)
#scipy.sparse.csr_matrix(df.values)
barcodes = []
batches = []
flbl = []
for i in range(0, len(sample_labels)):
    sl = sample_labels.index[i]
    pts = str.split(sl, '_')
    barcodes.append( pts[0] )
    batches.append( pts[1] )
    flbl.append(sl)



EBT_counts_ = EBT_counts.iloc[:,range(0,500)]
EBT_counts_ = EBT_counts_.iloc[range(0,5000,3)]

EBT_counts.shape
phate_operator = phate.PHATE(n_jobs=-2)
phate_operator2 = phate.PHATE(n_jobs=-2)


dd = pd.read_csv('/home/thiago/Tercen/repos/phate_operator/data/tmp.csv', index_col="Seq")
sample_labels2 = pd.Series([str.split(i,'_')[1] for i in dd.index])
sample_labels2.index = dd.index
# dd.index = sample_labels.index
# dd.columns = EBT_counts.columns
sample_labels.__class__
Y_phate = phate_operator.fit_transform(EBT_counts)
Y_phate2 = phate_operator2.fit_transform(dd)

scprep.plot.scatter2d(Y_phate, c=sample_labels, figsize=(12,8), cmap="Spectral",
                      ticks=False, label_prefix="PHATE")

scprep.plot.scatter2d(Y_phate2, c=sample_labels2, figsize=(12,8), cmap="Spectral",
                      ticks=False, label_prefix="PHATE")


EBT_counts["labels"] = flbl
EBT_counts["barcodes"] = barcodes
EBT_counts["batches"] = batches

EBT_counts_ = EBT_counts.copy()




# EBT_counts_.iloc[0,1]
EBT_counts_.head()


EBT_counts_.to_csv('/home/thiago/Tercen/repos/phate_operator/data/scRNAseq_full_.csv', index=False, 
                chunksize=1000)

# from numpy import savetxt

# savetxt(
#     '/home/thiago/Tercen/repos/phate_operator/data/scRNAseq_full.csv', EBT_counts_.values, fmt='%d,%.1f,%.1f,%.1f',
#     header=','.join(EBT_counts_.columns), comments=''
# )