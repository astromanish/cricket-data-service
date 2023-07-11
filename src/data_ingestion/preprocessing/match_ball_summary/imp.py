# Getting max match_id from target table
max_key_val = getMaxId(session, INNINGS_TABLE_NAME, INNINGS_KEY_COL, DB_NAME)


for rawdata in innings_raw_data:
    rawdata['competition_name'] = competition_name
    rawdata['season'] = season

    if match_wagon_wheel.empty:
        match_wagon_wheel = pd.DataFrame(columns=['BallID', 'FielderAngle', 'FielderLengthRatio'])
        match_wagon_wheel['BallID'] = match_wagon_wheel['BallID'].fillna('XX')
        match_wagon_wheel['FielderAngle'] = match_wagon_wheel['FielderAngle'].fillna(0)
        match_wagon_wheel['FielderLengthRatio'] = match_wagon_wheel['FielderLengthRatio'].fillna(0)

    innings_df = pd.merge(innings_df, match_wagon_wheel, on='BallID', how='left') \
        .rename(columns={'FielderLengthRatio': 'fielder_length_ratio', 'FielderAngle': 'fielder_angle'}) \
        .drop(['BallID'], axis=1)

    append_innings_df = append_innings_df.append(innings_df, ignore_index=True)
    
#############################################################################

matches_df = getPandasFactoryDF(session, GET_MATCHES_DETAILS_SQL)

append_innings_df = pd.merge(append_innings_df, matches_df[['match_id', 'src_match_id']],
                                left_on=append_innings_df['MatchID'], right_on='src_match_id', how='left') \
    .drop(['MatchID', 'src_match_id'], axis=1)

append_innings_df = append_innings_df.dropna(axis=0, subset=['match_id'])

append_innings_df = append_innings_df[append_innings_df['match_id'].notna()]

players_df = getPandasFactoryDF(session, GET_PLAYER_DETAILS_SQL).drop_duplicates()

# Getting Striker ID
append_innings_df = pd.merge(append_innings_df, players_df[['src_player_id', 'player_id']],
                                left_on=append_innings_df['StrikerID'],
                                right_on=players_df['src_player_id'],
                                how='left') \
    .rename(columns={'player_id': 'batsman_id'}) \
    .drop(['StrikerID', 'key_0', 'src_player_id'], axis=1)

# Getting Non Striker ID
append_innings_df = pd.merge(append_innings_df, players_df[['src_player_id', 'player_id']],
                                left_on=append_innings_df['NonStrikerID'],
                                right_on=players_df['src_player_id'],
                                how='left') \
    .rename(columns={'player_id': 'non_striker_id'}) \
    .drop(['NonStrikerID', 'key_0', 'src_player_id'], axis=1)

append_innings_df = pd.merge(append_innings_df, players_df[['src_player_id', 'player_id']],
                                left_on=append_innings_df['OutBatsManID'],
                                right_on=players_df['src_player_id'],
                                how='left') \
    .rename(columns={'player_id': 'out_batsman_id'}) \
    .drop(['OutBatsManID', 'key_0', 'src_player_id'], axis=1)

append_innings_df = pd.merge(append_innings_df, players_df[['src_player_id', 'player_id']],
                                left_on=append_innings_df['BowlerID'],
                                right_on=players_df['src_player_id'],
                                how='left') \
    .rename(columns={'player_id': 'against_bowler'}) \
    .drop(['BowlerID', 'key_0', 'src_player_id'], axis=1)

bat_card_df = getPandasFactoryDF(session, GET_BAT_CARD_DATA)[['match_id', 'innings', 'batsman_id',
                                                                'batting_team_id', 'batting_position']]

append_innings_df['InningsNo'] = append_innings_df['InningsNo'].astype(int)

append_innings_df = pd.merge(append_innings_df, bat_card_df, how="left",
                                left_on=['match_id', 'InningsNo', 'batsman_id'],
                                right_on=['match_id', 'innings', 'batsman_id'])\
    .rename(columns={'batting_team_id': 'batsman_team_id'}).drop(['InningsNo'], axis=1)

bowl_card_df = getPandasFactoryDF(session, GET_BOWL_CARD_DATA)[['match_id', 'innings', 'bowler_id', 'team_id']]

append_innings_df = pd.merge(append_innings_df, bowl_card_df, how="left",
                                left_on=['match_id', 'innings', 'against_bowler'],
                                right_on=['match_id', 'innings', 'bowler_id'])\
    .rename(columns={'team_id': 'bowler_team_id'}).drop(['bowler_id'], axis=1)

