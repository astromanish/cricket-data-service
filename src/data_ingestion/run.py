# Import external packages
import requests
import pandas as pd
import duckdb
import os

# Import internal modules
from collection import collect_data
from loading import load_match_result_data, load_match_summary_data, load_match_player_data, load_match_innings_data
from preprocessing import process_teams, process_players
from utils.dao import insert_data_into_db
from config import DELTA_LAKE_PATH, TEAMS_TABLE_NAME, PLAYERS_TABLE_NAME

# Define a unified function for data collection, loading, preprocessing, and insertion
def collect_load_preprocess_insert():

    # Data Collection
    collect_data()
    
    # Data loading
    match_result_data = load_match_result_data()
    match_summary_data = load_match_summary_data()
    match_player_data = load_match_player_data()
    
    # Data preprocessing
    processed_teams = process_teams(match_result_data, match_summary_data, match_player_data)
    processed_players = process_players(match_player_data)
    
    # Connection to DuckDB
    conn = duckdb.connect(DELTA_LAKE_PATH)
    
    # Insertion into database
    insert_data_into_db(conn, processed_teams, TEAMS_TABLE_NAME)
    insert_data_into_db(conn, processed_players, PLAYERS_TABLE_NAME)
    
    conn.close()

    print("Data collection, loading, preprocessing, and insertion completed successfully!")

if __name__ == "__main__":
    collect_load_preprocess_insert()
