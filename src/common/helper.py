from pathlib import Path
from tabulate import tabulate
import pandas as pd
import re
from environs import Env
import os

from common.utils.helper import pandas_factory
from log.log import get_logger

logger = get_logger("Ingestion", "Ingestion")


#################################  Data Access Object ############################

# This function takes in DB session and select statement
# and generates the DF of rows using pandas_factory function
def getPandasFactoryDF(session, select_sql):
    # Getting teams DF from db table using pandas_factory
    session.row_factory = pandas_factory
    session.default_fetch_size = None
    res = session.execute(select_sql, timeout=None)
    return res._current_rows


# This function fetches the max primary key value from the input DB table
def getMaxId(session, table_name, id_col, db_name):
    select_sql = "SELECT max({}) as max FROM {}.{};".format(id_col, db_name, table_name)
    rows = getPandasFactoryDF(session, select_sql)
    if rows["max"].iloc[0] is None:
        logger.info("Max id for table={} is 1".format(table_name))
        return 1
    else:
        max_val = rows["max"].iloc[0] + 1
        logger.info("Max id for table={} is {}".format(table_name, max_val))
        return max_val


# this function takes input as db session and SQL select statement
# and returns the data list of the selected column
def getAlreadyExistingValue(session, select_sql):
    rows = getPandasFactoryDF(session, select_sql)
    data_list = [row for row in rows.iloc[:, 0]]
    return data_list

import json

from cassandra.concurrent import execute_concurrent

from log.log import get_logger

logger = get_logger("Ingestion", "Ingestion")


# This function takes in session and data as input and insert the records to the provided db and table
def insertToDB(session, data_list, db_name, table_name):
    statements_and_params = []
    for jData in data_list:
        insert_stmt = "insert into {}.{} JSON \'{}\';".format(db_name, table_name, json.dumps(jData))
        statements_and_params.append((insert_stmt, ()))
    logger.info("Insert Started for --> {}".format(table_name))
    execute_concurrent(session, statements_and_params, concurrency=50)
    logger.info("Insert Completed for --> {}".format(table_name))


# this function deletes the records, taking input as list of data
def upsertDatatoDB(session, data_list, db_name, table_name, key_col):
    if data_list:
        key_li = tuple(d[key_col] for d in data_list)
        if len(key_li) > 1:
            key_li = str(key_li)
            clause = f"where {key_col} in {key_li}"
        else:
            key_li = key_li[0]
            clause = f"where {key_col} = {key_li}"
        logger.info("Delete Started for --> {}".format(table_name))
        delete_stmt = f"delete from {db_name}.{table_name} {clause};"
        logger.info("Delete Statement --> {}".format(delete_stmt))
        session.execute(delete_stmt)
        logger.info("Delete Completed for --> {}".format(table_name))

        # after deleting updated records, inserting the latest records
        insertToDB(session, data_list, db_name, table_name)


# this function truncates the given table
def truncateTable(session, db_name, table_name):
    logger.info("Truncate started for --> {}.{}".format(db_name, table_name))
    truncate_stmt = "truncate table {}.{}".format(db_name, table_name)
    session.execute(truncate_stmt)
    logger.info("Truncate completed for --> {}.{}".format(db_name, table_name))
    
################################# Common Utils Functions ##################################


# get project root
def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def print_df(df):
    return tabulate(df, headers='keys', tablefmt='psql')



# get integer from the input string
def getIntFromString(x: str):
    return int(re.search(r'\d+', x).group())


# function to get environment variables
def get_env_variable(key):
    env = Env()
    env.read_env()
    return os.environ.get(key)


def getTeamsMapping():
    team_dict = {
        "MI" : "Mumbai Indians",
        "MICT" : "MI Capetown",
        "MIE" : "MI Emirates",
        "MINY" : "MI New York"
    }
    return team_dict


############################ Data Ingestion Utils Functions ######################

