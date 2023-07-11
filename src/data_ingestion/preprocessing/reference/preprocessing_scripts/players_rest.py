import sys
sys.path.append("./../../")
sys.path.append("./")
import pandas as pd
import numpy as np


from common.dao_client import session
from common.dao.fetch_db_data import getMaxId, getPandasFactoryDF
from DataIngestion.utils.helper import getSquadRawData, readExcel, random_string_generator, getOtherTournamentsDF
from DataIngestion.config import (SQUAD_KEY_LIST,
                                  PLAYERS_TABLE_NAME,
                                  PLAYERS_KEY_COL,
                                  PLAYERS_REQD_COLS, IMAGE_STORE_URL)
from common.db_config import DB_NAME
from DataIngestion.query import (GET_TEAM_SQL, GET_PLAYERS_SQL)
from ethnicolr import pred_wiki_name





def get2022Players(session, MISSING_SQUAD_2022, MISSING_PLAYERS_2022, load_timestamp):
    GET_PLAYERS_DATA = f'''select src_player_id, player_id, player_name, batting_type, bowling_type, player_skill,
    is_captain, is_batsman, is_bowler, is_wicket_keeper, player_type, bowl_major_type
     from {DB_NAME}.Players; '''

    new_df = readExcel(MISSING_SQUAD_2022, "Sheet1")[['Player', 'Squad']]

    players_data = getPandasFactoryDF(session, GET_PLAYERS_DATA)
    if len(players_data)>0:
        players_data_df = players_data
        players_data_df["player_rank"] = players_data_df.groupby("player_id")["player_id"].rank(method="first",
                                                                                                ascending=True)
        players_data_df = players_data_df[players_data_df["player_rank"] == 1].drop('player_rank', axis=1)

        players_df = pd.merge(new_df, players_data_df, how='left',
                              left_on=new_df['Player'].apply(lambda x: x.strip().replace(" ", "").lower()),
                              right_on=players_data_df['player_name'].apply(lambda x: x.strip().replace(" ", "").lower())) \
            .drop(['Player', 'key_0'], axis=1).rename(columns={'Squad': 'team_short_name'})

        players_df['competition_name'] = 'IPL'
        players_df['season'] = 2022
        players_df = players_df[players_df['player_id'].notna()]
        missing_players_df = readExcel(MISSING_PLAYERS_2022, 'in')

        missing_players_df[['batting_type', 'bowling_type', 'bowl_major_type']] = \
            missing_players_df[['batting_type', 'bowling_type', 'bowl_major_type']].astype(str)

        missing_players_df['batting_type'] = missing_players_df['batting_type'].apply(lambda x: x.upper()).fillna('NA')
        missing_players_df['bowling_type'] = missing_players_df['bowling_type'].apply(lambda x: x.upper()).fillna('NA')
        missing_players_df['bowl_major_type'] = missing_players_df['bowl_major_type'].apply(lambda x: x.upper()).fillna('NA')

        missing_players_df['src_player_id'] = missing_players_df['player_name'].apply(lambda x: random_string_generator())
        missing_players_df = missing_players_df.drop('player_id', axis=1)
        max_key_val = getMaxId(session, PLAYERS_TABLE_NAME, PLAYERS_KEY_COL, DB_NAME)

        missing_players_df['player_id'] = missing_players_df['src_player_id'].rank(method='dense', ascending=False) \
            .apply(lambda x: x + max_key_val).astype(int)

        missing_players_df = missing_players_df.append(players_df)

        missing_players_df[['is_batsman', 'is_bowler', 'is_wicket_keeper', 'player_id', 'is_captain']] = missing_players_df[
            ['is_batsman', 'is_bowler', 'is_wicket_keeper', 'player_id', 'is_captain']].fillna(0).astype(int)

        missing_players_df['load_timestamp'] = load_timestamp

        teams_df = getPandasFactoryDF(session, GET_TEAM_SQL)

        missing_players_df = missing_players_df.merge(teams_df[["team_short_name", "team_id"]], on='team_short_name',
                                                      how='left') \
            .drop(["team_short_name"], axis=1)

        return missing_players_df.to_dict(orient='records')

