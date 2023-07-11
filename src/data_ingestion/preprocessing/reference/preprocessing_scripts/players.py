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



# function to generate player_type based on player_name
def getPlayerType(players_type_df):
    if not players_type_df.empty:
        players_type_df["first_name"] = players_type_df["player_name"].apply(lambda x: x.split(" ")[0])
        players_type_df["last_name"] = players_type_df["player_name"].apply(lambda x: x.split(" ")[-1])

        players_type_df = pred_wiki_name(players_type_df, 'last_name', 'first_name')
        players_type_df["player_type"] = np.where(players_type_df['race'] == 'Asian,IndianSubContinent', "Domestic",
                                                  "Overseas")

        overseas2Domestic = ["Umran Malik", "Tejas Baroka", "Syed Mohammad", "Mahipal Lomror", "Khaleel Ahmed",
                             "Ankit Bawne", "Krishnappa Gowtham", "Mohammed Shami", "Abdul Samad", "Virender Sehwag",
                             "Kb Arun Karthik", "Faiz Fazal", "Mohammad Kaif", "Yogesh Takawale", "Dishant Yagnik",
                             "Manprit Juneja", "Iqbal Abdulla", "Kartik Tyagi", "Cm Gautam", "Shahbaz Nadeem",
                             "Yogesh Nagar", "Vvs Laxman", "Murali Kartik", "Nayan Doshi", "Aditya Dole", "Paul Valthaty",
                             "Jaydev Unadkat", "Love Ablish", "Asif Km", "Stuart Binny", "Amit Uniyal", "Kc Cariappa",
                             "Dinesh Karthik", "Shahbaz Ahmed", "Abu Nechim", "R Ashwin", "Shrikant Wagh", "Varun Aaron",
                             "Ronit More", "Jasprit Bumrah", "Rahul Dravid", "Harpreet Brar", "Kedar Jadhav",
                             "Ravindra Jadeja", "Ms Dhoni", "Sarfaraz Khan", "Chetan Sakariya", "Manan Vohra",
                             "Abrar Kazi", "Rahul Chahar", "Mohammed Siraj", "Zaheer Khan", "Ts Suman", "Sachin Baby",
                             "Unmukt Chand", "Shubman Gill", "Ishan Kishan", "Ishan Porel", "Yusuf Pathan",
                             "Sheldon Jackson", "Sai Kishore R", "Ayush Badoni", "Mohsin Khan", "Aman Khan", "Axar Patel"]

        players_type_df.loc[players_type_df['player_name'].isin(overseas2Domestic), 'player_type'] = 'Domestic'

        domestic2Overseas = ["Thilan Thushara", "Shakib Al Hasan", "Nuwan Kulasekara", "Kumar Sangakkara", "Ish Sodhi",
                             "Krishmar Santokie", "Lasith Malinga", "Kushal Janith Perera", "Sanath Jayasuriya",
                             "Muttiah Muralitharan", "Ravi Bopara", "Sachithra Senanayake", "Suraj Randiv", "Johan Botha",
                             "Ravi Rampaul", "Tillakaratne Dilshan", "Dilhara Fernando", "Mahela Jayawardene",
                             "Sunil Narine", "Gudakesh Motie", "Akila Dananjaya", "Isuru Udana Tillakaratne",
                             "Ajantha Mendis", "Maheesh Theekshana", "Bhanuka Rajapaksa", "Dushmantha Chameera"]

        players_type_df.loc[players_type_df['player_name'].isin(domestic2Overseas), 'player_type'] = 'Overseas'

        return players_type_df