import json
import numpy as np
import pandas as pd
from os.path import isfile, join
from os import listdir
from common.dao.fetch_db_data import getPandasFactoryDF
import base64
import io
import csv

# Reads .js file and return json data as output



def readJsFile(filePath):
    with open(filePath) as dataFile:
        data = dataFile.read()
        obj = data[data.find('{'): data.rfind('}') + 1]
        jsonObj = json.loads(obj)
        return jsonObj


# reads csv file from the given input path and returns DF
def readCSV(path):
    df = pd.read_csv(path)
    return df


# reads excel file from the given input path and returns DF
def readExcel(path, sheet):
    df = pd.read_excel(path, engine='openpyxl', sheet_name=sheet)
    return df


# takes in dataframe, surrogate key column_name and last available max_val from the db as input and
# generates and add a sequence of numbers to the returned DF
def generateSeq(df, col_name, max_val):
    df.insert(0, col_name, range(max_val, max_val + len(df)))
    return df


# This function takes in dictionary and renames the dictionary old key(s) as per new key(s)
def renameDictKey(dictionary, new_name, old_name):
    dictionary[new_name] = dictionary.pop(old_name)
    return dictionary


# This function takes in list of jsons as input and returns the dataframe
def dataToDF(li, col_list=None):
    return pd.DataFrame(li, columns=col_list)


# This function reads data from the provided root path and returns the dictionary of files
# where key is the file name and value is the absolute path
# def getFiles(basePath):
#     files = {fname: join(basePath, fname) for fname in listdir(basePath) if isfile(join(basePath, fname))}
#     return files
def getFiles(basePath):
    file_dict = {}
    for basefold in listdir(basePath):
        if basefold != ".DS_Store":
            if basefold != "MI2022":
                for foldname in listdir(basePath + basefold):
                    if foldname != ".DS_Store":
                        files = {fname: join(basePath + basefold + '/' + foldname, fname)
                                 for fname in listdir(basePath + basefold + '/' + foldname)
                                 if isfile(join(basePath + basefold + '/' + foldname, fname))}
                        file_dict.update(files)
    return file_dict


# Takes in input as df and data_list and
# exclude the records based on key_name from the df which are available of data_list
def excludeAlreadyExistingRecords(df, key_name, data_list):
    return df[~df[key_name].str.strip().str.replace(" ", "").str.lower()
        .isin([str(x).strip().replace(" ", "").lower() for x in data_list])]


# generates a file name based on the provided input
def getSpecificFileKey(id_key, text_name, file_format):
    return id_key + '-' + text_name.strip().lower() + '.' + file_format.strip().lower()


# returns list of dicts with specific columns
def getRawDict(data_dict_list, reqd_cols):
    li = []
    for data_dict in data_dict_list:
        if 'FielderLengthRation' in data_dict:
            data_dict["FielderLengthRatio"] = data_dict.pop("FielderLengthRation")
        dicts = {key: str(data_dict[key]).split('(')[0].strip() for key in data_dict.keys()
                 & reqd_cols}
        li.append(dicts)
    return li


# gets dataframe out of matchSchedule.js files
def getMatchScheduleData(paths_set):
    data_li = []

    for path in paths_set:
        season = path.split("/")[-2].split(" ")[1]
        competition_name = path.split("/")[-3]
        for data in readJsFile(path)['Result']:
            data["competition_name"] = competition_name
            data["seasons"] = int(season)
            data_li.append(data)
    df = pd.DataFrame(data_li)
    return df


