#function to generate player_type based on player_name
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