def getPlayersData(session, squad_data_files, other_tournament_data_files, mapping_sheet_path, load_timestamp):
    if squad_data_files or other_tournament_data_files:
        if squad_data_files:
            players_df = getSquadRawData(squad_data_files, SQUAD_KEY_LIST, PLAYERS_REQD_COLS) \
                .drop_duplicates(subset=["TeamID", "PlayerName", "PlayerID", "season", "competition_name"],
                                keep='last').reset_index()

            players_df['player_skill'] = players_df['PlayerSkill'].map(lambda x: x.strip().upper().replace('ALLRONDER',
                                                                                                        'ALLROUNDER'))
            players_df['is_batsman'] = np.where((players_df['player_skill'] == 'BATSMAN') |
                                                (players_df['player_skill'] == 'ALLROUNDER')
                                                | (players_df['player_skill'] == 'WICKETKEEPER'), 1, 0)

            players_df['is_bowler'] = np.where((players_df['player_skill'] == 'BOWLER') |
                                            (players_df['player_skill'] == 'ALLROUNDER'), 1, 0)

            players_df['is_wicket_keeper'] = np.where(players_df['player_skill'] == 'WICKETKEEPER', 1, 0)

            players_df['batting_type'] = players_df['BattingType'].map(lambda x: x.strip().upper())
            players_df['bowling_type'] = players_df['BowlingProficiency'].map(lambda x: x.strip().upper())
            players_df['bowling_type'] = players_df['bowling_type'].apply(lambda x: "LEFT ARM FAST"
            if x == "LEFT ARM KNUCKLEBALL" else "RIGHT ARM FAST" if x == "RIGHT ARM KNUCKLEBALL" else x)

            players_df['bowl_major_type'] = np.where((players_df['bowling_type'] == 'LEFT ARM FAST') |
                                                    (players_df['bowling_type'] == 'RIGHT ARM FAST'), 'SEAM', 'SPIN')

            players_df["player_name"] = players_df["PlayerName"].apply(lambda x: x.replace("'", "").replace('Akshar Patel', 'Axar Patel').replace('Jason Behrendroff', 'Jason Behrendorff'))

            # adding column load timestamp
            players_df["load_timestamp"] = load_timestamp

            players_df = players_df.drop(["BattingType", "BowlingProficiency", "PlayerSkill", "index", "PlayerName",
                                        "src_match_id", "TeamID"]
                                        , axis=1) \
                .rename(columns={"PlayerID": "src_player_id", "IsCaptain": "is_captain", "TeamName": "team_name"})

            players_df['season'] = players_df['season'].astype(int)

            players_df['player_image_url'] = (IMAGE_STORE_URL + 'players/' + players_df['player_name'].apply(lambda x: x.replace(' ', '-')
                                                                                  .lower()).astype(str) + ".png")

            other_players_df = getOtherPlayersData(players_df, other_tournament_data_files, mapping_sheet_path, load_timestamp)
            
            players_df = players_df.append(other_players_df, ignore_index=True)
        else:
            players_df = pd.DataFrame(columns=['src_player_id', 'player_name', 'batting_type', 'bowling_type', 'player_skill',
            'is_captain', 'is_batsman', 'is_bowler', 'is_wicket_keeper', 'bowl_major_type', 'player_image_url', 'season'])
            other_players_df = getOtherPlayersData(players_df, other_tournament_data_files, mapping_sheet_path, load_timestamp)
            players_df = other_players_df

        teams_df = getPandasFactoryDF(session, GET_TEAM_SQL)

        players_df = players_df.merge(teams_df[["team_name", "team_id"]], on='team_name', how='left')
        # Get existing df from target table
        players_existing_df = getPandasFactoryDF(session, GET_PLAYERS_SQL)

        players_latest_df = pd.merge(players_df, players_existing_df[['src_player_id', 'season', 'competition_name', 'team_id']],
                                     how='left', on=['src_player_id', 'season', 'competition_name', 'team_id'], indicator=True)

        players_df = players_latest_df[players_latest_df['_merge'] == "left_only"]

        if not players_df.empty:

            players_df = pd.merge(players_df, players_existing_df[['src_player_id', 'player_id']].drop_duplicates(),
                                         how='left', on=['src_player_id'])

            if 'player_id_y' in players_df.columns:
                players_df = players_df.drop('player_id_y',axis=1).rename(columns={'player_id_x':'player_id'})

            players_df = getPlayerType(players_df)[
                ["player_id", "src_player_id", "player_name", "batting_type", "bowling_type", "player_skill",
                 "team_id", "season", "competition_name", "is_captain", "is_batsman", "is_bowler",
                 "is_wicket_keeper", "player_type", "bowl_major_type", "player_image_url", "load_timestamp"]]

            new_players_df = players_df.loc[players_df['player_id'].isnull()]

            max_key_val = getMaxId(session, PLAYERS_TABLE_NAME, PLAYERS_KEY_COL, DB_NAME)

            new_players_df['player_id'] = new_players_df['src_player_id'].rank(method='dense', ascending=False) \
                .apply(lambda x: x + max_key_val).astype(int)

            updated_players_df = players_df.loc[players_df['player_id'].notnull()].copy()
            updated_players_df['player_id'] = updated_players_df['player_id'].astype(int)

            players_final_df = new_players_df.append(updated_players_df)
            players_final_df['team_id'] = players_final_df['team_id'].fillna(-1).astype(int)
 
            return players_final_df.to_dict(orient='records')
    else:


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