# gets dataframe out of squad.js files
# base_path = root path of the squad files
# squad_key_list = ["squadA", "squadB"] keys from squad files
# key_dict = dictionary of keys to be selected specifically
def getSquadRawData(base_files, squad_key_list, key_dict):
    path_set = set(value for key, value in base_files.items()
                   if (key != ".DS_Store") if ('squad' in key.split("-")[1].split(".")[0].strip().lower()))
    squad_list = []
    for path in path_set:
        # getting data from players js file
        season = path.split("/")[-3].split(" ")[1]
        competition_name = path.split("/")[-3].split(" ")[0]
        match_id = path.split("/")[-1].split("-")[0]
        squad_data = readJsFile(path)

        for squad in squad_key_list:
            for data in squad_data[squad]:
                squad_dict = {key: str(data[key]).split('(')[0].strip() for key in data.keys()
                              & key_dict}
                squad_dict["season"] = season
                squad_dict["competition_name"] = competition_name
                squad_dict["src_match_id"] = match_id
                squad_list.append(squad_dict)
    raw_squad_df = dataToDF(squad_list)
    return raw_squad_df


# function to generate is_playoff flag
def checkPlayoff(li):
    if li in [1, 2, 3, 4]:
        return 1
    else:
        return 0


# function to generate is_title flag
def checkTitle(li):
    if li == 1:
        return 1
    else:
        return 0


# generated random string hash value
def random_string_generator(x):
    import hashlib
    val = hashlib.md5(bytes(x.encode('utf-8'))).hexdigest()
    return val


# function to get string before word WON
def getListTill(li):
    ele_li = [ele.lower().replace("`", "").replace("wn", "won").replace("win", "won").replace("wony", "won") for ele in li]
    if len(ele_li) > 4:
        return [li[i] for i in range(0, len(ele_li)) if i < ele_li.index('won')]


# function to get initials of the provided string
def getInitials(s):
    return "".join([st[0] for st in s.split(" ")] if len(s.split(" "))>1 else s[0:4])


# Get Nature of wicket (pitch type) data
def getPitchTypeData(data_path):
    pitch_df = pd.DataFrame()
    xls = pd.ExcelFile(data_path, engine='openpyxl')
    sheet_names = xls.sheet_names
    for sheet in sheet_names:
        pitch_df = pitch_df.append(readExcel(data_path, sheet))
    pitch_df = pitch_df.rename(columns={"MATCH ID": "match_id", "NATURE OF THE WICKET": "nature_of_wicket",
                                        "OVERALL NATURE": "overall_nature", "DEW": "dew"})

    return pitch_df[["match_id", "nature_of_wicket", "overall_nature", "dew"]]


# this function returns the latest files to process in the folder excluding already loaded files
def getLatestFiles(loaded_files_list, src_files_list):
    src_files = src_files_list.copy()
    for file_name in src_files_list.keys():
        if file_name in loaded_files_list:
            src_files.pop(file_name, None)
    return src_files


# function to split the path and get season
def splitString(s):
    path_li = s.split("/")
    if "Squad_Feeds" in path_li:
        return path_li[-3].split(" ")[1]
    elif "Data_Feeds" in path_li:
        return path_li[-2].split(" ")[1]


# generated list of latest files to be loaded
def logFilesIntoDB(files_key_col, latest_files, max_id, load_timestamp):
    file_df = pd.DataFrame.from_dict(latest_files, orient='index', columns=["file_path"])
    file_df["file_name"] = file_df.index
    file_df["load_timestamp"] = load_timestamp
    file_df["competition_name"] = file_df["file_path"].apply(lambda x: x.split("/")[-3].split(" ")[0])
    file_df["season"] = file_df["file_path"].apply(splitString)
    files_loaded = generateSeq(file_df.reset_index(drop=True), files_key_col, max_id).to_dict(orient='records')
    return files_loaded


# convert tuple to dict
def convertTupToDict(tup):
    di = dict(tup)
    return di


# get lines count
def file_len(filename):
    with open(filename) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1


# function to add column in case the column is missing
def columnCheck(df, colList):

    df.columns = df.columns = [x for x in df.columns]
    for scol in colList:
        if scol not in df.columns:
            df[scol] = np.NAN
    return df


