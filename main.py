from tercen.client import context as ctx
import tercen.util.helper_functions as utl

import pandas as pd
import numpy as np
from operator_funcs import fit_phate


# http://127.0.0.1:5402/test/w/047abdf84a6863e86050b9486100ccff/ds/b81b2ae0-e959-4b57-b3e7-19a6e6f6b34d
# http://127.0.0.1:5402/test/w/047abdf84a6863e86050b9486100ccff/ds/2eb7b60f-8edc-4b03-9795-eb493682c64f
# http://127.0.0.1:5402/test/w/047abdf84a6863e86050b9486100ccff/ds/ae4799ab-0312-47dc-a1dd-2b2edef63fec # 2.3Gb
# http://127.0.0.1:5402/test/w/047abdf84a6863e86050b9486100ccff/ds/dcf305df-2f88-4ba6-89bf-06c01349a1ca # 1Gb
# tercenCtx = ctx.TercenContext(workflowId="047abdf84a6863e86050b9486100ccff", stepId="2eb7b60f-8edc-4b03-9795-eb493682c64f",
                    # serviceUri = "http://127.0.0.1:5402/")
tercenCtx = ctx.TercenContext()


# TODO Add diagnostic plot
#      Save as relation
#      Ensure property values are within range
#      Ensure op can work with multilevel columns/rows


nDim = tercenCtx.operator_property('NumDim', typeFn=float, default=2)
knn = tercenCtx.operator_property('KNN', typeFn=float, default=5)
decay = tercenCtx.operator_property('Decay', typeFn=float, default=40)
t = tercenCtx.operator_property('t', typeFn=str, default='auto')
if t != 'auto':
    t = float(t)
gamma = tercenCtx.operator_property('Gamma', typeFn=float, default=1)


df = fit_phate(tercenCtx, nDim=nDim, knn=knn, decay=decay, t=t, gamma=gamma)
df = tercenCtx.add_namespace(df) 

#dfRel = utl.as_relation(df)
#dfJoin = utl.as_join_operator(dfRel, tercenCtx.context.cnames, 
#                tercenCtx.context.cnames)
#resDf = tercenCtx.context.save_relation(dfJoin)

tercenCtx.save(df)

