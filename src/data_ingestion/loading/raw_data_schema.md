match results: (59, 23)
Match Results Schema:
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 59 entries, 0 to 58
Data columns (total 23 columns):
 #   Column                 Non-Null Count  Dtype 
---  ------                 --------------  ----- 
 0   CompetitionID          59 non-null     object
 1   MatchID                59 non-null     object
 2   MatchTypeID            59 non-null     object
 3   MatchType              59 non-null     object
 4   MatchStatus            59 non-null     object
 5   MatchName              59 non-null     object
 6   MatchDate              59 non-null     object
 7   MatchTime              59 non-null     object
 8   FirstBattingTeamID     59 non-null     object
 9   FirstBattingTeamName   59 non-null     object
 10  HomeTeamLogo           59 non-null     object
 11  SecondBattingTeamID    59 non-null     object
 12  SecondBattingTeamName  59 non-null     object
 13  AwayTeamLogo           59 non-null     object
 14  GroundID               59 non-null     object
 15  GroundName             59 non-null     object
 16  Comments               59 non-null     object
 17  TossDetails            59 non-null     object
 18  TossTeam               59 non-null     object
 19  TossText               59 non-null     object
 20  FirstBattingSummary    59 non-null     object
 21  SecondBattingSummary   59 non-null     object
 22  MatchDateOrder         59 non-null     int64 
dtypes: int64(1), object(22)
memory usage: 10.7+ KB
None
match summaries: (1, 69)
Match Summaries Schema:
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1 entries, 0 to 0
Data columns (total 69 columns):
 #   Column                          Non-Null Count  Dtype 
---  ------                          --------------  ----- 
 0   MatchID                         1 non-null      object
 1   CompetitionName                 1 non-null      object
 2   Team1                           1 non-null      object
 3   Team2                           1 non-null      object
 4   Team1Logo                       1 non-null      object
 5   Team2Logo                       1 non-null      object
 6   MatchName                       1 non-null      object
 7   MatchDate                       1 non-null      object
 8   MatchType                       1 non-null      object
 9   FirstBattingTeamID              1 non-null      object
 10  FirstBattingTeamLogo            1 non-null      object
 11  FirstBattingTeam                1 non-null      object
 12  SecondBattingTeamID             1 non-null      object
 13  SecondBattingTeamLogo           1 non-null      object
 14  SecondBattingTeam               1 non-null      object
 15  SecondInningsFirstBattingID     1 non-null      object
 16  SecondInningsFirstBattingName   1 non-null      object
 17  SecondInningsSecondBattingID    1 non-null      object
 18  SecondInningsSecondBattingName  1 non-null      object
 19  TossDetails                     1 non-null      object
 20  BreakComments                   1 non-null      object
 21  GroundName                      1 non-null      object
 22  Comments                        1 non-null      object
 23  PointsComments                  1 non-null      object
 24  RevisedOver                     1 non-null      object
 25  RevisedTarget                   1 non-null      object
 26  RequiredRunRate                 1 non-null      object
 27  ChasingText                     1 non-null      object
 28  Target                          1 non-null      object
 29  CurrentInnings                  1 non-null      object
 30  IsMatchEnd                      1 non-null      int64 
 31  Umpire1Name                     1 non-null      object
 32  Umpire2Name                     1 non-null      object
 33  Umpire3Name                     1 non-null      object
 34  VideoAnalyst1                   1 non-null      object
 35  VideoAnalyst2                   1 non-null      object
 36  Referee                         1 non-null      object
 37  CurrentStrikerID                1 non-null      object
 38  CurrentBowlerID                 1 non-null      object
 39  CurrentStrikerName              1 non-null      object
 40  CurrentNonStrikerID             1 non-null      object
 41  CurrentNonStrikerName           1 non-null      object
 42  CurrentBowlerName               1 non-null      object
 43  1Summary                        1 non-null      object
 44  1FallScore                      1 non-null      object
 45  1FallWickets                    1 non-null      object
 46  1FallOvers                      1 non-null      object
 47  1RunRate                        1 non-null      object
 48  2Summary                        1 non-null      object
 49  2FallScore                      1 non-null      object
 50  2FallWickets                    1 non-null      object
 51  2FallOvers                      1 non-null      object
 52  2RunRate                        1 non-null      object
 53  3Summary                        1 non-null      object
 54  3FallScore                      1 non-null      object
 55  3FallWickets                    1 non-null      object
 56  3FallOvers                      1 non-null      object
 57  3RunRate                        1 non-null      object
 58  4Summary                        1 non-null      object
 59  4FallScore                      1 non-null      object
 60  4FallWickets                    1 non-null      object
 61  4FallOvers                      1 non-null      object
 62  4RunRate                        1 non-null      object
 63  TimerValue                      1 non-null      object
 64  IsSuperOver                     1 non-null      object
 65  FBURL                           1 non-null      object
 66  WinningTeamID                   1 non-null      object
 67  MOM                             1 non-null      object
 68  SuperOverMatchID                0 non-null      object
