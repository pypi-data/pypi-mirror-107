import pandas_gbq as gbq
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv, find_dotenv
from google.cloud import bigquery
import traceback
from .constants import *
import requests
import time

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
credentials =  Credentials.from_service_account_file(BIG_QUERY_SERVICE_ACCOUNT_CRED)



client = bigquery.Client(
    credentials=credentials,
    project=credentials.project_id,
)



def insert_rows_array_in_bigquery(dataset=None, table=None, rows_to_insert=None):
    try:

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = BIG_QUERY_SERVICE_ACCOUNT_CRED
        client = bigquery.Client()
        table = f'{WRITE_BIG_QUERY_PROJECT}.{dataset}.{table}'
        rows_to_insert = rows_to_insert
        errors = client.insert_rows_json(table, rows_to_insert)
        assert errors == []

    except Exception as e:
        print(str(e))
        print(traceback.format_exc())

def insert_rows_in_bigquery(dataset=None, table=None, rows_to_insert=None):
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = BIG_QUERY_SERVICE_ACCOUNT_CRED
        client = bigquery.Client()
        table_id =  f'{WRITE_BIG_QUERY_PROJECT}.{dataset}.{table}'
        table = client.get_table(table_id)
        errors = client.insert_rows(table, rows_to_insert)
        if errors == []:
            print("Rows added successfully")
        else:
            print("Failed adding rows",'\n',errors)

    except Exception as e:
        print(str(e))
        print(traceback.format_exc())




def get_bigquery_data_from_query(query=None, max_retries=0, time_interval = 5):

    flag = True
    while (flag):
        try:
            if query:
                df = gbq.read_gbq(query=query, project_id=READ_BIG_QUERY_PROJECT, credentials=credentials)
                return df
            else:
                return "Query is None"
            flag = False
        except requests.exceptions.Timeout:
            print(f"readtimeot - - - - - - - - waiting for {time_interval} seconds")
            max_retries = max_retries - 1
            flag = False if max_retries <= 0 else True
            time.sleep(time_interval)
        except:
            print(traceback.format_exc())
            flag = False

def dump_dataframe_to_bigquery_table(dataset=None, table=None, dataframe=None, mode="append"):
    try:
        gbq.to_gbq(dataframe, dataset + "." + table, WRITE_BIG_QUERY_PROJECT, if_exists=mode, credentials=credentials)
        print("Appending Done")
    except Exception as e:
        print(str(e))
        print(traceback.format_exc())

def execute_bigquery_query(query, max_retries=0, time_interval = 5):
    flag = True
    while (flag):
        try:
            query_job = client.query(query)  # API request
            query_job.result()  # Waits for statement to finish
            print("Executed auery -- ", query)
            flag = False
        except requests.exceptions.Timeout:
            print(f"readtimeot - - - - - - - - waiting for {time_interval} seconds")
            max_retries = max_retries - 1
            flag = False if max_retries <= 0 else True
            time.sleep(time_interval)
        except:
            print(traceback.format_exc())
            flag = False