def getOtherPlayersData(original_players_df, other_tournament_data_files, mapping_sheet_path, load_timestamp):
    if other_tournament_data_files:
        other_tournaments_df = getOtherTournamentsDF(other_tournament_data_files)
        players_mapping_df = readExcel(mapping_sheet_path, "players")
        players_mapping_df['database'] = np.where(players_mapping_df['database'].isnull(), players_mapping_df['cricsheet'],
                                                  players_mapping_df['database'])

        players_striker_df = other_tournaments_df[['striker', 'competition_name', 'season', 'batting_team']] \
            .rename(columns={'striker': 'player_name', 'batting_team': 'team_name'})

        players_nonstriker_df = other_tournaments_df[['non_striker', 'competition_name', 'season', 'batting_team']] \
            .rename(columns={'non_striker': 'player_name', 'batting_team': 'team_name'})

        players_bowler_df = other_tournaments_df[['bowler', 'competition_name', 'season', 'bowling_team']] \
            .rename(columns={'bowler': 'player_name', 'bowling_team': 'team_name'})

        players_df = players_striker_df.append(players_nonstriker_df, ignore_index=True)
        players_df = players_df.append(players_bowler_df, ignore_index=True).drop_duplicates()

        teams_mapping_df = readExcel(mapping_sheet_path, "teams")

        players_df = pd.merge(players_df, teams_mapping_df, left_on='team_name', right_on='cricsheet_teams',how='inner')

        players_df['database_teams'] = np.where(players_df['database_teams'].isnull(),
                                                players_df['cricsheet_teams'],
                                                players_df['database_teams'])
        players_df = players_df[['player_name', 'competition_name', 'season', 'database_teams']].rename(
            columns={'database_teams': 'team_name'})

        players_df = players_df.merge(players_mapping_df.drop_duplicates(), left_on='player_name',
                                      right_on='cricsheet', how='left')

        players_df['database'] = np.where(players_df['database'].isnull(), players_df['player_name'],
                                          players_df['database'])
        players_df = players_df.drop(['player_name', 'cricsheet'], axis=1).rename(columns={'database': 'player_name'})

        GET_PLAYERS_DATA = f'''select src_player_id, player_id, player_name, batting_type, bowling_type, player_skill,
            is_captain, is_batsman, is_bowler, is_wicket_keeper, player_type, bowl_major_type, player_image_url, season  
             from {DB_NAME}.Players; '''
        players_data_df = getPandasFactoryDF(session, GET_PLAYERS_DATA)

        if not players_data_df.empty:
            players_data_df["player_rank"] = players_data_df.groupby("player_id")["season"].rank(method="first", ascending=False)

        else:
            players_data_df = original_players_df[['src_player_id', 'player_name', 'batting_type', 'bowling_type', 'player_skill',
            'is_captain', 'is_batsman', 'is_bowler', 'is_wicket_keeper', 'bowl_major_type', 'player_image_url', 'season']]

            players_data_df["player_rank"] = players_data_df.groupby("src_player_id")["season"].rank(method="first", ascending=False)

        players_data_df = players_data_df[players_data_df["player_rank"] == 1].drop(['player_rank', 'season'], axis=1)

        players_df = players_df.merge(players_data_df, on='player_name', how='left')
        players_df['src_player_id'] = players_df['src_player_id'].fillna(
            players_df['player_name'].apply(lambda x: random_string_generator(x)))
        players_df[['batting_type', 'bowling_type', 'player_skill', 'bowl_major_type']] = \
            players_df[['batting_type', 'bowling_type', 'player_skill', 'bowl_major_type']].fillna("NA")
        players_df[['is_captain', 'is_batsman', 'is_bowler', 'is_wicket_keeper']] = \
            players_df[['is_captain', 'is_batsman', 'is_bowler', 'is_wicket_keeper']].fillna(0).astype(int)
        players_df["player_name"] = players_df["player_name"].apply(lambda x: x.replace("'", ""))
        players_df['player_image_url'] = players_df['player_image_url'].fillna("")
        players_df['load_timestamp'] = load_timestamp

        return players_df


# if __name__=="__main__":
#     import datetime
#     loaded_files = getAlreadyExistingValue(session, GET_EXISTING_FILES)
#     root_data_files = getLatestFiles(loaded_files, getFiles(ROOT_DATA_PATH))
#     load_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     squad_data_files = getLatestFiles(loaded_files, getFiles(SQUAD_ROOT_PATH))
#     other_tournament_data_files = getLatestFiles(loaded_files, getOtherTournamentFiles(OTHER_TOURNAMENTS_DATA_PATH))
#     players_data = getPlayersData(session, squad_data_files, other_tournament_data_files, OTHER_TOURNAMENTS_MAPPING_FILE, load_timestamp)
#     # print(getPrettyDF(players_data[players_data['team_id'].isnull()]))
#     if players_data:
#         # players data insert
#         insertToDB(session, players_data, DB_NAME, PLAYERS_TABLE_NAME)