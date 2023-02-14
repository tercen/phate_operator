import phate
from tercen.client import context as ctx
import pandas as pd
import numpy as np


# Cannot handle the table from the Embryod example...
def fit_phate(tercenCtx:ctx.TercenContext) -> pd.DataFrame:
  #, '.ri'
  sdf = tercenCtx.select_sparse(wide=True)
    
  # dfCol = tercenCtx.cselect(tercenCtx.context.cnames)
  # dfCol[".ci"] = range(0, len(dfCol) )
  # dfRow = tercenCtx.rselect(tercenCtx.context.rnames)
  # dfRow[".ri"] = range(0, len(dfRow) )

  # y = ssp.csr_matrix(tercenCtx.select(['.y']))
  # col = y.nonzero()[0]
  

  # df = ssp.csr_matrix(tercenCtx.select(['.y', '.ci', '.ri']))
  # lines = df[:,0].nonzero()[0]
  # cols = df[:,1].toarray()[list(lines)].flatten()
  # rows = df[:,2].toarray()[list(lines)].flatten()
  # y   = df[:,0].toarray()[list(lines)].flatten()

  # # y.eliminate_zeros()
  # # df.eliminate_zeros()
  
  # col_u = np.unique(list(np.sort(df[".ci"].values)))
  # row_u = np.unique(list(np.sort(df[".ri"].values)))
  
  # # col_u = np.unique(list(np.sort(df[:,0].data)))
  # # row_u = np.unique(list(np.sort(df[:,1].data)))

  # # col_u = np.unique(list((col)))
  # # row_u = np.unique(list((row)))

  # # sdf = ssp.csr_matrix((y.data, (row, col)), shape=(len(row_u), len(col_u)))
  # sdf = ssp.csr_matrix((y, (rows, cols)), shape=(int(rows.max()+1), int(cols.max()+1)))
  # sdf = ssp.csr_matrix((df[".y"], (df[".ri"], df[".ci"])), shape=(rows.max(), cols.max()))


  # # # FIXME Cannot handle multi-level columns
  # # # To fix that, a new column must be added to dfCol which joins the other column values
  # df['GeneID'] = df['.ci'].map(dfCol.set_index('.ci')[tercenCtx.context.cnames[0]])
  # df['Seq'] = df['.ri'].map(dfRow.set_index('.ri')[tercenCtx.context.rnames[0]])
  # # df = df.drop([".ci"], axis=1)
  # # df = df.drop([".ri"], axis=1)

  
  # # 26067884
  # dfPvt = pd.pivot_table( sdf )

  # dfPvt = dfPvt.replace(np.NaN, 0)

  phateModel = phate.PHATE()
  # Y_phate = phateModel.fit_transform(dfPvt) 

  dfOut = pd.DataFrame( phateModel.fit_transform( sdf ))


  
  dfOut.columns = ["PHATE_1", "PHATE_2"]

  # dfOut[".ci"] = df[".ci"]
  dfOut[".ri"] = np.ndarray.astype(np.asarray(range(0, len(dfOut))), np.int32)
  # dfOut["Batch"] = df["Batch"] #range(0, len(dfOut))

  
  

  return dfOut