dtypes: int64(1), object(68)
memory usage: 684.0+ bytes
None
match players: (22, 13)
Match Players Schema:
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 22 entries, 0 to 21
Data columns (total 13 columns):
 #   Column              Non-Null Count  Dtype 
---  ------              --------------  ----- 
 0   TeamID              22 non-null     object
 1   TeamCode            22 non-null     object
 2   TeamName            22 non-null     object
 3   TeamImage           22 non-null     object
 4   PlayerName          22 non-null     object
 5   PlayerShortName     22 non-null     object
 6   PlayerImage         22 non-null     object
 7   PlayerID            22 non-null     object
 8   BattingType         22 non-null     object
 9   BowlingProficiency  22 non-null     object
 10  PlayerSkill         22 non-null     object
 11  IsCaptain           22 non-null     int64 
 12  IsViceCaptain       22 non-null     int64 
dtypes: int64(2), object(11)
memory usage: 2.4+ KB
None
/usr/lib/python3.11/concurrent/futures/thread.py:58: DtypeWarning: Columns (20,21) have mixed types. Specify dtype option on import or set low_memory=False.
  result = self.fn(*self.args, **self.kwargs)
match balls: (70582, 22)
Match Balls Schema:
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 70582 entries, 0 to 70581
Data columns (total 22 columns):
 #   Column                  Non-Null Count  Dtype  
---  ------                  --------------  -----  
 0   match_id                70582 non-null  int64  
 1   season                  70582 non-null  object 
 2   start_date              70582 non-null  object 
 3   venue                   70582 non-null  object 
 4   innings                 70582 non-null  int64  
 5   ball                    70582 non-null  float64
 6   batting_team            70582 non-null  object 
 7   bowling_team            70582 non-null  object 
 8   striker                 70582 non-null  object 
 9   non_striker             70582 non-null  object 
 10  bowler                  70582 non-null  object 
 11  runs_off_bat            70582 non-null  int64  
 12  extras                  70582 non-null  int64  
 13  wides                   2108 non-null   float64
 14  noballs                 242 non-null    float64
 15  byes                    228 non-null    float64
 16  legbyes                 1055 non-null   float64
 17  penalty                 1 non-null      float64
 18  wicket_type             3781 non-null   object 
 19  player_dismissed        3781 non-null   object 
 20  other_wicket_type       1 non-null      object 
 21  other_player_dismissed  1 non-null      object 
dtypes: float64(6), int64(4), object(12)
memory usage: 11.8+ MB
None

match_batting_card DataFrame:
Shape: (22, 31)
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 22 entries, 0 to 21
Data columns (total 31 columns):
 #   Column              Non-Null Count  Dtype  
---  ------              --------------  -----  
 0   MatchID             22 non-null     object 
 1   InningsNo           22 non-null     object 
 2   TeamID              22 non-null     object 
 3   PlayerID            22 non-null     object 
 4   BatSpec             22 non-null     object 
 5   BowlSpec            22 non-null     object 
 6   PlayerName          22 non-null     object 
 7   PlayerImage         22 non-null     object 
 8   PlayingOrder        22 non-null     int64  
 9   BowlerName          22 non-null     object 
 10  OutDesc             22 non-null     object 
 11  Runs                22 non-null     object 
 12  Balls               22 non-null     object 
 13  DotBalls            22 non-null     object 
 14  DotBallPercentage   22 non-null     object 
 15  DotBallFrequency    22 non-null     object 
 16  Ones                22 non-null     object 
 17  Twos                22 non-null     object 
 18  Threes              22 non-null     object 
 19  Fours               22 non-null     object 
 20  Sixes               22 non-null     object 
 21  BoundaryPercentage  22 non-null     object 
 22  BoundaryFrequency   22 non-null     object 
 23  StrikeRate          22 non-null     object 
 24  MinOver             22 non-null     float64
 25  MinStrikerOver      22 non-null     float64
 26  WicketNo            22 non-null     object 
 27  AgainstFast         22 non-null     object 
 28  AgainstFastPercent  22 non-null     object 
 29  AgainstSpin         22 non-null     object 
 30  AgainstSpinPercent  22 non-null     object 
