from .utils import preapare_data, generate_match_df, generate_teams_df, clean_match_summary_data

def process_teams(match_result, match_summary, match_player):
    clean_match_summary_data(match_summary)
    match_result, match_summary, match_player = preapare_data(match_result, match_summary, match_player)
    match_df = generate_match_df(match_summary, match_result)
    teams_df = generate_teams_df(match_df, match_player)

    return teams_df
