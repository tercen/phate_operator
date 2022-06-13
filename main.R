library(tercen)
library(tercenApi)
library(dplyr)
library(reticulate)

reticulate::source_python("main.py")

df <- (ctx <- tercenCtx()) %>%
  as.matrix(fill=0) %>%
  t()

df_out <- df %>%
  fit_phate()

colnames(df) <- c("PHATE_1", "PHATE_2")
df <- as.data.frame(df)
df$.ci <- 1:nrow(df) - 1

df %>%
  ctx$addNamespace() %>%
  ctx$save()