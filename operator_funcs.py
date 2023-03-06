import phate
from tercen.client import context as ctx
import pandas as pd
import numpy as np


def fit_phate(tercenCtx:ctx.TercenContext, nDim:float=2, knn:float=5,
      decay:float=40, t='auto', gamma:float=1) -> pd.DataFrame:

  sdf = tercenCtx.select_sparse(wide=True).transpose()


  phateModel = phate.PHATE(n_components=nDim, knn=knn, decay=decay,
                  t=t, gamma=gamma, n_jobs = -1)


  dfOut = pd.DataFrame( phateModel.fit_transform( sdf ))

  dfOut.columns = [''.join(['PHATE_', str(i+1)]) for i in range(0, len(dfOut.columns))]

  dfOut[".ci"] = np.ndarray.astype(np.asarray(range(0, sdf.shape[0])), np.int32)


  return dfOut
