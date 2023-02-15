from tercen.client import context as ctx
import tercen.util.helper_functions as utl

from operator_funcs import fit_phate
# http://127.0.0.1:5402/test/w/047abdf84a6863e86050b9486100ccff/ds/b81b2ae0-e959-4b57-b3e7-19a6e6f6b34d
# http://127.0.0.1:5402/test/w/047abdf84a6863e86050b9486100ccff/ds/2eb7b60f-8edc-4b03-9795-eb493682c64f
# http://127.0.0.1:5402/test/w/047abdf84a6863e86050b9486100ccff/ds/ae4799ab-0312-47dc-a1dd-2b2edef63fec # 2.3Gb
# tercenCtx = ctx.TercenContext(workflowId="047abdf84a6863e86050b9486100ccff", stepId="ae4799ab-0312-47dc-a1dd-2b2edef63fec",
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

