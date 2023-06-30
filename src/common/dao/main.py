import duckdb
import pandas as pd

def insert_data_into_db(connection, dataframe, table_name):
    # Convert dataframe to DuckDB table
    duckdb_table = duckdb.from_df(dataframe)

    # Register table in Delta Lake
    connection.register('delta_table', duckdb_table, create=True)

    # Execute SQL query to insert data into the table
    connection.execute(sql_query.format(table_name='delta_table'))

def fetch_data_from_db(connection, table_name, sql_query):
    # Execute SQL query to fetch data from the table
    result = connection.execute(sql_query.format(table_name=table_name))

    # Convert the result to a Pandas DataFrame
    dataframe = pd.DataFrame(result.fetchall(), columns=result.description)

    return dataframe
