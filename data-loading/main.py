from config import data_feeds_path, squad_feeds_path, other_tournament_data_path
from config import match_schedule_file_name, match_summary_file_name, match_inning1_file_name, match_inning2_file_name, match_squad_file_name
from config import match_result_key, match_player_key, match_summary_key, match_batting_card_key, match_batting_head_to_head_key, match_bowling_card_key, match_bowling_head_to_head_key, match_extras_key, match_fall_of_wickets_key, match_manhattan_graph_key, match_manhattan_graph_key, match_manhattan_wickets_key, match_partnership_break_key, match_over_history_key, match_wagon_wheel_key, match_wagon_wheel_summary_key, match_partnership_scores_key
from utils import read_json_files, read_csv_files, combine_squad_data, combine_innings_data, convert_json_list_to_df

# get list of json from collected data  
match_schedule_json_data_list = read_json_files(data_feeds_path, match_schedule_file_name, 14, 2)
match_summary_json_data_list = read_json_files(data_feeds_path, match_summary_file_name, 22, 2)
match_squad_json_data_list = read_json_files(squad_feeds_path, match_squad_file_name, 8, 2)
innings_1_json_data_list = read_json_files(data_feeds_path, match_inning1_file_name, 10, 2)
innings_2_json_data_list = read_json_files(data_feeds_path, match_inning2_file_name, 10, 2)

# update some list of json
match_player_json_data_list = combine_squad_data(match_squad_json_data_list)
innings_json_data_list = combine_innings_data(innings_1_json_data_list, innings_2_json_data_list)

# get dataframe from list of json
match_result = convert_json_list_to_df(match_schedule_json_data_list, match_result_key)
match_player = convert_json_list_to_df(match_player_json_data_list, match_player_key)
match_summary = convert_json_list_to_df(match_summary_json_data_list, match_summary_key)
match_batting_card = convert_json_list_to_df(innings_json_data_list, match_batting_card_key)
match_extras = convert_json_list_to_df(innings_json_data_list, match_extras_key)
match_fall_of_wickets = convert_json_list_to_df(innings_json_data_list, match_fall_of_wickets_key)
match_wagon_wheel = convert_json_list_to_df(innings_json_data_list, match_wagon_wheel_key)
match_partnership_scores = convert_json_list_to_df(innings_json_data_list, match_partnership_scores_key)
match_partnership_break = convert_json_list_to_df(innings_json_data_list, match_partnership_break_key)
match_bowling_card = convert_json_list_to_df(innings_json_data_list, match_bowling_card_key)
match_manhattan_graph = convert_json_list_to_df(innings_json_data_list, match_manhattan_graph_key)
match_manhattan_wickets = convert_json_list_to_df(innings_json_data_list, match_manhattan_wickets_key)
match_over_history = convert_json_list_to_df(innings_json_data_list, match_over_history_key)
match_wagon_wheel_summary = convert_json_list_to_df(innings_json_data_list, match_wagon_wheel_summary_key)
match_batting_head_to_head = convert_json_list_to_df(innings_json_data_list, match_batting_head_to_head_key)
match_bowling_head_to_head = convert_json_list_to_df(innings_json_data_list, match_bowling_head_to_head_key)

print('collected data loaded into dataframe.')
