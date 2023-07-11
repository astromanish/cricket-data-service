import sys
sys.path.append("./../../")
sys.path.append("./")
import pandas as pd
import numpy as np

from common.dao.fetch_db_data import getMaxId, getAlreadyExistingValue
from DataIngestion.query import GET_VENUE_DETAILS_SQL
from common.db_config import DB_NAME
from DataIngestion.utils.helper import readJsFile, excludeAlreadyExistingRecords, generateSeq, readExcel, \
    random_string_generator
from DataIngestion.config import (VENUE_TABLE_NAME, VENUE_KEY_COL)




def getOtherVenues(mapping_sheet_path):
    venue_mapping_df = readExcel(mapping_sheet_path, "venue")

    venue_mapping_df['database_venue'] = np.where(venue_mapping_df['database_venue'].isnull(),
                                                  venue_mapping_df['cricsheet_venue'],
                                                  venue_mapping_df['database_venue'])

    venue_mapping_df['database_venue'] = venue_mapping_df['database_venue'].apply(
        lambda x: str(x).split(",")[0].replace("'", ""))

    venue_mapping_df['src_venue_id'] = venue_mapping_df['database_venue'].apply(lambda x: random_string_generator(x))

    return venue_mapping_df.rename(columns={'database_venue': 'stadium_name'})[['src_venue_id', 'stadium_name']]



# if __name__=="__main__":
#     import datetime
#     loaded_files = getAlreadyExistingValue(session, GET_EXISTING_FILES)
#     root_data_files = getLatestFiles(loaded_files, getFiles(ROOT_DATA_PATH))
#     load_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     venue_data = getVenueData(session, root_data_files, OTHER_TOURNAMENTS_MAPPING_FILE, load_timestamp)
#     if venue_data:
#         # venue data insert
#         insertToDB(session, venue_data, DB_NAME, VENUE_TABLE_NAME)
