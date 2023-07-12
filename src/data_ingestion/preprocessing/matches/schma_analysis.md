# Matche Df 1 - For 
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 120 entries, 0 to 119
Data columns (total 8 columns):
 #   Column                  Non-Null Count  Dtype 
---  ------                  --------------  ----- 
 0   match_id                120 non-null    object
 1   competition_name        120 non-null    object
 2   first_batting_team_id   120 non-null    object
 3   second_batting_team_id  120 non-null    object
 4   is_title                120 non-null    int64 
 5   is_playoff              120 non-null    int64 
 6   winning_team_id         120 non-null    object
 7   season                  120 non-null    object
dtypes: int64(2), object(6)
memory usage: 7.6+ KB
None

# Matches Df 2
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 118 entries, 0 to 117
Data columns (total 15 columns):
 #   Column                    Non-Null Count  Dtype 
---  ------                    --------------  ----- 
 0   match_id                  118 non-null    object
 1   match_date                118 non-null    object
 2   match_time                118 non-null    object
 3   first_batting_team_id     118 non-null    object
 4   match_date_order          118 non-null    int64 
 5   match_name                118 non-null    object
 6   first_batting_team_name   118 non-null    object
 7   second_batting_team_id    118 non-null    object
 8   second_batting_team_name  118 non-null    object
 9   ground_name               118 non-null    object
 10  comments                  118 non-null    object
 11  toss_team                 118 non-null    object
 12  toss_details              118 non-null    object
 13  first_batting_summary     118 non-null    object
 14  second_batting_summary    118 non-null    object
dtypes: int64(1), object(14)
memory usage: 14.0+ KB

# Teams 
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 8 entries, 0 to 7
Data columns (total 8 columns):
 #   Column            Non-Null Count  Dtype 
---  ------            --------------  ----- 
 0   team_id           8 non-null      int64 
 1   src_team_id       8 non-null      object
 2   team_name         8 non-null      object
 3   competition_name  8 non-null      object
 4   seasons_played    8 non-null      object
 5   titles            8 non-null      int64 
 6   playoffs          8 non-null      int64 
 7   team_short_name   8 non-null      object
dtypes: int64(3), object(5)
memory usage: 644.0+ bytes
None

# Players
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 151 entries, 0 to 150
Data columns (total 3 columns):
 #   Column         Non-Null Count  Dtype 
---  ------         --------------  ----- 
 0   player_name    151 non-null    object
 1   src_player_id  151 non-null    object
 2   player_id      151 non-null    int64 
dtypes: int64(1), object(2)
memory usage: 3.7+ KB
None

# Venues
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 15 entries, 0 to 14
Data columns (total 3 columns):
 #   Column        Non-Null Count  Dtype 
---  ------        --------------  ----- 
 0   stadium_name  15 non-null     object
 1   src_venue_id  15 non-null     object
 2   venue_id      15 non-null     int64 
dtypes: int64(1), object(2)
memory usage: 492.0+ bytes
None

