import phate

def fit_phate(df):
  phate_model = phate.PHATE()
  df_out = phate_model.fit_transform(df)
  return df_out
