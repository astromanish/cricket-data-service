def getOtherMatchesBallSummary(session, other_data_files, mapping_sheet_path, load_timestamp):

    if other_data_files:
        con = createCon()

        final_tournament_df = getOtherTournamentsDF(other_data_files)

        players_mapping_df = readExcel(mapping_sheet_path, "players")
        players_mapping_df['database'] = np.where(players_mapping_df['database'].isnull(), players_mapping_df['cricsheet'],
                                                  players_mapping_df['database'])

        players_mapping_df["database"] = players_mapping_df["database"].apply(lambda x: str(x).replace("'", ""))

        venue_mapping_df = readExcel(mapping_sheet_path, "venue")

        venue_mapping_df['database_venue'] = np.where(venue_mapping_df['database_venue'].isnull(),
                                                      venue_mapping_df['cricsheet_venue'],
                                                      venue_mapping_df['database_venue'])
        venue_mapping_df['database_venue'] = venue_mapping_df['database_venue'].apply(
            lambda x: str(x).split(",")[0].replace("'", ""))
        venue_mapping_df['database_venue'] = venue_mapping_df['database_venue'].apply(lambda x: x.upper())

        venue_mapping_df = venue_mapping_df.drop_duplicates()

        venues_df = getPandasFactoryDF(session, GET_VENUE_DETAILS_SQL)[['stadium_name', 'venue_id']]

        players_data_df = getPlayersDataDF(session)

        teams_df = getPandasFactoryDF(session, GET_TEAM_SQL)[['team_id', 'team_short_name', 'team_name']]

        matches_data = getPandasFactoryDF(session, GET_MATCH_SUMMARY)[['match_id', 'src_match_id', 'match_name', 'match_date']]

        final_tournament_df['over_number'] = final_tournament_df['ball'].apply(lambda x: int(str(x).split(".")[0]) + 1)
        final_tournament_df['ball_number'] = final_tournament_df['ball'].apply(lambda x: int(str(x).split(".")[1]))
        # final_tournament_df[['striker', 'non_striker', 'bowler']] = final_tournament_df[
        #     ['striker', 'non_striker', 'bowler']].apply(lambda x: x.replace("'", ""))

        # [['match_id', 'batsman_id', 'innings', 'batting_position', 'bowler_id', 'runs', 'season', 'over_number',
        #                      'is_wide', 'is_no_ball', 'ball_number', 'match_date', 'is_playoff', 'match_name','is_four', 'is_six',
        #                      'competition_name', 'batting_team', 'bat_team_short_name', 'bowling_team', 'bowl_team_short_name',
        #                      'batsman', 'striker_player_type', 'striker_batting_type', 'bowler', 'bowling_type', 'Bowler_type',
        #                      'batsman_team_id', 'bowler_team_id', 'venue_id', 'is_wicket', 'non_striker_id', 'non_striker_name',
        #                      'is_leg_bye', 'pitch_type', 'stadium_name', 'match_date_form']]

        ball_by_ball_sql = '''select cast(ftd.match_id as string) as src_match_id, md.match_name, md.match_id, md.match_date, ftd.season, ftd.innings, 
ftd.over_number, ftd.ball_number, ftd.competition_name, cast(ftd.runs_off_bat+coalesce(ftd.extras,0) as int) as runs,
cast(ftd.ball as string) as over_text, ftd.runs_off_bat as ball_runs, ftd.extras, case when ftd.wides is not null then 1 else 0 end as is_wide, 
case when ftd.noballs is not null then 1 else 0 end as is_no_ball, case when ftd.byes is not null then 1 else 0 end as is_bye,
 case when ftd.legbyes is not null then 1 else 0 end as is_leg_bye, coalesce(ven.venue_id, -1) as venue_id, 
 coalesce(vdf.database_venue, ftd.venue) as stadium_name, coalesce(tdf.team_short_name, 'NA') as bat_team_short_name,
 case when ftd.runs_off_bat=4 then 1 else 0 end as is_four,  case when ftd.runs_off_bat=6 then 1 else 0 end as is_six,
 ftd.batting_team, coalesce(tdf.team_id, -1) as batsman_team_id, coalesce(ftd.wicket_type, 'NA') as wicket_type,
 ftd.bowling_team,  coalesce(tdf2.team_id, -1) as bowler_team_id, coalesce(tdf2.team_short_name, 'NA') as bowl_team_short_name,
 case when ftd.wicket_type is not null then 1 else 0 end as is_wicket, coalesce(pdf1.database, ftd.striker) as batsman, 
 coalesce(pld1.player_id, -1) as batsman_id, pld1.batting_type as striker_batting_type, 
 pld1.player_type as striker_player_type, start_date as match_date_form, 0 as is_playoff,
 coalesce(pdf2.database, ftd.non_striker) as non_striker_name, coalesce(pld2.player_id, -1) as non_striker_id, 
 coalesce(pdf3.database, ftd.bowler) as bowler, coalesce(pld3.player_id, -1) as bowler_id,
 pld3.bowling_type as bowling_type, pld3.player_type as bowler_type, 'TRUE' as pitch_type, 
 coalesce(pld4.player_id, -1) as out_batsman_id,coalesce(pdf4.database, ftd.player_dismissed) as out_batsman 
 from final_tournament_df ftd 
 inner join matches_data md on (md.src_match_id=cast(ftd.match_id as string)) 
  left join players_mapping_df pdf1 on (ftd.striker=pdf1.cricsheet) 
  left join players_mapping_df pdf2 on (ftd.non_striker=pdf2.cricsheet) 
 left join players_mapping_df pdf3 on (ftd.bowler=pdf3.cricsheet)
 left join players_mapping_df pdf4 on (ftd.player_dismissed=pdf4.cricsheet)
 left join players_data_df pld1 on (pld1.player_name=coalesce(pdf1.database, ftd.striker))
 left join players_data_df pld2 on (pld2.player_name= coalesce(pdf2.database, ftd.non_striker))
 left join players_data_df pld3 on (pld3.player_name=coalesce(pdf3.database, ftd.bowler))
  left join players_data_df pld4 on (pld4.player_name=coalesce(pdf4.database, ftd.player_dismissed)) 
  left join venue_mapping_df vdf on (vdf.cricsheet_venue=venue)
 left join venues_df ven on (vdf.database_venue=ven.stadium_name)
 left join teams_df tdf on (tdf.team_name=ftd.batting_team)
left join teams_df tdf2 on (tdf2.team_name=ftd.bowling_team) '''


        ball_by_ball_df = executeQuery(con, ball_by_ball_sql).drop_duplicates()

        ball_by_ball_df['load_timestamp'] = load_timestamp

        ball_by_ball_df['out_batsman'] = ball_by_ball_df['out_batsman'].fillna('NA')

        ball_by_ball_df['batting_position'] = ball_by_ball_df.sort_values(by=['over_number', 'ball_number']) \
            .groupby(['innings', 'match_id']).batsman.transform(lambda x: pd.factorize(x)[0] + 1)

        max_key_val = getMaxId(session, OTHER_TOURNAMENTS_INNINGS_TABLE, OTHER_TOURNAMENTS_INNINGS_KEY_COL, DB_NAME)

        ball_by_ball_df = generateSeq(ball_by_ball_df.where(pd.notnull(ball_by_ball_df), None) \
                                         .sort_values(['match_id', 'innings', 'over_number', 'ball_number']),
                                         OTHER_TOURNAMENTS_INNINGS_KEY_COL,
                                         max_key_val)

        return ball_by_ball_df.to_dict(orient="records")
