from tercen.client import context as ctx
import tercen.util.helper_functions as utl

import pandas as pd
import numpy as np
from operator_funcs import fit_phate


# http://127.0.0.1:5400/test/w/1363a5f9d61a415565cebfb6f1003019/ds/d48a3bfa-7153-41c5-bf73-31a1b931ddc1
# tercenCtx = ctx.TercenContext(workflowId="1363a5f9d61a415565cebfb6f1003019", stepId="d48a3bfa-7153-41c5-bf73-31a1b931ddc1",
                    # serviceUri = "http://127.0.0.1:5400/")
tercenCtx = ctx.TercenContext()


# TODO Add diagnostic plot
#      Save as relation
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
df = tercenCtx.add_namespace(df) 

df[".i"] = df[".ci"]


crel = tercenCtx.get_crelation()


rids_factor = ''.join((crel.id, "._rids"))


dfRel = utl.as_relation(df)
dfRel = utl.left_join_relation(dfRel, crel, ".i", rids_factor)


dfJoin = utl.as_join_operator(dfRel, tercenCtx.cnames, 
                tercenCtx.cnames[0] )
tercenCtx.save_relation(dfJoin)



# tercenCtx.save(df)
#