dtypes: float64(2), int64(1), object(28)
memory usage: 5.5+ KB
Columns: None

match_extras DataFrame:
Shape: (2, 17)
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 2 entries, 0 to 1
Data columns (total 17 columns):
 #   Column              Non-Null Count  Dtype 
---  ------              --------------  ----- 
 0   MatchID             2 non-null      object
 1   InningsNo           2 non-null      object
 2   TeamID              2 non-null      object
 3   Total               2 non-null      object
 4   TotalExtras         2 non-null      object
 5   Byes                2 non-null      object
 6   LegByes             2 non-null      object
 7   NoBalls             2 non-null      object
 8   Wides               2 non-null      object
 9   Penalty             2 non-null      object
 10  CurrentRunRate      2 non-null      object
 11  FallScore           2 non-null      object
 12  FallWickets         2 non-null      object
 13  FallOvers           2 non-null      object
 14  BattingTeamName     2 non-null      object
 15  BowlingTeamName     2 non-null      object
 16  MaxPartnerShipRuns  2 non-null      int64 
dtypes: int64(1), object(16)
memory usage: 404.0+ bytes
Columns: None

match_fall_of_wickets DataFrame:
Shape: (10, 9)
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 10 entries, 0 to 9
Data columns (total 9 columns):
 #   Column       Non-Null Count  Dtype 
---  ------       --------------  ----- 
 0   MatchID      10 non-null     object
 1   InningsNo    10 non-null     object
 2   TeamID       10 non-null     object
 3   PlayerID     10 non-null     object
 4   PlayerName   10 non-null     object
 5   Score        10 non-null     object
 6   FallScore    10 non-null     object
 7   FallWickets  10 non-null     object
 8   FallOvers    10 non-null     object
dtypes: object(9)
memory usage: 852.0+ bytes
Columns: None

match_wagon_wheel DataFrame:
Shape: (143, 9)
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 143 entries, 0 to 142
Data columns (total 9 columns):
 #   Column              Non-Null Count  Dtype  
---  ------              --------------  -----  
 0   BallID              143 non-null    object 
 1   StrikerID           143 non-null    object 
 2   BowlerID            143 non-null    object 
 3   FielderAngle        143 non-null    float64
 4   FielderLengthRatio  143 non-null    float64
 5   Runs                143 non-null    int64  
 6   BatType             143 non-null    object 
 7   IsFour              143 non-null    bool   
 8   IsSix               143 non-null    bool   
dtypes: bool(2), float64(2), int64(1), object(4)
memory usage: 8.2+ KB
Columns: None

match_partnership_scores DataFrame:
Shape: (24, 15)
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 24 entries, 0 to 23
Data columns (total 15 columns):
 #   Column            Non-Null Count  Dtype  
---  ------            --------------  -----  
 0   MatchID           24 non-null     object 
 1   BattingTeamID     24 non-null     object 
 2   InningsNo         24 non-null     object 
 3   StrikerID         24 non-null     object 
 4   Striker           24 non-null     object 
 5   NonStrikerID      24 non-null     object 
 6   NonStriker        24 non-null     object 
 7   PartnershipTotal  24 non-null     int64  
 8   StrikerRuns       24 non-null     int64  
 9   StrikerBalls      24 non-null     int64  
 10  Extras            24 non-null     int64  
 11  NonStrikerRuns    24 non-null     int64  
 12  NonStrikerBalls   24 non-null     int64  
 13  MatchMaxOver      24 non-null     float64
 14  MatchMinOver      24 non-null     float64
dtypes: float64(2), int64(6), object(7)
memory usage: 2.9+ KB
Columns: None

match_partnership_break DataFrame:
Shape: (10, 5)
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 10 entries, 0 to 9
Data columns (total 5 columns):
 #   Column        Non-Null Count  Dtype  
---  ------        --------------  -----  
 0   InningsNo     10 non-null     object 
 1   OverNo        10 non-null     float64
 2   WicketNo      10 non-null     int64  
 3   WicketType    10 non-null     object 
 4   OutBatsmanID  10 non-null     object 
dtypes: float64(1), int64(1), object(3)
memory usage: 532.0+ bytes
Columns: None

match_bowling_card DataFrame:
Shape: (12, 32)
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 12 entries, 0 to 11
Data columns (total 32 columns):
 #   Column                 Non-Null Count  Dtype 
