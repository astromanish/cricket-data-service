import inflection
import pandas as pd

def clean_match_summary_data(match_summary):
    match_summary.loc[match_summary.competition_name =='BIG BASH LEAGUE 2018-19', 'competition_name'] = 'BBL 2018-19'

def preapare_data(match_result, match_summary, match_player):
    match_result = create_winning_team_id_column(match_result)
    match_result['is_title'] = (match_result['MatchDateOrder'] == 1).astype(int)
    match_result['is_playoff'] = (
        match_result['MatchDateOrder'].isin([1, 2, 3, 4])).astype(int)

    match_result.columns = [inflection.underscore(col) for col in match_result.columns]
    match_summary.columns = [inflection.underscore(col) for col in match_summary.columns]
    match_player.columns = [inflection.underscore(col) for col in match_player.columns]

    return match_result, match_summary, match_player

def generate_match_df(match_summary, match_result):
    match_df = pd.merge(
        match_summary[['match_id', 'competition_name', 'first_batting_team_id', 'second_batting_team_id']],
        match_result[['match_id', 'is_title', 'is_playoff', 'winning_team_id']],
        on='match_id'
    )

    match_df['season'] = match_df.competition_name.apply(lambda x: x.split(' ')[1][:4])
    match_df.competition_name = match_df.competition_name.apply(lambda x: x.split(' ')[0])

    return match_df

def generate_teams_df(match_df, match_player):
    teams_data = []

    for team_id in set(match_df['first_batting_team_id']).union(set(match_df['second_batting_team_id'])):
        team_matches = match_df[(match_df['first_batting_team_id'] == team_id) | (match_df['second_batting_team_id'] == team_id)]
        competitions = team_matches['competition_name'].unique().tolist()

        for competition in competitions:
            competition_matches = team_matches[team_matches['competition_name'] == competition]
            season_year_list = competition_matches['season'].unique().tolist()
            titles_count = len(competition_matches[competition_matches['is_title'] & (competition_matches['winning_team_id'] == team_id)])
            playoffs_count = len(competition_matches[competition_matches['is_playoff'] == 1])

            team_data = {
                'team_id': team_id,
                'competition_name': competition,
                'seasons_played': season_year_list,
                'titles': titles_count,
                'playoffs': playoffs_count
            }

            teams_data.append(team_data)

    teams_df = pd.DataFrame(teams_data)
     # Add more relevent columns to teams df
    teams_df = pd.merge(teams_df, match_player[['team_id', 'team_name', 'team_image', 'team_code']], on='team_id')
    return teams_df

