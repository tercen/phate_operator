# PHATE operator

##### Description

PHATE is a dimensionality reduction algorithm for the visualisation of high-dimensional data.

##### Usage

Input|.
---|---
`row`   | represents the variables (e.g. genes, channels, markers)
`col`   | represents the observations (e.g. cells, samples, individuals) 
`y-axis`| measurement value

Settings|.
---|---
`NumDim`   | Number of dimensions in which the data will be embedded.
`KNN`   | Number of nearest neighbors on which to build kernel.
`Decay`   | Sets decay rate of kernel tails.
`t`   | Power to which the diffusion operator is powered sets the level of diffusion.
`Gamma`   | Informational distance constant between -1 and 1. gamma=1 gives the PHATE log potential, gamma=0 gives a square root potential.

Output|.
---|---
`PHATE_1, ..., PHATE_N`| components containing the new projected values


##### Details

The operator is based on the method described in [Moon et al., 2019](10.1038/s41587-019-0336-3):

> Moon, K.R., van Dijk, D., Wang, Z. et al. Visualizing structure and transitions in high-dimensional biological data. Nat Biotechnol 37, 1482–1492 (2019).

##### See Also

[umap](https://github.com/tercen/umap_operator), [tsne](https://github.com/tercen/tsne_operator)
