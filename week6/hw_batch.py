#!/usr/bin/env python
# coding: utf-8

import sys
import pickle
import pandas as pd

################################################### HOMEWORK ###########################################################
def read_data(filename: str):
    df = pd.read_parquet(filename)
    return df

def prepare_data(df: pd.DataFrame, categorical: list):
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')

    return df

def main(
    year: str = "2022",
    month: str = "01",
) -> None:

    input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f'results/type=yellow_year={year:04d}_month={month:02d}.parquet'

    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)
    
    categorical = ['PULocationID', 'DOLocationID']

    # read data
    df = read_data(input_file)
    # transform data
    df = prepare_data(df, categorical)
    # create ride_id
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    # pre-prediction
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    # prediction
    y_pred = lr.predict(X_val)


    print('predicted mean duration:', y_pred.mean())


    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred


    df_result.to_parquet(output_file, engine='pyarrow', index=False)

if __name__ == "__main__":
    main()