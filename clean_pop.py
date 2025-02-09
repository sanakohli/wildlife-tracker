# %%
import pandas as pd

df1 = pd.read_csv('data/co-est2019-alldata.csv', encoding = "ISO-8859-1")
df2 = pd.read_csv('data/co-est2023-alldata.csv', encoding = "ISO-8859-1")
df = df1.merge(df2, on='CTYNAME', suffixes=('_2019', '_2023'))
df.to_csv('data/county_populations.csv')
print(df.head().to_string())