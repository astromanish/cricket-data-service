from .utils import prepare_data

def process_players(match_players):
    match_players = prepare_data(match_players)
    return match_players 