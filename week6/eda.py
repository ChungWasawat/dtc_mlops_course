from datetime import datetime
import pandas as pd 
from deepdiff import DeepDiff

def prepare_data(df: pd.DataFrame, categorical: list):
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')

    return df

def dt(hour, minute, second=0):
    return datetime(2022, 1, 1, hour, minute, second)

################################################################################
df = pd.read_parquet('data/yellow_tripdata_2023-01.parquet')
categorical = ['PULocationID', 'DOLocationID']

# print("PU ", df['PULocationID'].isna().sum())
# print("DO ", df['DOLocationID'].isna().sum())

transformed_df = prepare_data(df, categorical)

# print(transformed_df.info())

# print("datetime1 ", dt(1, 2, 0))
# print("datetime2 ", type(dt(1, 10, 0)))
# print("datetime4 ", dt(2, 2, 1))
# print("datetime4 -  datetime1", dt(2, 2, 1)-dt(1, 2, 0))
# print("above but in seconds and min", (dt(2, 2, 1)-dt(1, 2, 0)).total_seconds(), (dt(2, 2, 1)-dt(1, 2, 0)).total_seconds()/60)


################################################################################
data = [
    (None, None, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2), dt(1, 10)),
    (1, 2, dt(2, 2), dt(2, 3)),
    (None, 1, dt(1, 2, 0), dt(1, 2, 50)),
    (2, 3, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),     
]
    
columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
test_df = pd.DataFrame(data, columns=columns)

tf_test_df = prepare_data(test_df, categorical)

# print("before\n", test_df.to_dict())
# print("after\n", tf_test_df.to_dict())

expected_test_df = pd.DataFrame([["-1", "-1", dt(1, 2), dt(1, 10), 8.0],
                   ["1", "-1", dt(1, 2), dt(1, 10), 8.0],
                   ["1", "2", dt(2, 2), dt(2, 3), 1.0]], columns=['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'duration'])

diff = DeepDiff( tf_test_df.to_dict(), expected_test_df.to_dict(), ignore_order=True)
print("comparison\n", diff)