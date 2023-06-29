import datetime
import time
import random
# show sth on terminal
import logging 
# like week4 batch lesson
import uuid
# about timezone
import pytz
import pandas as pd
# write sth to file system
import io
import psycopg

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

SEND_TIMEOUT = 10
rand = random.Random()

create_table_statement = """
drop table if exists dummy_metrics;
create table dummy_metrics(
	timestamp timestamp,
	value1 integer,
	value2 varchar,
	value3 float
)
"""

def prep_db():
	# configuration like in docker-compose.yml
	with psycopg.connect("host=localhost port=5432 user=postgres password=example", autocommit=True) as conn:
		res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
		# database not exist
		if len(res.fetchall()) == 0:
			conn.execute("create database test;")
		# create table 
		with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example") as conn:
			conn.execute(create_table_statement)

def calculate_dummy_metrics_postgresql(curr):
	value1 = rand.randint(0, 1000)
	value2 = str(uuid.uuid4())
	value3 = rand.random()

	curr.execute(
		"insert into dummy_metrics(timestamp, value1, value2, value3) values (%s, %s, %s, %s)",
		(datetime.datetime.now(pytz.timezone('Europe/London')), value1, value2, value3)
	)

def main():
	prep_db()
	last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
	with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example", autocommit=True) as conn:
		for i in range(0, 100):
			# provide methods to execute sql
			with conn.cursor() as curr:
				calculate_dummy_metrics_postgresql(curr)

			new_send = datetime.datetime.now()
			seconds_elapsed = (new_send - last_send).total_seconds()
			if seconds_elapsed < SEND_TIMEOUT:
				time.sleep(SEND_TIMEOUT - seconds_elapsed)
			while last_send < new_send:
				last_send = last_send + datetime.timedelta(seconds=10)
			logging.info("data sent")

if __name__ == '__main__':
	main()