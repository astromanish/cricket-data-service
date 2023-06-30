from config import data_feeds_path, squad_feeds_path, other_tournament_data_path
from config import match_schedule_file_name, match_summary_file_name, match_inning1_file_name, match_inning2_file_name, match_squad_file_name
from config import match_result_key, match_player_key, match_summary_key, match_batting_card_key, match_batting_head_to_head_key, match_bowling_card_key, match_bowling_head_to_head_key, match_extras_key, match_fall_of_wickets_key, match_manhattan_graph_key, match_manhattan_wickets_key, match_partnership_break_key, match_over_history_key, match_wagon_wheel_key, match_wagon_wheel_summary_key, match_partnership_scores_key
from utils import read_json_files, read_csv_files, combine_squad_data, combine_innings_data, convert_json_list_to_df

def load_match_result_data():
    match_schedule_json_data_list = read_json_files(data_feeds_path, match_schedule_file_name, 14, 2)
    return convert_json_list_to_df(match_schedule_json_data_list, match_result_key)

def load_match_player_data():
    match_squad_json_data_list = read_json_files(squad_feeds_path, match_squad_file_name, 8, 2)
    match_player_json_data_list = combine_squad_data(match_squad_json_data_list)
    return convert_json_list_to_df(match_player_json_data_list, match_player_key)

def load_match_summary_data():
    match_summary_json_data_list = read_json_files(data_feeds_path, match_summary_file_name, 22, 2)
    return convert_json_list_to_df(match_summary_json_data_list, match_summary_key)

def load_match_innings_data():
    innings_1_json_data_list = read_json_files(data_feeds_path, match_inning1_file_name, 10, 2)
    innings_2_json_data_list = read_json_files(data_feeds_path, match_inning2_file_name, 10, 2)
    innings_json_data_list = combine_innings_data(innings_1_json_data_list, innings_2_json_data_list)
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
    return (match_batting_card, match_extras, match_fall_of_wickets, match_wagon_wheel, match_partnership_scores, match_partnership_break, match_bowling_card, match_manhattan_graph, match_manhattan_wickets, match_over_history, match_wagon_wheel_summary, match_batting_head_to_head, match_bowling_head_to_head)

def load_match_ball_data():
    match_balls = read_csv_files(other_tournament_data_path)
    return match_balls