# function to get other tournament files
def getOtherTournamentFiles(basePath):
    file_dict = {}
    files = {}
    for basefold in listdir(basePath):
        if basefold != ".DS_Store":
            if basefold != "MI2022":
                files = {basefold: join(basePath + basefold)}
                file_dict.update(files)
    return file_dict


# get other tournaments df
def getOtherTournamentsDF(OTHER_DATA_FILES):
    final_tournament_df = pd.DataFrame()

    if len(OTHER_DATA_FILES) != 0:
        for fname, file in OTHER_DATA_FILES.items():
            tournament_df = readCSV(file)
            tournament_df['competition_name'] = fname.split('.')[0].split('-')[1].replace("_", " ").upper()
            tournament_df['season'] = tournament_df['season'].apply(lambda x: int(str(x).split('/')[0]))
            tournament_df = tournament_df[tournament_df['season'] >= 2018]
            tournament_df['striker'] = tournament_df['striker'].apply(lambda x: str(x).replace("'", ""))
            tournament_df['bowler'] = tournament_df['bowler'].apply(lambda x: str(x).replace("'", ""))
            tournament_df['non_striker'] = tournament_df['non_striker'].apply(lambda x: str(x).replace("'", ""))
            tournament_df['player_dismissed'] = tournament_df['player_dismissed'].apply(lambda x: str(x).replace("'", "")).fillna("NA")
            tournament_df['venue'] = tournament_df['venue'].apply(lambda x: str(x).replace("'", ""))
            final_tournament_df = final_tournament_df.append(tournament_df, ignore_index=True)

    return final_tournament_df


def getPlayersDataDF(session):
    GET_PLAYERS_DATA = '''select src_player_id, player_id, player_name, batting_type, bowling_type, player_skill,
        is_captain, is_batsman, is_bowler, is_wicket_keeper, player_type, bowl_major_type, player_image_url, season  
         from CricketSimulatorDB.Players; '''
    players_data_df = getPandasFactoryDF(session, GET_PLAYERS_DATA)

    if not players_data_df.empty:

        players_data_df["player_rank"] = players_data_df.groupby("player_id")["season"].rank(method="first",
                                                                                             ascending=False)
        players_data_df = players_data_df[players_data_df["player_rank"] == 1].drop(['player_rank', 'season'], axis=1)

        return players_data_df

    else:
        return pd.DataFrame()


# generate DF for match playing XI
def getMatchesSquadDF(session, team_squad_striker, team_squad_nonstriker, team_squad_bowler, players_mapping_df):
    team_squad = team_squad_striker.append(team_squad_nonstriker, ignore_index=True).append(team_squad_bowler,
                                                                                            ignore_index=True).drop_duplicates()
    team_squad['player_name'] = team_squad['player_name'].apply(lambda x: x.replace("'", ""))

    team_squad = team_squad.merge(players_mapping_df.drop_duplicates(), left_on='player_name',
                                  right_on='cricsheet', how='left')

    team_squad['database'] = np.where(team_squad['database'].isnull(), team_squad['player_name'],
                                      team_squad['database'])

    team_squad = team_squad.drop(['player_name', 'cricsheet'], axis=1).rename(columns={'database': 'player_name'})

    players_data_df = getPlayersDataDF(session)[['player_name', 'player_id']]

    team_squad = team_squad.merge(players_data_df, on='player_name', how='left')

    team_squad = team_squad.groupby(['src_match_id', 'team_name'])['player_id'].agg(list).reset_index()

    return team_squad

def decodeReadCSV(encode_csv):
    decrypted = base64.b64decode(encode_csv).decode('utf-8')
    with io.StringIO(decrypted) as fp:
        reader = pd.read_csv(fp)
    return reader

def encodeCSV(csv_file):
    csv_list = list()
    file = open(csv_file, mode='r')
    for row in csv.reader(file):
        csv_list.extend(row)
    csv_string = ', '.join(csv_list)
    encrypted = base64.b64encode(csv_string.encode())
    return encrypted