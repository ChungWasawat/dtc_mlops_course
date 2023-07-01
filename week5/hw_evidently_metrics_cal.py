import datetime
import time
import random
import logging 
import uuid
import pytz
import pandas as pd
import io
import psycopg
import joblib

from prefect import task, flow

from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric, ColumnQuantileMetric, ColumnCorrelationsMetric


# ColumnCorrelationsMetric(column_name="prediction")
# ColumnQuantileMetric(column_name="fare_amount", quantile=0.5)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

SEND_TIMEOUT = 10
rand = random.Random()


create_table_statement = """
drop table if exists hw_metrics;
create table hw_metrics(
	timestamp timestamp,
	prediction_drift float,
	num_drifted_columns integer,
	share_missing_values float,
    fare_quantile_50 float,
    corr_pred_x_passenger_count float,
    corr_pred_x_trip_dist float,
    corr_pred_x_fare_amount float,
    corr_pred_x_total_amount float
)
"""

reference_data = pd.read_parquet('data/reference.parquet')
with open('models/lin_reg.bin', 'rb') as f_in:
	model = joblib.load(f_in)
	

raw_data = pd.read_parquet('data/green_tripdata_2023-03.parquet')

begin = datetime.datetime(2023, 3, 1, 0, 0)
num_features = ['passenger_count', 'trip_distance', 'fare_amount', 'total_amount']
cat_features = ['PULocationID', 'DOLocationID']
column_mapping = ColumnMapping(
    prediction='prediction',
    numerical_features=num_features,
    categorical_features=cat_features,
    target=None
)

report = Report(metrics = [
    ColumnDriftMetric(column_name='prediction'),
    DatasetDriftMetric(),
    DatasetMissingValuesMetric(),
    ColumnQuantileMetric(column_name="fare_amount", quantile=0.5),
    ColumnCorrelationsMetric(column_name="prediction")
])

@task(retries=2, retry_delay_seconds=5, name="connect to db")
def prep_db():
	with psycopg.connect("host=localhost port=5432 user=postgres password=example", autocommit=True) as conn:
		res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
		if len(res.fetchall()) == 0:
			conn.execute("create database test;")
		with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example") as conn:
			conn.execute(create_table_statement)
			
@task(retries=2, retry_delay_seconds=5, name="calculate metrics")
def calculate_metrics_postgresql(curr, i):
	# compare one day data (current data) with whole reference data
	current_data = raw_data[(raw_data.lpep_pickup_datetime >= (begin + datetime.timedelta(i))) &
		(raw_data.lpep_pickup_datetime < (begin + datetime.timedelta(i + 1)))]

	#current_data.fillna(0, inplace=True)
	current_data['prediction'] = model.predict(current_data[num_features + cat_features].fillna(0))

	report.run(reference_data = reference_data, current_data = current_data,
		column_mapping=column_mapping)

	result = report.as_dict()

	prediction_drift = result['metrics'][0]['result']['drift_score']
	num_drifted_columns = result['metrics'][1]['result']['number_of_drifted_columns']
	share_missing_values = result['metrics'][2]['result']['current']['share_of_missing_values']
	fare_quantile_50 = result['metrics'][3]['result']['current']['value']
	corr_pred_pass = result['metrics'][4]['result']['current']['pearson']['values']['y'][0]
	corr_pred_trip = result['metrics'][4]['result']['current']['pearson']['values']['y'][1]
	corr_pred_fare = result['metrics'][4]['result']['current']['pearson']['values']['y'][2]
	corr_pred_total = result['metrics'][4]['result']['current']['pearson']['values']['y'][3]

	# add the result to postgres db
	curr.execute(
		"insert into hw_metrics(timestamp, prediction_drift, num_drifted_columns, share_missing_values, fare_quantile_50, \
		corr_pred_x_passenger_count, corr_pred_x_trip_dist, corr_pred_x_fare_amount, corr_pred_x_total_amount) \
	    values (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
		(begin + datetime.timedelta(i), prediction_drift, num_drifted_columns, share_missing_values, fare_quantile_50, \
   		corr_pred_pass, corr_pred_trip, corr_pred_fare, corr_pred_total)
	)
	
@flow
def hw_monitoring():
	prep_db()
	date_name = 31
	last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
	with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example", autocommit=True) as conn:
		for i in range(0, date_name):
			with conn.cursor() as curr:
				calculate_metrics_postgresql(curr, i)

			new_send = datetime.datetime.now()
			seconds_elapsed = (new_send - last_send).total_seconds()
			if seconds_elapsed < SEND_TIMEOUT:
				time.sleep(SEND_TIMEOUT - seconds_elapsed)
			while last_send < new_send:
				last_send = last_send + datetime.timedelta(seconds=10)
			logging.info("data sent")

if __name__ == '__main__':
	hw_monitoring()