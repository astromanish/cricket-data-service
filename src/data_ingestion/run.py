#external packages
import sys 
import pickle
import datetime


# TODO: import collect_data() function from data_collection module

#functions for data loading
from loading.main import load_match_result_data, load_match_summary_data, load_match_player_data, load_match_innings_data, load_match_ball_data

#functions for data preprocessing
from preprocessing.teams.main import process_teams
from preprocessing.players.main import process_players
# from preprocessing.venue.main import process_venues
# from preprocessing.matches.main import process_matches
from preprocessing.match_ball_summary.main import process_match_ball_summary

#functions for data insertion 
sys.path.append('./../')
from common.dao.main import update_existing_data

# Define a unified function for data collection, loading, preprocessing, and insertion
def collect_load_preprocess_insert():

    #TODO: Add script to collect data from relevent APIs

    #### Data loading ####
    
    ## Record time
    load_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    ## Load data
    match_result_data = load_match_result_data()
    match_summary_data = load_match_summary_data()
    match_player_data = load_match_player_data()
    match_ball_data = load_match_ball_data()
    match_innings_tuple_data = load_match_innings_data()
    
    #### Data preprocessing ####
    
    processed_teams = process_teams(match_result_data, match_summary_data, match_player_data)
    processed_players = process_players(match_player_data)
    # processed_venues = process_venues()
    # processed_matches = process_matches()
    processed_match_ball_summary = process_match_ball_summary(match_innings_tuple_data)

    #### Insertion into database ####
    
    ##Convert to Serialized Dataframe
    serialized_df = pickle.dumps(processed_teams)
    serialized_players_df = pickle.dumps(processed_players)
    
    ##Insert Data 
    update_existing_data(serialized_df, 'teams')
    update_existing_data(serialized_players_df,'players')
    
    #### Print Success #### 
    print("Data collection, loading, preprocessing, and insertion completed successfully!")

if __name__ == "__main__":
    collect_load_preprocess_insert()
