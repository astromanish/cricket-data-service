import pandas as pd
import numpy as np
import sys
sys.path.append("./../../")
sys.path.append("./")

from DataService.utils.helper import executeQuery, createCon
from DataIngestion.config import INNINGS_REQD_COLS, WAGONWHEEL_REQD_COLS, \
    INNINGS_KEY_COL, INNINGS_TABLE_NAME, OTHER_TOURNAMENTS_INNINGS_TABLE, OTHER_TOURNAMENTS_INNINGS_KEY_COL
from common.dao.fetch_db_data import getPandasFactoryDF, getMaxId
from DataIngestion.query import GET_MATCHES_DETAILS_SQL, GET_PLAYER_DETAILS_SQL, GET_BAT_CARD_DATA, \
    GET_BOWL_CARD_DATA, GET_VENUE_DETAILS_SQL, GET_TEAM_SQL, GET_MATCH_SUMMARY
from DataIngestion.utils.helper import readJsFile, dataToDF, generateSeq, getRawDict, getOtherTournamentsDF, readExcel, \
    getPlayersDataDF
from common.db_config import DB_NAME



def getMatchBallSummaryData(session, root_data_files, load_timestamp):
    if root_data_files:
        # Getting max match_id from target table
        max_key_val = getMaxId(session, INNINGS_TABLE_NAME, INNINGS_KEY_COL, DB_NAME)

        # Initializing empty DF
        append_innings_df = pd.DataFrame()

        path_set = set((key.split("-")[1].split(".")[0].strip(), value) for key, value in root_data_files.items()
                       if 'innings' in key.split("-")[1].split(".")[0].strip().lower())

        for tupes in path_set:
            path_key = tupes[0]
            data_path = tupes[1]

            competition_name = data_path.split("/")[-3].split(" ")[0]
            season = data_path.split("/")[-2].split(" ")[1]

            innings_raw_data = readJsFile(data_path)[path_key]['OverHistory']

            for rawdata in innings_raw_data:
                rawdata['competition_name'] = competition_name
                rawdata['season'] = season

            innings_list = getRawDict(innings_raw_data, INNINGS_REQD_COLS)

            innings_df = dataToDF(innings_list)

            wagonwheel_raw_data = readJsFile(data_path)[path_key]['WagonWheel']
            wagonwheel_list = getRawDict(wagonwheel_raw_data, WAGONWHEEL_REQD_COLS)
            wagonwheel_df = dataToDF(wagonwheel_list)

            if wagonwheel_df.empty:
                wagonwheel_df = pd.DataFrame(columns=['BallID', 'FielderAngle', 'FielderLengthRatio'])
                wagonwheel_df['BallID'] = wagonwheel_df['BallID'].fillna('XX')
                wagonwheel_df['FielderAngle'] = wagonwheel_df['FielderAngle'].fillna(0)
                wagonwheel_df['FielderLengthRatio'] = wagonwheel_df['FielderLengthRatio'].fillna(0)

            innings_df = pd.merge(innings_df, wagonwheel_df, on='BallID', how='left') \
                .rename(columns={'FielderLengthRatio': 'fielder_length_ratio', 'FielderAngle': 'fielder_angle'}) \
                .drop(['BallID'], axis=1)

            append_innings_df = append_innings_df.append(innings_df, ignore_index=True)

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
    else:


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

    else:


# if __name__=="__main__":
#     import datetime
#     load_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     loaded_files = getAlreadyExistingValue(session, GET_EXISTING_FILES)
#     root_data_files = getLatestFiles(loaded_files, getFiles(ROOT_DATA_PATH))
#     other_tournament_data_files = getLatestFiles(loaded_files, getOtherTournamentFiles(OTHER_TOURNAMENTS_DATA_PATH))
#     squad_data_files = getLatestFiles(loaded_files, getFiles(SQUAD_ROOT_PATH))
#
#     other_matches_ball_summary_data = getOtherMatchesBallSummary(session, other_tournament_data_files, OTHER_TOURNAMENTS_MAPPING_FILE, load_timestamp)
#     # print(getPrettyDF(ball_summary_data))
#     if other_matches_ball_summary_data:
#         # match ball summary data insert
#         insertToDB(session, other_matches_ball_summary_data, DB_NAME, OTHER_TOURNAMENTS_INNINGS_TABLE)
#
