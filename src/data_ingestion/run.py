# Import internal modules
# from collection import collect_data
import sys 
import pickle

sys.path.append('./../')

from loading.main import load_match_result_data, load_match_summary_data, load_match_player_data
from preprocessing.teams.main import process_teams
from common.dao.main import update_existing_data

# Define a unified function for data collection, loading, preprocessing, and insertion
def collect_load_preprocess_insert():

    # Data Collection
    # collect_data()

    # Data loading
    match_result_data = load_match_result_data()
    match_summary_data = load_match_summary_data()
    match_player_data = load_match_player_data()
    
    # Data preprocessing
    processed_teams = process_teams(match_result_data, match_summary_data, match_player_data)

    # Insertion into database
    serialized_df = pickle.dumps(processed_teams)
    update_existing_data(serialized_df, 'teams')
    
    print("Data collection, loading, preprocessing, and insertion completed successfully!")

if __name__ == "__main__":
    collect_load_preprocess_insert()