---  ------                 --------------  ----- 
 0   MatchID                12 non-null     object
 1   InningsNos             12 non-null     int64 
 2   TeamID                 12 non-null     object
 3   PlayerID               12 non-null     object
 4   BatSpec                12 non-null     object
 5   BowlSpec               12 non-null     object
 6   PlayerName             12 non-null     object
 7   PlayerImage            12 non-null     object
 8   Overs                  12 non-null     object
 9   Maidens                12 non-null     int64 
 10  Runs                   12 non-null     int64 
 11  Wickets                12 non-null     int64 
 12  Wides                  12 non-null     int64 
 13  NoBalls                12 non-null     int64 
 14  Economy                12 non-null     object
 15  BowlingOrder           12 non-null     int64 
 16  InningsNo              12 non-null     object
 17  TotalLegalBallsBowled  12 non-null     int64 
 18  ScoringBalls           12 non-null     int64 
 19  DotBalls               12 non-null     int64 
 20  DBPercent              12 non-null     object
 21  DBFrequency            12 non-null     object
 22  Ones                   12 non-null     int64 
 23  Twos                   12 non-null     int64 
 24  Threes                 12 non-null     int64 
 25  Fours                  12 non-null     int64 
 26  Sixes                  12 non-null     int64 
 27  BdryPercent            12 non-null     object
 28  BdryFreq               12 non-null     object
 29  StrikeRate             12 non-null     object
 30  FourPercent            12 non-null     object
 31  SixPercent             12 non-null     object
dtypes: int64(15), object(17)
memory usage: 3.1+ KB
Columns: None

match_manhattan_graph DataFrame:
Shape: (76, 7)
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 76 entries, 0 to 75
Data columns (total 7 columns):
 #   Column      Non-Null Count  Dtype  
---  ------      --------------  -----  
 0   InningsNo   76 non-null     object 
 1   OverNo      76 non-null     int64  
 2   OverRuns    76 non-null     float64
 3   BowlerRuns  76 non-null     int64  
 4   BowlerID    76 non-null     object 
 5   Wickets     76 non-null     int64  
 6   Bowler      76 non-null     object 
dtypes: float64(1), int64(3), object(3)
memory usage: 4.3+ KB
Columns: None

match_manhattan_wickets DataFrame:
Shape: (18, 6)
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 18 entries, 0 to 17
Data columns (total 6 columns):
 #   Column        Non-Null Count  Dtype 
---  ------        --------------  ----- 
 0   InningsNo     18 non-null     object
 1   OverNo        18 non-null     int64 
 2   OutBatsman    18 non-null     object
 3   OutDesc       18 non-null     object
 4   BatsmanRuns   18 non-null     int64 
 5   BatsmanBalls  18 non-null     int64 
dtypes: int64(3), object(3)
memory usage: 996.0+ bytes
Columns: None

match_over_history DataFrame:
Shape: (232, 59)
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 232 entries, 0 to 231
Data columns (total 59 columns):
 #   Column            Non-Null Count  Dtype 
---  ------            --------------  ----- 
 0   BallID            232 non-null    object
 1   MatchID           232 non-null    object
 2   InningsNos        232 non-null    int64 
 3   BattingTeamID     232 non-null    object
 4   TeamName          232 non-null    object
 5   StrikerID         232 non-null    object
 6   NonStrikerID      232 non-null    object
 7   BatsManName       232 non-null    object
 8   BowlerID          232 non-null    object
 9   BowlerName        232 non-null    object
 10  BowlerType        232 non-null    object
 11  OverNo            232 non-null    int64 
 12  OverName          232 non-null    object
 13  BallNo            232 non-null    int64 
 14  Runs              232 non-null    object
 15  BallRuns          232 non-null    object
 16  RunsText          232 non-null    object
 17  ActualRuns        232 non-null    int64 
 18  IsOne             232 non-null    int64 
 19  IsTwo             232 non-null    int64 
 20  IsThree           232 non-null    int64 
 21  IsDotball         232 non-null    int64 
 22  BallCount         232 non-null    int64 
 23  Extras            232 non-null    int64 
 24  IsWide            232 non-null    bool  
 25  IsNoBall          232 non-null    bool  
 26  IsBye             232 non-null    bool  
 27  IsLegBye          232 non-null    bool  
 28  IsFour            232 non-null    bool  
 29  IsSix             232 non-null    bool  
 30  BowlType          232 non-null    object
 31  ShotType          232 non-null    object
 32  Length            232 non-null    object
 33  Line              232 non-null    object
 34  IsWicket          232 non-null    int64 
 35  WicketType        232 non-null    object
 36  Wickets           232 non-null    object
 37  VideoFile         232 non-null    object
 38  CommentOver       232 non-null    object
 39  BallName          232 non-null    object
 40  CommentStrikers   232 non-null    object
 41  NewCommentry      232 non-null    object
 42  IsExtra           232 non-null    int64 
 43  OutBatsManID      232 non-null    object
 44  SNO               232 non-null    int64 
 45  BallTime          232 non-null    object
 46  FBCommentry       0 non-null      object
 47  Xpitch            232 non-null    int64 
 48  Ypitch            232 non-null    int64 
 49  IsBowlerWicket    232 non-null    int64 
 50  IsBeaten          232 non-null    bool  
 51  IsUncomfortable   232 non-null    bool  
 52  BowlingDirection  232 non-null    object
 53  IsMaiden          232 non-null    int64 
 54  InningsNo         232 non-null    object
 55  TotalRuns         232 non-null    int64 
 56  TotalWickets      232 non-null    int64 
 57  OverRuns          232 non-null    int64 
 58  Commentry         232 non-null    object
