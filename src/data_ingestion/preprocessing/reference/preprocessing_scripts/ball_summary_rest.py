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
