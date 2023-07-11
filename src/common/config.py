import os

HOME_DIR = ''
# below mentioned paths are for DEV purpose only, for prod, paths are being passed through run.sh
ROOT_DATA_PATH = os.path.join(HOME_DIR, "data/Data_Feeds/")
IPL_2022_PATH = os.path.join(ROOT_DATA_PATH, 'IPL/IPL 2022/')
SQUAD_ROOT_PATH = os.path.join(HOME_DIR, "data/Squad_Feeds/")
PITCH_TYPE_DATA_PATH = os.path.join(HOME_DIR, "data/IPL-NATURE_OF_WICKETS.xlsx")
DAILY_ACTIVITY_EXCEL_DATA_PATH = os.path.join(HOME_DIR, "data/Daily_Activity.xlsx")
PITCH_TYPE_2019_TO_2021_DATA_PATH = os.path.join(HOME_DIR, "data/2019_2020_2021_matches-wicket-type.csv")
CONTRIBUTION_CONSTRAINTS_DATA_PATH = os.path.join(HOME_DIR, "data/Contribution_Constraints.csv")
MISSING_SQUAD_2022 = os.path.join(HOME_DIR, 'data/Squad_missing.xlsx')
MISSING_PLAYERS_2022 = os.path.join(HOME_DIR, 'data/missing_players-2022.xlsx')
OTHER_MATCHES_DATA = os.path.join(HOME_DIR, 'data/all_other_data_final.xlsx')
FITNESS_DATA = os.path.join(HOME_DIR, 'data/fitness_data.csv')
BOWLING_PLANNING_TEMPLATE = os.path.join(HOME_DIR, 'data/bowling-planning-template.xlsx')
CONTRIBUTION_SCORE_TABLE_NAME = 'contributionScore'
FTP_PATH = "MI2022"
IMAGE_STORE_URL = ''
OTHER_TOURNAMENTS_DATA_PATH = os.path.join(HOME_DIR, "data/other-tournaments-data/")
OTHER_TOURNAMENTS_MAPPING_FILE = os.path.join(HOME_DIR, "data/mapping-sheet-other-tournaments.xlsx")
PLAYER_LIST_2023_FILE = os.path.join(HOME_DIR, "data/player_list_2023.csv")
IPL_2023_PATH = os.path.join(ROOT_DATA_PATH, 'IPL/IPL 2023/')
FIELDING_ANALYSIS_FILE = os.path.join(HOME_DIR, "data/field-analysis-template.csv")
# FILE METADATA
FILES_KEY_COL = "file_id"
FILES_TABLE = "fileLogs"

# Players configs
SQUAD_KEY_LIST = ['squadA', 'squadB']
PLAYERS_TABLE_NAME = 'players'
PLAYERS_KEY_COL = 'player_id'
PLAYERS_REQD_COLS = {"TeamID", "PlayerName", "PlayerID", "BattingType", "BowlingProficiency", "PlayerSkill",
                     "IsCaptain",
                     "season", "competition_name", "TeamName"}

# Teams configs
TEAMS_TABLE_NAME = 'Teams'
TEAMS_KEY_COL = 'team_id'
TEAMS_KEYS_FROM_SQUAD = {'TeamID', 'TeamName', 'TeamCode'}

# Venue Configs
VENUE_TABLE_NAME = 'Venue'
VENUE_KEY_COL = 'venue_id'

# Matches Configs
MATCHES_KEY_COL = 'match_id'
MATCHES_TABLE_NAME = 'Matches'
MATCHES_REQD_COLS = ["MatchID", "MatchDate", "MatchTime", "FirstBattingTeamID", "MatchDateOrder", "MatchName", \
                     "FirstBattingTeamName", "SecondBattingTeamID", "SecondBattingTeamName", \
                     "GroundName", "Comments", "TossTeam", "TossDetails", "FirstBattingSummary", \
                     "SecondBattingSummary", "competition_name", "seasons"]

# Innings configs

INNINGS_REQD_COLS = 'BallID', 'MatchID', 'InningsNo', 'StrikerID', 'BowlerID', 'OutBatsManID', \
                    'OverNo', 'BallNo', 'Runs', 'IsOne', 'IsTwo', 'IsThree', 'IsDotball', 'Extras', 'IsExtra', \
                    'IsWide', 'IsNoBall', 'IsBye', 'IsLegBye', 'IsFour', 'IsSix', 'IsWicket', 'WicketType', \
                    'IsBowlerWicket', 'Xpitch', 'Ypitch', 'IsMaiden', 'Line', 'BowlType', 'Length', \
                    'ShotType', 'CommentOver', 'BallRuns', 'competition_name', 'season', 'NonStrikerID', 'IsBeaten', \
                    'IsUncomfortable', 'BowlingDirection', 'VideoFile'

WAGONWHEEL_REQD_COLS = 'BallID', 'FielderAngle', 'FielderLengthRatio', 'FielderLengthRation'
BATTING_REQD_COLS = 'PlayerID', 'PlayingOrder', 'TeamID'
BOWLING_REQD_COLS = 'PlayerID', 'TeamID'
INNINGS_KEY_COL = 'id'
INNINGS_TABLE_NAME = 'MatchBallSummary'

OTHER_TOURNAMENTS_INNINGS_TABLE = "OtherMatchesBallSummary"
OTHER_TOURNAMENTS_INNINGS_KEY_COL = 'id'

# Extras required columns

EXTRAS_REQD_COLS = 'MatchID', 'InningsNo', 'TeamID', 'TotalExtras', 'Byes', 'LegByes', 'NoBalls', 'Wides'
EXTRAS_KEY_COL = 'id'
EXTRAS_TABLE_NAME = "MatchExtras"
