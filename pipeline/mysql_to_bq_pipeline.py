import os

import mysql.connector as connection
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def data_pipeline_mysql_to_bq(**kwargs):
    mysql_host = kwargs.get('mysql_host')
    mysql_database = kwargs.get('mysql_database')
    mysql_user = kwargs.get('mysql_user')
    mysql_password = kwargs.get('mysql_password')
    bq_project_id = kwargs.get('bq_project_id')
    dataset = kwargs.get('dataset')

    try:
        mydb = connection.connect(
            host=mysql_host,
            database=mysql_database,
            user=mysql_user,
            passwd=mysql_password
        )

        all_tables = "SELECT table_name FROM information_schema.tables" \
        "   WHERE table_schema = '{}'".format(mysql_database)

        df_tables = pd.read_sql(all_tables, mydb, parse_dates={'Date': {'format': '%Y-%m-%d'}})

        for table in df_tables.TABLE_NAME:
            table_name = table

            # Extract table data from MySQL
            df_table_data = extract_table_from_mysql(table_name, mydb)

            # Transform table data from MySQL
            df_table_data = transform_data_from_table(df_table_data)

            # Load data to BigQuery
            load_data_into_bigquery(bq_project_id, dataset, table_name, df_table_data)

            # Show confirmation message
            print("Ingested table: {}".format(table_name))

        mydb.close() # close the connection
    except Exception as e:
        mydb.close()
        print(str(e))


"""
Simulate the extraction step in an ETL job
"""
def extract_table_from_mysql(table_name, my_sql_connection):
    # Extract data from mysql table
    extraction_query = 'SELECT * FROM  ' + table_name
    df_table_data = pd.read_sql(extraction_query, my_sql_connection)
    return df_table_data


"""
Simulates the transformation step in ETL job
"""
def transform_data_from_table(df_table_data):
    # Clean dates - convert to string
    object_cols = df_table_data.select_dtypes(include=['object']).columns
    for column in object_cols:
        dtype = str(type(df_table_data[column].values[0]))
        if dtype == "<class 'datetime.date'>":
            df_table_data[column] = df_table_data[column].map(lambda x: str(x))
    return df_table_data

"""
Simulate the load step in an ETL job
"""
def load_data_into_bigquery(bq_project_id, dataset, table_name, df_table_data):
    import pandas_gbq as pdbq
    full_table_name_bg = "{}.{}".format(dataset, table_name)
    pdbq.to_gbq(df_table_data, full_table_name_bg, project_id=bq_project_id, if_exists='replace')


"""
Call the main function -- values pulled from .env, not hardcoded.
Run auth_bigquery.py first if you haven't authenticated to BigQuery yet.
"""

kwargs = {
    'mysql_host': os.environ.get('MYSQL_HOST'),
    'mysql_database': os.environ.get('MYSQL_DATABASE'),
    'mysql_user': os.environ.get('MYSQL_USER'),
    'mysql_password': os.environ.get('MYSQL_PASSWORD'),
    'bq_project_id': os.environ.get('BQ_PROJECT_ID'),
    'dataset': os.environ.get('BQ_DATASET'),
}
data_pipeline_mysql_to_bq(**kwargs)
