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
