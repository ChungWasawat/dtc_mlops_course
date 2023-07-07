import pandas as pd 

df = pd.read_parquet('data/yellow_tripdata_2023-01.parquet')

print("PU ", df['PULocationID'].isna().sum())
print("DO ", df['DOLocationID'].isna().sum())
