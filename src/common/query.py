DB_NAME = 'duckdb_table'

# matches table config

GET_EXISTING_PLAYERS_DETAILS_SQL = f'''Select player_name, src_player_id, player_id 
from {DB_NAME};'''

GET_EXISTNG_TEAMS_DETAILS_SQL = f'''Select team_id, src_team_id, team_name, competition_name, seasons_played, titles, playoffs, 
team_short_name from {DB_NAME};'''

GET_EXISTING_VENUE_DETAILS_SQL = f'''Select stadium_name, src_venue_id, venue_id from {DB_NAME};'''

#################################

GET_EXISTING_FILES = f'''select file_name from {DB_NAME}.fileLogs'''


GET_PLAYERS_SQL = f'''Select player_id, src_player_id, season, competition_name, player_type, team_id, 
player_name, bowling_type, batting_type from {DB_NAME}.Players;'''

GET_VENUE_DETAILS_SQL = f'''Select stadium_name, src_venue_id, venue_id from {DB_NAME}.Venue;'''

GET_MATCHES_DETAILS_SQL = f'''Select match_id, src_match_id, team1, team2, team1_players, team2_players
                            from {DB_NAME}.Matches;'''

GET_EXISTING_MATCHES_SQL = f'''Select src_match_id, match_name from {DB_NAME}.Matches;'''

GET_MATCH_SUMMARY = f'''select src_match_id ,match_id, team1, team2, team1_players, team2_players, season, competition_name, 
load_timestamp, match_date, is_playoff, match_name, venue, winning_team from {DB_NAME}.Matches'''

GET_MATCH_DATA_SQL = f'''select match_id, batsman_id, innings, batting_position, batting_phase, against_bowler, runs,
is_four, is_six,is_one, is_two, is_three , is_dot_ball, extras, is_wicket, wicket_type, ball_runs, season, 
competition_name, load_timestamp, over_number,batsman_team_id, is_wide, is_no_ball, ball_number, bowler_team_id, out_batsman_id, 
is_bye, is_leg_bye, is_bowler_wicket, non_striker_id from {DB_NAME}.MatchBallSummary '''

