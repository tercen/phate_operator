from tercen.client import context as ctx
import tercen.util.helper_functions as utl

from operator_funcs import fit_phate
# http://127.0.0.1:5400/test/w/e8b46826b0b5a4b935374a416b000f26/ds/82701b5b-3fb7-4e00-8749-132183ea8d7d
# http://127.0.0.1:5400/test/w/e8b46826b0b5a4b935374a416b000f26/ds/591d896b-a563-4e7b-9cda-fe74e4491f1f
# http://127.0.0.1:5400/test/w/e8b46826b0b5a4b935374a416b000f26/ds/a433313e-ecb4-420d-925c-f4bd458c21b5
# http://127.0.0.1:5400/test/w/e8b46826b0b5a4b935374a416b000f26/ds/6c6c01b5-a6fb-45ef-8c81-53fd2801dd3b
# tercenCtx = ctx.TercenContext(workflowId="e8b46826b0b5a4b935374a416b000f26", stepId="6c6c01b5-a6fb-45ef-8c81-53fd2801dd3b")
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

