def getMatchesData(session, root_data_files, squad_data_files, PITCH_TYPE_DATA_PATH, load_timestamp, pitch_data_path_2019_to_2021):
    path_set = set(value for key, value in root_data_files.items()
                    if 'matchschedule' in key.split("-")[1].split(".")[0].strip().lower())

    match_data = getMatchScheduleData(path_set)[MATCHES_REQD_COLS]

    existing_matches_data = getPandasFactoryDF(session, GET_EXISTING_MATCHES_SQL)
    existing_matches_list = existing_matches_data['src_match_id'].tolist()

    match_data = match_data[~match_data['MatchID'].isin(existing_matches_list)]

    if ~match_data.empty:
        
        # teams df is deltalake teams df, match data is match result data 

        teams_df = getPandasFactoryDF(session, GET_TEAM_SQL)[['team_id', 'src_team_id', 'team_name']]

        matches_df = pd.merge(match_data, teams_df[['team_id', 'src_team_id']], how='left', left_on='FirstBattingTeamID',
                                right_on='src_team_id') \
            .rename(columns={'team_id': 'team1'}).drop(['FirstBattingTeamID', 'src_team_id'], axis=1)

        matches_df = pd.merge(matches_df, teams_df[['team_id', 'src_team_id']], how='left', left_on='SecondBattingTeamID',
                                right_on='src_team_id') \
            .rename(columns={'team_id': 'team2'}).drop(['SecondBattingTeamID', 'src_team_id'], axis=1)

        matches_df = pd.merge(matches_df, teams_df[['team_id', 'team_name']], how='left',
                                left_on=matches_df['TossTeam'].str.replace(" ", "").str.strip().str.lower(),
                                right_on=teams_df['team_name'].str.replace(" ", "").str.strip().str.lower()) \
            .rename(columns={'team_id': 'toss_team'}).drop(['TossTeam', 'team_name', 'key_0'], axis=1)

        matches_df["is_playoff"] = matches_df["MatchDateOrder"].apply(checkPlayoff)
        # matches_df["is_playoff"] = np.where(matches_df["seasons"]==2022, 0, 0)

        # getting is_title from MatchDateOrder key
        matches_df["is_title"] = matches_df["MatchDateOrder"].apply(checkTitle)
        # matches_df["is_title"] = np.where(matches_df["seasons"] == 2022, 0, 0)

        # Generating a set of source files
        match_path_set = set(value for key, value in root_data_files.items()
                                if 'matchsummary' in key.split("-")[1].split(".")[0].strip().lower())
        # Initializing empty DF
        append_match_summary_df = pd.DataFrame()

        # Reading each file one by one from path set
        for path in match_path_set:
            # Reading the JS file
            matches_data = readJsFile(path)['MatchSummary'][0]

            # Getting specific required keys
            matches_dict = {key: str(matches_data[key]).split('(')[0].strip() for key in matches_data.keys()
                            & {'MatchID', 'WinningTeamID', 'Target'}}

            match_summary_df = dataToDF([matches_dict])
            append_match_summary_df = append_match_summary_df.append(match_summary_df)

        matches_df = pd.merge(matches_df, append_match_summary_df, how='left', on="MatchID")

        null_result_df = matches_df[matches_df["WinningTeamID"].isnull()][["MatchID", "Comments"]]
        null_result_df["winning_team_name"] = null_result_df["Comments"].str.split(' ').apply(getListTill).str.join(" ")
        null_result_df = pd.merge(null_result_df, teams_df[['team_id', 'team_name']], how='left',
                                    left_on=null_result_df['winning_team_name'].str.replace(" ", "").str.strip().str.lower(),
                                    right_on=teams_df['team_name'].str.replace(" ", "").str.strip().str.lower()) \
            .rename(columns={'team_id': 'winning_team'}).drop(['winning_team_name', 'team_name', 'key_0'], axis=1)

        matches_df = psql.sqldf('''select mdf.MatchID as src_match_id, mdf.MatchDate as match_date, mdf.MatchTime as match_time,
        mdf.GroundName, mdf.TossDetails as toss_decision, mdf.FirstBattingSummary, mdf.SecondBattingSummary, mdf.is_playoff, 
        mdf.competition_name, mdf.seasons as season, mdf.team1, mdf.team2, mdf.toss_team, mdf.Comments as match_result, 
        coalesce(coalesce(tdf.team_id, nrdf.winning_team),-1) as winning_team, mdf.is_title, mdf.MatchName as 
        match_name, Target as team2_target from matches_df mdf left join teams_df tdf on (mdf.WinningTeamID=tdf.src_team_id) 
            left join null_result_df nrdf on (mdf.MatchID=nrdf.MatchID)''')

        matches_df["winning_team"] = matches_df["winning_team"].astype(int)
        
        #############################

        venues_df = getPandasFactoryDF(session, GET_VENUE_DETAILS_SQL)[['stadium_name', 'venue_id']]

        matches_df = pd.merge(matches_df, venues_df, how='left', \
                                left_on=matches_df['GroundName'].str.replace(" ", "").str.strip().str.lower() \
                                , right_on=venues_df['stadium_name'].str.replace(" ", "").str.strip().str.lower()) \
            .rename(columns={'venue_id': 'venue'}).drop(['stadium_name', 'GroundName', 'key_0'], axis=1)

        matches_df["team1_score"] = matches_df["FirstBattingSummary"].apply(
            lambda x: int(x.split("/")[0]) if (x != "") else 0)
        matches_df["team1_wickets"] = matches_df["FirstBattingSummary"].apply(
            lambda x: int(x.split("/")[1].split(" ")[0]) if (x != "") else 0)
        matches_df["team1_overs"] = matches_df["FirstBattingSummary"].apply(
            lambda x: x.split(" ")[1].strip().replace("(", "") if (x != "") else 0)
        matches_df["team2_score"] = matches_df["SecondBattingSummary"].apply(
            lambda x: int(x.split("/")[0]) if (x != "") else 0)
        matches_df["team2_wickets"] = matches_df["SecondBattingSummary"].apply(
            lambda x: int(x.split("/")[1].split(" ")[0]) if (x != "") else 0)
        matches_df["team2_overs"] = matches_df["SecondBattingSummary"].apply(
            lambda x: x.split(" ")[1].strip().replace("(", "") if (x != "") else 0)
        
        ##############################

        players_df = getPandasFactoryDF(session, GET_PLAYER_DETAILS_SQL).drop_duplicates()

        squad_key_cols = {"TeamID", "src_match_id", "PlayerID"}
        squad_df = getSquadRawData(squad_data_files, SQUAD_KEY_LIST, squad_key_cols)
        squad_df = pd.merge(squad_df, teams_df[['team_id', 'src_team_id']], how="left", left_on="TeamID",
                            right_on="src_team_id").drop("TeamID", axis=1)

        squad_df = pd.merge(squad_df, players_df[['src_player_id', 'player_id']], how="left", left_on="PlayerID",
                            right_on="src_player_id").drop("PlayerID", axis=1)[["src_match_id", "player_id", "team_id"]]

        squad_df["src_match_id"] = squad_df["src_match_id"].str.strip().astype(str)

        squad_df = squad_df.groupby(["src_match_id", "team_id"])["player_id"].agg(list).reset_index()

        matches_df = pd.merge(matches_df, squad_df, how="left", left_on=["team1", "src_match_id"],
                                right_on=["team_id", "src_match_id"]).rename(columns={"player_id": "team1_players"}) \
            .drop(["team_id", "FirstBattingSummary", "SecondBattingSummary"], axis=1)

        matches_df = pd.merge(matches_df, squad_df, how="left", left_on=["team2", "src_match_id"],
                                right_on=["team_id", "src_match_id"]).rename(columns={"player_id": "team2_players"}) \
            .drop(["team_id"], axis=1)

        matches_df = pd.merge(matches_df, getPitchTypeData(PITCH_TYPE_DATA_PATH), how="left", left_on="src_match_id",
                                right_on="match_id").drop(["match_id"], axis=1)
        
        ##################################

        pitch_data_2019_to_2021 = readCSV(pitch_data_path_2019_to_2021)[['match_name', 'Wicket Type']].rename(columns={"Wicket Type": "wicket_type"})

        matches_df = pd.merge(matches_df, pitch_data_2019_to_2021, how='left', on='match_name')

        matches_df['overall_nature'] = np.where(matches_df['overall_nature'].isnull(), matches_df['wicket_type'], matches_df['overall_nature'])

        matches_df['nature_of_wicket'] = np.where(matches_df['nature_of_wicket'].isnull(), matches_df['wicket_type'],
                                                    matches_df['nature_of_wicket'])

        matches_df[["nature_of_wicket", "overall_nature", "dew"]] = \
            matches_df[["nature_of_wicket", "overall_nature", "dew"]].fillna("NA").astype(str)
        matches_df[["nature_of_wicket", "overall_nature", "dew"]] = matches_df[["nature_of_wicket", "overall_nature", "dew"]]            
        matches_df = matches_df.drop('wicket_type', axis=1)

        matches_df["team1_players"].loc[matches_df["team1_players"].isnull()] = matches_df["team1_players"].loc[
            matches_df["team1_players"].isnull()].apply(lambda x: [])
        matches_df["team2_players"].loc[matches_df["team2_players"].isnull()] = matches_df["team2_players"].loc[
            matches_df["team2_players"].isnull()].apply(lambda x: [])

        matches_df["match_date_form"] = matches_df["match_date"] \
            .apply(lambda x: datetime.strptime(x, '%d %b %Y').strftime('%Y-%m-%d'))

        matches_df["load_timestamp"] = load_timestamp

        max_key_val = getMaxId(session, MATCHES_TABLE_NAME, MATCHES_KEY_COL, DB_NAME)

        final_matches_data = generateSeq(matches_df.sort_values(['competition_name', 'match_date_form']),
                                            MATCHES_KEY_COL, max_key_val) \
            .to_dict(orient='records')

        return final_matches_data