append_innings_df['over_number'] = append_innings_df['OverNo'].astype(int)
# conditions for batting phases
phase_conditions = [
    (append_innings_df['over_number'] <= 6),
    (append_innings_df['over_number'] > 6) & (append_innings_df['over_number'] <= 10),
    (append_innings_df['over_number'] > 10) & (append_innings_df['over_number'] <= 15),
    (append_innings_df['over_number'] > 15)
]

# different batting phases
phase_values = [1, 2, 3, 4]

# create batting_phase column
append_innings_df['batting_phase'] = np.select(phase_conditions, phase_values)

append_innings_df['over_text'] = append_innings_df['CommentOver'].str.split(" ").map(lambda x: x[1])

append_innings_df['Runs'] = append_innings_df['Runs'].apply(lambda x: x.split(" ")[0])
append_innings_df['BallRuns'] = append_innings_df['BallRuns'].fillna(0).astype(int)

append_innings_df = append_innings_df.rename(
    columns={'BallNo': 'ball_number', 'Runs': 'runs',
                'IsOne': 'is_one', 'IsTwo': 'is_two', 'IsThree': 'is_three',
                'IsDotball': 'is_dot_ball', 'Extras': 'extras', 'BallRuns': 'ball_runs',
                'IsExtra': 'is_extra', 'IsWide': 'is_wide', 'BowlingDirection': 'bowling_direction',
                'IsNoBall': 'is_no_ball', 'IsBye': 'is_bye', 'IsUncomfortable': 'is_uncomfortable',
                'IsLegBye': 'is_leg_bye', 'IsFour': 'is_four', 'IsBeaten': 'is_beaten',
                'IsSix': 'is_six', 'IsWicket': 'is_wicket', 'VideoFile' : 'video_file',
                'WicketType': 'wicket_type', 'IsBowlerWicket': 'is_bowler_wicket',
                'Xpitch': 'x_pitch', 'Ypitch': 'y_pitch', 'IsMaiden': 'is_maiden',
                'BowlType': 'bowl_type', 'Line': 'bowl_line',
                'ShotType': 'shot_type', 'Length': 'bowl_length'}) \
    .drop(['OverNo', 'CommentOver'], axis=1)

append_innings_df[['against_bowler', 'batsman_id', 'match_id', 'out_batsman_id']] = append_innings_df[
    ['against_bowler', 'batsman_id', 'match_id', 'out_batsman_id']].fillna(-1).astype(int)
append_innings_df[['wicket_type', 'bowl_type', 'shot_type', 'bowl_line', 'bowl_length', 'video_file']] = append_innings_df[
    ['wicket_type', 'bowl_type', 'shot_type', 'bowl_line', 'bowl_length', 'video_file']].fillna("NA")  # .astype(int)
append_innings_df[['x_pitch', 'y_pitch', 'fielder_length_ratio', 'fielder_angle']] = \
    append_innings_df[['x_pitch', 'y_pitch', 'fielder_length_ratio', 'fielder_angle']].fillna(0)
append_innings_df['bowling_direction'] = append_innings_df['bowling_direction'].fillna("NA")
append_innings_df['is_bye'] = append_innings_df['is_bye'].apply(lambda x: 1 if x == 'True' else 0)
append_innings_df['is_leg_bye'] = append_innings_df['is_leg_bye'].apply(lambda x: 1 if x == 'True' else 0)
append_innings_df['is_wide'] = append_innings_df['is_wide'].apply(lambda x: 1 if x == 'True' else 0)
append_innings_df['is_no_ball'] = append_innings_df['is_no_ball'].apply(lambda x: 1 if x == 'True' else 0)
append_innings_df['is_four'] = append_innings_df['is_four'].apply(lambda x: 1 if x == 'True' else 0)
append_innings_df['is_six'] = append_innings_df['is_six'].apply(lambda x: 1 if x == 'True' else 0)
append_innings_df['is_beaten'] = append_innings_df['is_beaten'].apply(lambda x: 1 if x == 'True' else 0)
append_innings_df['is_uncomfortable'] = append_innings_df['is_uncomfortable'].apply(
    lambda x: 1 if x == 'True' else 0)

append_innings_df['bowl_line'] = np.where(append_innings_df['bowl_line'] == 'Middle', 'Middle Stump',
                                            append_innings_df['bowl_line'])

append_innings_df['bowl_length'] = np.where(append_innings_df['bowl_length'] == 'Short Of Good Length',
                                            'Good Length', append_innings_df['bowl_length'])

append_innings_df['load_timestamp'] = load_timestamp

final_innings_data = generateSeq(append_innings_df.where(pd.notnull(append_innings_df), None) \
                                    .sort_values(['match_id', 'innings', 'over_number', 'ball_number']),
                                    INNINGS_KEY_COL,
                                    max_key_val) \
    .to_dict(orient='records')

return final_innings_data