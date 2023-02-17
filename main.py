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


    # for p in props:

# op.value = function(name, type=as.character, default=NULL){
#       property = Find(function(propertyValue) propertyValue$name == name ,
#                       self$query$operatorSettings$operatorRef$propertyValues)
#       if (is.null(property)) return(default)
#       return(type(property$value))
#     },
    # def operator_property(self, type="character", default=None):
        # self.context.cubeQuery.operatorSettings.operatorRef.propertyValues
        # pass



# TODO Add diagnostic plot
#      Save as relation

# df = fit_phate(tercenCtx)
props = tercenCtx.context.cubeQuery.operatorSettings.operatorRef.propertyValues
propVal = str(props)

df = pd.DataFrame({"PropVal": np.asarray([propVal]), ".ci":np.ndarray.astype(np.asarray([0]), np.int32)})
df = tercenCtx.add_namespace(df) 

#dfRel = utl.as_relation(df)
#dfJoin = utl.as_join_operator(dfRel, tercenCtx.context.cnames, 
#                tercenCtx.context.cnames)
#resDf = tercenCtx.context.save_relation(dfJoin)

tercenCtx.save(df)

