from .config import OVER_HISTORY_REQD_COLS, WAGONWHEEL_REQD_COLS

def process_match_ball_summary(match_innings_tuple_data):
    match_over_history = match_innings_tuple_data[9].loc[:,OVER_HISTORY_REQD_COLS]
    match_wagon_wheel = match_innings_tuple_data[3].loc[:,WAGONWHEEL_REQD_COLS]
    
    #get maximum id in innings table 
    #set competition name and season from path into match over history df
    #prepare wagonwheel df (by adding column if empty) for merge with innings df
    #get match ... and players df 
    #then merge with  final df 
    return []