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


def getVenueData(session, root_data_files, other_data_files, mapping_sheet_path, load_timestamp):
    if root_data_files or other_data_files:
        if root_data_files:
            path_set = set(value for key, value in root_data_files.items()
                        if 'matchschedule' in key.split("-")[1].split(".")[0].strip().lower())

            data_li = []
            for path in path_set:
                for data in readJsFile(path)['Result']:
                    data_li.append(data)

            venues_df = pd.DataFrame(data_li)[["GroundID", "GroundName"]].drop_duplicates().reset_index()\
                .rename(columns={"GroundID": "src_venue_id", "GroundName": "stadium_name"}).drop("index", axis=1)
                
            other_venues_df = getOtherVenues(mapping_sheet_path)
            venues_df = venues_df.append(other_venues_df, ignore_index=True)
        else:
            other_venues_df = getOtherVenues(mapping_sheet_path)
            venues_df = other_venues_df

        venues_df['stadium_name'] = venues_df['stadium_name'].apply(lambda x: x.upper())

        venues_df['load_timestamp'] = load_timestamp

        venues_df = venues_df.drop_duplicates(subset='stadium_name', keep='first')
        # Fetching name of the players already exists in the db table
        venues_list = getAlreadyExistingValue(session, GET_VENUE_DETAILS_SQL)

        # Excluding the records already present in the DB table
        venues_df = excludeAlreadyExistingRecords(venues_df, 'stadium_name', venues_list)
        # Fetching max primary key value
        max_key_val = getMaxId(session, VENUE_TABLE_NAME, VENUE_KEY_COL, DB_NAME)

        # Generating and adding the sequence to the primary key and converting it to dictionary
        venue_final_data = generateSeq(venues_df, VENUE_KEY_COL, max_key_val).to_dict(orient='records')
        return venue_final_data

    else:


# if __name__=="__main__":
#     import datetime
#     loaded_files = getAlreadyExistingValue(session, GET_EXISTING_FILES)
#     root_data_files = getLatestFiles(loaded_files, getFiles(ROOT_DATA_PATH))
#     load_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     venue_data = getVenueData(session, root_data_files, OTHER_TOURNAMENTS_MAPPING_FILE, load_timestamp)
#     if venue_data:
#         # venue data insert
#         insertToDB(session, venue_data, DB_NAME, VENUE_TABLE_NAME)
