def getOtherMatchesData(other_tournament_data_files, session, mapping_sheet_path, load_timestamp):
    
    if other_tournament_data_files:
        other_tournaments_df = getOtherTournamentsDF(other_tournament_data_files)

        teams_mapping_df = readExcel(mapping_sheet_path, "teams")
        teams_mapping_df['database_teams'] = np.where(teams_mapping_df['database_teams'].isnull(),
                                                      teams_mapping_df['cricsheet_teams'],
                                                      teams_mapping_df['database_teams'])

        other_tournaments_df = pd.merge(teams_mapping_df, other_tournaments_df, left_on='cricsheet_teams',
                                        right_on='bowling_team', how='inner')
        other_tournaments_df = other_tournaments_df.drop(['cricsheet_teams', 'bowling_team'], axis=1).rename(
            columns={'database_teams': 'bowling_team'})

        other_tournaments_df = pd.merge(teams_mapping_df, other_tournaments_df, left_on='cricsheet_teams',
                                        right_on='batting_team', how='inner')
        other_tournaments_df = other_tournaments_df.drop(['cricsheet_teams', 'batting_team'], axis=1).rename(
            columns={'database_teams': 'batting_team'})

        existing_matches_data = getPandasFactoryDF(session, GET_EXISTING_MATCHES_SQL)
        existing_matches_list = existing_matches_data['src_match_id'].tolist()

        other_tournaments_df = other_tournaments_df[~other_tournaments_df['match_id'].apply(str).isin(existing_matches_list)]

        if not other_tournaments_df.empty:
            
            matches_df_t1 = other_tournaments_df[['match_id', 'season', 'start_date', 'venue', 'innings', 'ball', 'runs_off_bat',
                                  'extras', 'wicket_type', 'competition_name', 'batting_team', 'bowling_team']][
                other_tournaments_df['innings'] == 1] \
                .drop('innings', axis=1)

            matches_df_t1 = psql.sqldf('''select match_id as src_match_id, season, start_date as match_date, venue, competition_name, batting_team as team1,
            max(case when ball>19.5 then 20 else ball end) as team1_overs, sum(coalesce(runs_off_bat, 0))+ sum(coalesce(extras, 0)) as team1_score, 
            sum(case when (wicket_type is null or wicket_type='') then 0 else 1 end) as team1_wickets, bowling_team as inn1_bowl_team, 
            (sum(coalesce(runs_off_bat, 0))+sum(coalesce(extras, 0)) + 1) as team2_target from matches_df_t1 group by 
            match_id, season, start_date, venue, competition_name, batting_team, bowling_team''')

            venue_mapping_df = readExcel(mapping_sheet_path, "venue")

            venue_mapping_df['database_venue'] = np.where(venue_mapping_df['database_venue'].isnull(),
                                                          venue_mapping_df['cricsheet_venue'],
                                                          venue_mapping_df['database_venue'])
            venue_mapping_df['database_venue'] = venue_mapping_df['database_venue'].apply(
                lambda x: str(x).split(",")[0].replace("'", ""))

            venue_mapping_df['cricsheet_venue'] = venue_mapping_df['cricsheet_venue'].apply(
                lambda x: str(x).replace("'", ""))

            matches_df_t1 = matches_df_t1.merge(venue_mapping_df.drop_duplicates(), left_on='venue', right_on='cricsheet_venue', how='left') \
                # .drop(['venue', 'cricsheet_venue'], axis=1).rename(columns={'database_venue': 'venue'})

            matches_df_t1['venue'] = np.where(matches_df_t1['database_venue'].isnull(), matches_df_t1['venue'], matches_df_t1['database_venue'])

            venues_df = getPandasFactoryDF(session, GET_VENUE_DETAILS_SQL)[['stadium_name', 'venue_id']]

            matches_df_t1 = pd.merge(matches_df_t1, venues_df, how='left', \
                                     left_on=matches_df_t1['venue'].str.replace(" ", "").str.strip().str.lower() \
                                     , right_on=venues_df['stadium_name'].str.replace(" ", "").str.strip().str.lower()) \
                .drop(['stadium_name', 'venue', 'key_0', 'cricsheet_venue', 'database_venue'], axis=1).rename(columns={'venue_id': 'venue'})

            matches_df_t2 = other_tournaments_df[['match_id', 'innings', 'ball', 'runs_off_bat', 'extras', 'wicket_type',
                                  'competition_name', 'batting_team']][other_tournaments_df['innings'] == 2].drop(
                'innings', axis=1)

            matches_df_t2 = psql.sqldf('''select match_id as src_match_id, batting_team as team2,
            max(case when ball>19.5 then 20 else ball end) as team2_overs, sum(coalesce(runs_off_bat, 0))+sum(coalesce(extras, 0)) as team2_score, 
            sum(case when (wicket_type is null or wicket_type='') then 0 else 1 end) as team2_wickets from matches_df_t2 group by match_id, batting_team''')

            # Generating squad for team1

            teams_df = getPandasFactoryDF(session, GET_TEAM_SQL)[['team_id', 'src_team_id', 'team_name']]

            team1_squad_striker = other_tournaments_df[['match_id', 'striker', 'batting_team']][
                other_tournaments_df['innings'] == 1].rename(columns={'match_id': 'src_match_id',
                                                                      'striker': 'player_name',
                                                                      'batting_team': 'team_name'})

            team1_squad_nonstriker = other_tournaments_df[['match_id', 'non_striker', 'batting_team']][
                other_tournaments_df['innings'] == 1].rename(columns={'match_id': 'src_match_id',
                                                                      'non_striker': 'player_name',
                                                                      'batting_team': 'team_name'})
            team1_squad_bowler = other_tournaments_df[['match_id', 'bowler', 'bowling_team']][
                other_tournaments_df['innings'] == 2].rename(columns={'match_id': 'src_match_id',
                                                                      'bowler': 'player_name',
                                                                      'bowling_team': 'team_name'})

            players_mapping_df = readExcel(mapping_sheet_path, "players")
            players_mapping_df['database'] = np.where(players_mapping_df['database'].isnull(), players_mapping_df['cricsheet'],
                                                      players_mapping_df['database'])

            team1_squad = getMatchesSquadDF(session, team1_squad_striker, team1_squad_nonstriker, team1_squad_bowler,
                                            players_mapping_df)

            matches_df_t1 = matches_df_t1.merge(team1_squad, left_on=['src_match_id', 'team1'],
                                                right_on=['src_match_id', 'team_name'], how='left').rename(
                columns={'player_id': 'team1_players'}).drop('team_name', axis=1)

            # generating squad for team2

            team2_squad_striker = other_tournaments_df[['match_id', 'striker', 'batting_team']][
                other_tournaments_df['innings'] == 2].rename(columns={'match_id': 'src_match_id',
                                                                      'striker': 'player_name',
                                                                      'batting_team': 'team_name'})

            team2_squad_nonstriker = other_tournaments_df[['match_id', 'non_striker', 'batting_team']][
                other_tournaments_df['innings'] == 2].rename(columns={'match_id': 'src_match_id',
                                                                      'non_striker': 'player_name',
                                                                      'batting_team': 'team_name'})
            team2_squad_bowler = other_tournaments_df[['match_id', 'bowler', 'bowling_team']][
                other_tournaments_df['innings'] == 1].rename(columns={'match_id': 'src_match_id',
                                                                      'bowler': 'player_name',
                                                                      'bowling_team': 'team_name'})
            team2_squad = getMatchesSquadDF(session, team2_squad_striker, team2_squad_nonstriker, team2_squad_bowler,
                                            players_mapping_df)

            matches_df_t2 = matches_df_t2.merge(team2_squad, left_on=['src_match_id', 'team2'],
                                                right_on=['src_match_id', 'team_name'], how='left').rename(
                columns={'player_id': 'team2_players'}).drop('team_name', axis=1)

            # merging team1 and team2 dataframe
            matches_df = matches_df_t1.merge(matches_df_t2, on='src_match_id', how='left')

            matches_df['match_name'] = matches_df['team1'].apply(lambda x: getInitials(str(x)).upper()) + "VS" + matches_df[
                'team2'].apply(lambda x: getInitials(str(x)).upper()) + matches_df['match_date'].str.replace("-", "")

            existing_match_names_list = existing_matches_data['match_name'].tolist()

            matches_df = matches_df[~matches_df['match_name'].isin(existing_match_names_list)]

            matches_df['team2'] = matches_df['team2'].fillna(matches_df['inn1_bowl_team'])

            matches_df = pd.merge(matches_df, teams_df[['team_id', 'team_name']], how='left',
                                  right_on='team_name', left_on='team1').drop(['team_name', 'team1'], axis=1) \
                .rename(columns={'team_id': 'team1'})

            matches_df = pd.merge(matches_df, teams_df[['team_id', 'team_name']], how='left',
                                  right_on='team_name', left_on='team2').drop(['team_name', 'team2'], axis=1) \
                .rename(columns={'team_id': 'team2'})

            matches_df['src_match_id'] = matches_df['src_match_id'].astype(str)

            matches_df['venue'] = matches_df['venue'].fillna(-1).astype(int)

            matches_df[['is_playoff', 'is_title']] = 0
            matches_df[['toss_decision', 'match_time', 'match_result', 'overall_nature', 'dew']] = 'NA'
            matches_df['nature_of_wicket'] = 'TRUE'
            matches_df[['winning_team', 'toss_team']] = -1
            matches_df[['team2_score', 'team2_wickets', 'team1_score', 'team1_wickets']] = matches_df[
                ['team2_score', 'team2_wickets', 'team1_score', 'team1_wickets']].fillna(0).astype(int)

            # matches_df[['team1_players', 'team2_players']] = matches_df[['team1_players', 'team2_players']].fillna([])
            matches_df["team1_players"].loc[matches_df["team1_players"].isnull()] = matches_df["team1_players"].loc[
                matches_df["team1_players"].isnull()].apply(lambda x: [])

            matches_df["team2_players"].loc[matches_df["team2_players"].isnull()] = matches_df["team2_players"].loc[
                (matches_df["team2_players"].isnull()) | (matches_df["team2_players"] == "")].apply(lambda x: [])

            matches_df[['team1_overs', 'team2_overs']] = matches_df[['team1_overs', 'team2_overs']].fillna(0.0)

            matches_df['match_date_form'] = matches_df['match_date']
            matches_df['match_date'] = pd.to_datetime(matches_df['match_date'], format='%Y-%m-%d').apply(
                lambda x: x.strftime('%d %b %Y'))
            matches_df["load_timestamp"] = load_timestamp

            max_key_val = getMaxId(session, MATCHES_TABLE_NAME, MATCHES_KEY_COL, DB_NAME)

            final_matches_data = generateSeq(matches_df.drop_duplicates(subset=['match_name'], keep='first')
                                             .drop('inn1_bowl_team', axis=1).sort_values(['competition_name', 'match_date_form']),
                                             MATCHES_KEY_COL, max_key_val).to_dict(orient='records')

            return final_matches_data