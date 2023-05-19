from tercen.client import context as ctx
import tercen.util.helper_functions as utl

import pandas as pd
import numpy as np
from operator_funcs import fit_phate

import matplotlib.pyplot as plt
import os, hashlib, base64, tempfile, random, string



# http://127.0.0.1:5400/test/w/1363a5f9d61a415565cebfb6f1003019/ds/d48a3bfa-7153-41c5-bf73-31a1b931ddc1
# tercenCtx = ctx.TercenContext(workflowId="1363a5f9d61a415565cebfb6f1003019", stepId="d48a3bfa-7153-41c5-bf73-31a1b931ddc1",
                    # serviceUri = "http://127.0.0.1:5400/")
tercenCtx = ctx.TercenContext()


def plot_file_to_pandas(file_path, filename = None):
    if filename is None:
        filename = os.path.dirname(file_path)
    
    ftype = os.path.splitext(filename)[1]

    if type == 'png':
        mimetype = "image/png"
    elif type == 'svg':
        mimetype = "image/svg+xml"
    elif type == 'pdf':
        mimetype = "image/pdf"
    else:
        mimetype = 'unknown'
    pass

    checksum = hashlib.md5(open(file_path,'rb').read()).hexdigest()
    
    output_str = []
    for fpath in file_path:
        with open(file_path, mode="rb") as f:
            base64.b64encode(f.read())
            output_str.append(output_str)
        pass

    df = pd.DataFrame({
        "filename":filename,
        "mimetype":mimetype,
        "checksum":checksum,
        ".content":output_str
    })

# plot_file_to_df <- function(file_path, filename = NULL) {
  
#   if(is.null(filename)) filename <- basename(file_path)
  
#   type <- tools::file_ext(filename)
#   mimetype <- switch (type,
#     png = "image/png",
#     svg = "image/svg+xml",
#     pdf = "application/pdf",
#     "unknown"
#   )
  
#   # compute checksum
#   checksum <- as.vector(tools::md5sum(file_path))
  
#   # serialise
#   output_str <- sapply(file_path, function(x) {
#     base64enc::base64encode(
#       readBin(x, "raw", file.info(x)[1, "size"]),
#       "txt"
#     )
#   })
  
#   df <- tibble::tibble(
#     filename = filename,
#     mimetype = mimetype,
#     checksum = checksum,
#     .content = output_str
#   )
  
#   return(df)
# }

# #' Save plot as a temporary file.
# #'
# #' @param plt ggplot object.
# #' @param type any of png, pdf, svg.
# #' @keywords utils
# #' @export
# save_plot <- function(plt, type = "png", ...) {
#   tmp <- tempfile(fileext = paste0(".", type))
#   ggplot2::ggsave(tmp, plot = plt, ...)
#   return(tmp)
# }

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

plt.scatter( df["PHATE_1"], df["PHATE_2"],
            s=4 )
letters = string.ascii_lowercase
fname = ''.join(random.choice(letters) for i in range(12))
file_path = ''.join((tempfile.gettempdir(), '/', fname,
         '.png'))

plt.savefig(file_path)
plt.close()

filename = None

if filename is None:
    filename = os.path.dirname(file_path)

ftype = os.path.splitext(file_path)[1]

if ftype == '.png':
    mimetype = "image/png"
elif ftype == '.svg':
    mimetype = "image/svg+xml"
elif ftype == '.pdf':
    mimetype = "image/pdf"
else:
    mimetype = 'unknown'

checksum = hashlib.md5(open(file_path,'rb').read()).hexdigest()

output_str = []

for fpath in file_path:
    with open(file_path, mode="rb") as f:
        fc = f.read()
        output_str.append([base64.b64encode(fc)])

outs = str(output_str[0][0])
imgDf = pd.DataFrame({
    "filename":filename,
    "mimetype":mimetype,
    "checksum":checksum,
    ".content":outs
}, index=[0])


imgDfRel = utl.as_relation(imgDf)
imgDfJoin = utl.as_join_operator(imgDfRel, list(), list() )

df = tercenCtx.add_namespace(df) 

df[".i"] = df[".ci"]
df = df.drop(".ci", axis=1)

crel = tercenCtx.get_crelation()


rids_factor = ''.join((crel.id, "._rids"))


dfRel = utl.as_relation(df)
dfRel = utl.left_join_relation(dfRel, crel, ".i", rids_factor)


dfJoin = utl.as_join_operator(dfRel, tercenCtx.cnames, 
                tercenCtx.cnames )


#   # Output 3: Diagnostic plot (yield)
#   img_df <- tim::plot_file_to_df(plot_file, filename = plot_file)
#   img_df$mimetype <- 'image/png'
  
#   if( "filename" %in% names(df)){
#     img_df$filename <- df$filename[[1]]
#   }else{
#     img_df$filename <- "IMG"
#   }
#   # END of output 3 -> img_df


# img_df <-  res[[3]] %>%
#   as_relation() %>%
#   as_join_operator(list(), list()) #%>%



tercenCtx.save_relation([ dfJoin, imgDfJoin ])


