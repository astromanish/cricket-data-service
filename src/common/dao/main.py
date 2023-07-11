import duckdb
from deltalake import DeltaTable
from deltalake.writer import write_deltalake
from .config import azure_storage_account_name, azure_storage_account_key, local_delta_lake_path, azure_delta_lake_path
import pickle

# to access azure delta lake 
options={"AZURE_STORAGE_ACCOUNT_NAME": azure_storage_account_name,
 "AZURE_STORAGE_ACCOUNT_KEY":azure_storage_account_key}

def query_existing_data(table_name, sql_query):
    table_path = f'{local_delta_lake_path}/{table_name}'
    delta_table = DeltaTable(table_path, options=options)
    pyarrow_delta_table = delta_table.to_pyarrow_dataset()
    duckdb_table = duckdb.arrow(pyarrow_delta_table)
    df = duckdb.query(sql_query).to_df()
    return df

def update_existing_data(serialized_df, table_name):
    df = pickle.loads(serialized_df)
    table_path = f'{LOCAL_DELTA_LAKE_PATH}/{table_name}'
    write_deltalake(table_path,df)
    
