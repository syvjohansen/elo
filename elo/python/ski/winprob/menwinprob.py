import pandas as pd

refdf = pd.read_pickle("~/ski/elo/python/ski/menelodf2.pkl")
refdf = refdf.loc[refdf['season']==2020]

race = refdf.loc[refdf['race']==1]

