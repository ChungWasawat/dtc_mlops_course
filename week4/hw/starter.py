#get_ipython().system('pip freeze | grep scikit-learn')

import pickle
import pandas as pd
import argparse

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def load_model():
    with open('model.bin', 'rb') as f_in:
        dv, model = pickle.load(f_in)
    return dv, model

def predict(df):

    dv, model = load_model()

    categorical = ['PULocationID', 'DOLocationID']
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)

    return y_pred

def ride_prediction_hw(
        year: int = 2022, 
        month: int = 2,
        ):
    input = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04}-{month:02}.parquet'

    print('reading data...')
    df = read_data(input)
    print('predicting...')
    pred_value = predict(df)
    print(f'the mean of prediction from month ={month:02} and year ={year:04} is ',pred_value.mean())

    # upload to cloud storage


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process ride duration prediction.')
    parser.add_argument('year', type=int, help='enter year from 2022')
    parser.add_argument('month', type=int,  help='enter month from 1 to 12')
    args = parser.parse_args()

    year = args.year
    month = args.month

    ride_prediction_hw(year, month)

    