dtypes: bool(8), int64(20), object(31)
memory usage: 94.4+ KB
Columns: None

match_wagon_wheel_summary DataFrame:
Shape: (2, 8)
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 2 entries, 0 to 1
Data columns (total 8 columns):
 #   Column         Non-Null Count  Dtype 
---  ------         --------------  ----- 
 0   MatchID        2 non-null      object
 1   BattingTeamID  2 non-null      object
 2   InningsNo      2 non-null      object
 3   Ones           2 non-null      int64 
 4   Twos           2 non-null      int64 
 5   Threes         2 non-null      int64 
 6   Fours          2 non-null      int64 
 7   Sixes          2 non-null      int64 
dtypes: int64(5), object(3)
memory usage: 260.0+ bytes
Columns: None

match_batting_head_to_head DataFrame:
Shape: (48, 23)
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 48 entries, 0 to 47
Data columns (total 23 columns):
 #   Column             Non-Null Count  Dtype  
---  ------             --------------  -----  
 0   KPI                48 non-null     object 
 1   BatsManID          48 non-null     object 
 2   BowlerID           48 non-null     object 
 3   BatsManName        48 non-null     object 
 4   BowlerName         48 non-null     object 
 5   Runs               48 non-null     int64  
 6   RunsThroughExtras  48 non-null     int64  
 7   TotalRuns          48 non-null     int64  
 8   BallsFaced         48 non-null     int64  
 9   StrikeRate         48 non-null     float64
 10  DotBalls           48 non-null     int64  
 11  DBPercent          48 non-null     float64
 12  DotBallFrequency   48 non-null     float64
 13  ScoringBalls       48 non-null     int64  
 14  Ones               48 non-null     int64  
 15  Twos               48 non-null     int64  
 16  Threes             48 non-null     int64  
 17  Fours              48 non-null     int64  
 18  Sixes              48 non-null     int64  
 19  BdryFreq           48 non-null     float64
 20  BdryPercent        48 non-null     float64
 21  WicketsLost        48 non-null     int64  
 22  RPSS               48 non-null     float64
dtypes: float64(6), int64(12), object(5)
memory usage: 8.8+ KB
Columns: None

match_bowling_head_to_head DataFrame:
Shape: (48, 23)
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 48 entries, 0 to 47
Data columns (total 23 columns):
 #   Column             Non-Null Count  Dtype  
---  ------             --------------  -----  
 0   KPI                48 non-null     object 
 1   BatsManID          48 non-null     object 
 2   BowlerID           48 non-null     object 
 3   BatsManName        48 non-null     object 
 4   BowlerName         48 non-null     object 
 5   Runs               48 non-null     int64  
 6   RunsThroughExtras  48 non-null     int64  
 7   TotalRuns          48 non-null     int64  
 8   BallsFaced         48 non-null     int64  
 9   StrikeRate         48 non-null     float64
 10  DotBalls           48 non-null     int64  
 11  DBPercent          48 non-null     float64
 12  DotBallFrequency   48 non-null     float64
 13  ScoringBalls       48 non-null     int64  
 14  Ones               48 non-null     int64  
 15  Twos               48 non-null     int64  
 16  Threes             48 non-null     int64  
 17  Fours              48 non-null     int64  
 18  Sixes              48 non-null     int64  
 19  BdryFreq           48 non-null     float64
 20  BdryPercent        48 non-null     float64
 21  WicketsLost        48 non-null     int64  
 22  RPSS               48 non-null     float64
dtypes: float64(6), int64(12), object(5)
memory usage: 8.8+ KB
Columns: None