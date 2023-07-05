import inflection
def prepare_data(match_player):
    match_player.columns = [inflection.underscore(col) for col in match_player.columns]

    match_player['is_bowler'] = 0
    match_player['is_batsman'] = 0
    match_player['is_wicket_keeper'] = 0

    # Update the column values based on player_skill
    for index, row in match_player.iterrows():
        player_skill = row['player_skill']
        
        if player_skill == 'Batsman' or player_skill == 'Allrounder':
            match_player.at[index, 'is_batsman'] = 1
        
        if player_skill == 'Bowler' or player_skill == 'Allrounder':
            match_player.at[index, 'is_bowler'] = 1
        
        if player_skill == 'Wicketkeeper':
            match_player.at[index, 'is_wicket_keeper'] = 1
            match_player.at[index, 'is_batsman'] = 1

    return match_player.loc[:,['player_id','player_name','team_id','is_captain','player_skill','is_batsman','is_bowler','is_wicket_keeper']]
