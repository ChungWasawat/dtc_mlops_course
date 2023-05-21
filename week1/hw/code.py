import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

#Q1
month = 1
file_name = f'yellow_tripdata_2022-0{month}.parquet'
df1 = pd.read_parquet(f'data/{file_name}')

#print(df1.info())
print('--------Q1-----------')
print(df1.shape[1])

print('--------Q2-----------')
df1['duration'] = (df1['tpep_dropoff_datetime'] - df1['tpep_pickup_datetime']) / pd.Timedelta(minutes=1)
print(df1[['duration']].std())

print('--------Q3-----------')
print('before removing ', df1.shape[0])
df2 = df1[(df1['duration'] > 0) & (df1['duration'] < 61)]
print('after removing ', df2.shape[0])
print((df2.shape[0]/df1.shape[0])*100)

print('--------Q4-----------')
categorical = ['PULocationID', 'DOLocationID']
df2[categorical] = df2[categorical].astype(str)

train_dicts = df2[categorical].to_dict(orient='records')
dv = DictVectorizer()
X_train = dv.fit_transform(train_dicts)
print('column ', X_train.shape[1])
target = 'duration'
y_train = df2[target].values

print('--------Q5-----------')
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred = lr.predict(X_train)
print('rmse ', mean_squared_error(y_train, y_pred, squared=False))

print('--------Q6-----------')
month = 2
file_name = f'yellow_tripdata_2022-0{month}.parquet'
df3 = pd.read_parquet(f'data/{file_name}')
df3['duration'] = (df3['tpep_dropoff_datetime'] - df3['tpep_pickup_datetime']) / pd.Timedelta(minutes=1)
df3 = df3[(df3['duration'] > 0) & (df3['duration'] < 61)]

val_dicts = df3[categorical].to_dict(orient='records')
X_val = dv.transform(val_dicts)
y_val = df3[target].values

y_pred2 = lr.predict(X_val)
print('rmse_val ', mean_squared_error(y_val, y_pred2, squared=False))