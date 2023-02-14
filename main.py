from tercen.client import context as ctx
import tercen.util.helper_functions as utl

from operator_funcs import fit_phate
# http://127.0.0.1:5402/test/w/047abdf84a6863e86050b9486100ccff/ds/b81b2ae0-e959-4b57-b3e7-19a6e6f6b34d
# http://127.0.0.1:5400/test/w/047abdf84a6863e86050b9486100ccff/ds/823a75ea-98cf-4490-96a2-6e97f7aec483
# tercenCtx = ctx.TercenContext(workflowId="047abdf84a6863e86050b9486100ccff", stepId="b81b2ae0-e959-4b57-b3e7-19a6e6f6b34d",
                    # serviceUri = "http://127.0.0.1:5402/")
tercenCtx = ctx.TercenContext()

# TODO Add diagnostic plot
#      Save as relation

df = fit_phate(tercenCtx)
df = tercenCtx.add_namespace(df) 

#dfRel = utl.as_relation(df)
#dfJoin = utl.as_join_operator(dfRel, tercenCtx.context.cnames, 
#                tercenCtx.context.cnames)
#resDf = tercenCtx.context.save_relation(dfJoin)

tercenCtx.save(df)

