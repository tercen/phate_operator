from tercen.client import context as ctx
import tercen.util.helper_functions as utl

import pandas as pd
import numpy as np
from operator_funcs import fit_phate

import matplotlib.pyplot as plt
import os, hashlib, base64, tempfile, random, string



# http://127.0.0.1:5400/test/w/1363a5f9d61a415565cebfb6f1003019/ds/d48a3bfa-7153-41c5-bf73-31a1b931ddc1
# tercenCtx = ctx.TercenContext(workflowId="1363a5f9d61a415565cebfb6f1003019", stepId="d48a3bfa-7153-41c5-bf73-31a1b931ddc1",
                    # serviceUri = "http://127.0.0.1:5402/")
tercenCtx = ctx.TercenContext()


# TODO 
#      Ensure property values are within range
#      Ensure op can work with multilevel columns/rows


nDim = tercenCtx.operator_property('NumDim', typeFn=int, default=2)
knn = tercenCtx.operator_property('KNN', typeFn=int, default=5)
decay = tercenCtx.operator_property('Decay', typeFn=int, default=40)
t = tercenCtx.operator_property('t', typeFn=str, default='auto')
if t != 'auto':
    t = int(t)
gamma = tercenCtx.operator_property('Gamma', typeFn=float, default=1)


df = fit_phate(tercenCtx, nDim=nDim, knn=knn, decay=decay, t=t, gamma=gamma)

plt.scatter( df["PHATE_1"], df["PHATE_2"],
            s=4 )
letters = string.ascii_lowercase
fname = ''.join(random.choice(letters) for i in range(12))
file_path = ''.join((tempfile.gettempdir(), '/', fname,
         '.png'))


file_path = utl.get_temp_filepath(ext='png')

plt.savefig(file_path)
plt.close()

imgDf = utl.image_file_to_df(file_path)

imgDfRel = utl.as_relation(imgDf)
imgDfJoin = utl.as_join_operator(imgDfRel, list(), list() )

df = tercenCtx.add_namespace(df) 

df[".i"] = df[".ci"]

crel = tercenCtx.get_crelation()


rids_factor = ''.join((crel.id, "._rids"))


dfRel = utl.as_relation(df)
dfRel = utl.left_join_relation(dfRel, crel, ".i", rids_factor)


dfJoin = utl.as_join_operator(dfRel, tercenCtx.cnames, 
                tercenCtx.cnames )



tercenCtx.save_relation([ dfJoin, imgDfJoin ])
# tercenCtx.save(df)


