import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

data_path = os.getenv('data_path')

data_feeds_path = f'{data_path}/Data_Feeds'
squad_feeds_path = f'{data_path}/Squad_Feeds'
other_tournament_data_path = f'{data_path}/other-tournament-data'

# file name of collected data 
match_schedule_file_name = 'matchSchedule'
match_squad_file_name = 'squad'
match_summary_file_name = 'matchsummary' 
match_inning1_file_name = 'Innings1'
match_inning2_file_name = 'Innings2'

# key value of relevant data in json objects of collected data
match_result_key = 'Result'
match_player_key = 'squad'
match_summary_key = 'MatchSummary'
match_batting_card_key = 'BattingCard'
match_extras_key = 'Extras'
match_fall_of_wickets_key = 'FallOfWickets'
match_wagon_wheel_key = 'WagonWheel'
match_partnership_scores_key = 'PartnershipScores'
match_partnership_break_key = 'PartnershipBreak'
match_bowling_card_key = 'BowlingCard'
match_manhattan_graph_key = 'ManhattanGraph'
match_manhattan_wickets_key = 'ManhattanWickets'
match_over_history_key = 'OverHistory'
match_wagon_wheel_summary_key = 'WagonWheelSummary'
match_batting_head_to_head_key = 'battingheadtohead'
match_bowling_head_to_head_key = 'battingheadtohead'