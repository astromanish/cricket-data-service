# packages
from datetime import datetime
import os
import pandas as pd
from pathlib import Path
import concurrent.futures
import json
import warnings
import inflection

def read_and_parse_file(file_path, start_index, end_index):
    with open(file_path, "r") as file:
        js_object = file.read()
    data = js_object.strip()[start_index:-end_index]
    json_data = json.loads(data)
    return json_data


def read_json_files(folder_path, data_type, start_index, end_index):
    json_data_list = []
    file_paths = list(Path(folder_path).rglob(f"*{data_type}.js"))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(
            read_and_parse_file, path, start_index, end_index) for path in file_paths]

        for future in concurrent.futures.as_completed(futures):
            json_data = future.result()
            json_data_list.append(json_data)

    return json_data_list


def read_csv_files(folder_path):
    dataframes = []
    file_paths = list(Path(folder_path).rglob("*.csv"))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(pd.read_csv, path, dtype={'column20': str, 'column21': str}) for path in file_paths]

        for future in concurrent.futures.as_completed(futures):
            df = future.result()
            dataframes.append(df)

    final_dataframe = pd.concat(dataframes, ignore_index=True)
    return final_dataframe


def combine_squad_data(json_list):
    comined_json_list = []

    for json_obj in json_list:
        squad_a = json_obj.get("squadA", [])
        squad_b = json_obj.get("squadB", [])

        divided_json_1 = {"squad": squad_a}
        divided_json_2 = {"squad": squad_b}

        comined_json_list.append(divided_json_1)
        comined_json_list.append(divided_json_2)

    return comined_json_list


def combine_innings_data(innings_1_json_data_list, innings_2_json_data_list):
    combined_data = []

    # Append the JSON objects from the first list
    for innings_1_json_data in innings_1_json_data_list:
        combined_data.append(innings_1_json_data["Innings1"])

    # Append the JSON objects from the second list
    for innings_2_json_data in innings_2_json_data_list:
        combined_data.append(innings_2_json_data["Innings2"])

    return combined_data


def convert_json_list_to_df(json_data_list, key_name):
    dataframes = []
    for json_data in json_data_list:
        df = pd.DataFrame(json_data[key_name])
        dataframes.append(df)
    final_dataframe = pd.concat(dataframes, ignore_index=True)

    return final_dataframe

