import duckdb
import pandas as pd
from deltalake import DeltaTable
from deltalake.writer import write_deltalake
from .config import LOCAL_DELTA_LAKE_PATH, AZURE_DELTA_LAKE_PATH, OPTIONS
import pickle

def query_existing_data(table_name, sql_query):
    table_path = f'{LOCAL_DELTA_LAKE_PATH}/{table_name}'
    delta_table = DeltaTable(table_path, options=OPTIONS)
    pyarrow_delta_table = delta_table.to_pyarrow_dataset()
    duckdb_table = duckdb.arrow(pyarrow_delta_table)
    df = duckdb.query(sql_query).to_df()
    return df

def update_existing_data(serialized_df, table_name):
    df = pickle.loads(serialized_df)
    table_path = f'{LOCAL_DELTA_LAKE_PATH}/{table_name}'
    write_deltalake(table_path,df,overwrite_schema=True)
    