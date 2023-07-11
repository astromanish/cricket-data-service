import sys
sys.path.append("./../../")
sys.path.append("./")
import pandas as pd
from datetime import datetime
import numpy as np


from DataIngestion.config import MATCHES_TABLE_NAME, MATCHES_KEY_COL, MATCHES_REQD_COLS, SQUAD_KEY_LIST
from common.dao.fetch_db_data import getPandasFactoryDF, getMaxId
from DataIngestion.query import GET_TEAM_SQL, GET_EXISTING_MATCHES_SQL
from DataIngestion.utils.helper import readJsFile, dataToDF, generateSeq, getSquadRawData, checkPlayoff, \
    checkTitle, getListTill, getPitchTypeData, getMatchScheduleData, readCSV, getMatchesSquadDF, readExcel, getInitials, \
    getOtherTournamentsDF
from DataIngestion.query import (GET_PLAYER_DETAILS_SQL, GET_VENUE_DETAILS_SQL)
from common.db_config import DB_NAME
import pandasql as psql


pd.options.mode.chained_assignment = None






        

# if __name__=="__main__":
#
#     load_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     loaded_files = getAlreadyExistingValue(session, GET_EXISTING_FILES)
#     root_data_files = getLatestFiles(loaded_files, getFiles(ROOT_DATA_PATH))
#     other_tournament_data_files = getLatestFiles(loaded_files, getOtherTournamentFiles(OTHER_TOURNAMENTS_DATA_PATH))
#     squad_data_files = getLatestFiles(loaded_files, getFiles(SQUAD_ROOT_PATH))
#     matches_data = getMatchesData(session, root_data_files, squad_data_files, PITCH_TYPE_DATA_PATH, load_timestamp, PITCH_TYPE_2019_TO_2021_DATA_PATH)
#
#     # print(getPrettyDF(matches_data[matches_data['venue'].isnull()].head(100)))
#     if matches_data:
#         # matches data insert
#         insertToDB(session, matches_data, DB_NAME, MATCHES_TABLE_NAME)
#
#     other_matches_data = getOtherMatchesData(other_tournament_data_files, session, OTHER_TOURNAMENTS_MAPPING_FILE,
#                                              load_timestamp)
#     if other_matches_data:
#         # matches data insert
#         insertToDB(session, other_matches_data, DB_NAME, MATCHES_TABLE_NAME)