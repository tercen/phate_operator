import phate
from tercen.client import context as ctx
import pandas as pd
import numpy as np


# Cannot handle the table from the Embryod example...
def fit_phate(tercenCtx:ctx.TercenContext) -> pd.DataFrame:
  #, '.ri'
  df = tercenCtx.select(['.y', '.ci', '.ri'])
  
  dfCol = tercenCtx.cselect(tercenCtx.context.cnames)
  dfCol[".ci"] = range(0, len(dfCol) )
  dfRow = tercenCtx.rselect(tercenCtx.context.rnames)
  dfRow[".ri"] = range(0, len(dfRow) )


  # FIXME Cannot handle multi-level columns
  # To fix that, a new column must be added to dfCol which joins the other column values
  df['GeneID'] = df['.ci'].map(dfCol.set_index('.ci')[tercenCtx.context.cnames[0]])
  df['Seq'] = df['.ri'].map(dfRow.set_index('.ri')[tercenCtx.context.rnames[0]])
  # df = df.drop([".ci"], axis=1)
  # df = df.drop([".ri"], axis=1)

  
  # 26067884
  dfPvt = pd.pivot_table( df, values=".y", 
            index="Seq", columns="GeneID")

  dfPvt = dfPvt.replace(np.NaN, 0)

  phateModel = phate.PHATE()
  # Y_phate = phateModel.fit_transform(dfPvt) 

  dfOut = pd.DataFrame( phateModel.fit_transform(dfPvt) )


  
  dfOut.columns = ["PHATE_1", "PHATE_2"]

  # dfOut[".ci"] = df[".ci"]
  dfOut[".ri"] = df[".ri"] #range(0, len(dfOut))
  # dfOut["Batch"] = df["Batch"] #range(0, len(dfOut))

  
  

  return dfOut
