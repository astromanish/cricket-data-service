MatchBallSummary.md

- Table Name: cricketsimulatordb.MatchBallSummary
  This is the name of the table within the database.

- Columns:
  - id: INT
    This column represents a unique identifier for each record in the table.

  - competition_name: VARCHAR
    It stores the name of the cricket competition. It is of variable character type.

  - season: INT
    It represents the season of the cricket competition. It is stored as an integer.

  - match_id: INT
    This column stores the unique identifier for each cricket match.

  - over_number: INT
    It represents the number of the over in the match.

  - ball_number: INT
    It represents the number of the ball within an over.

  - over_text: VARCHAR
    This column stores a textual representation of the over, such as "1st over" or "2nd over".

  - batsman_id: INT
    It represents the unique identifier of the batsman.

  - non_striker_id: INT
    It represents the unique identifier of the non-striker batsman.

  - batting_position: SMALLINT
    It stores the position of the batsman in the batting order.

  - batsman_team_id: INT
    This column stores the unique identifier of the team to which the batsman belongs.

  - batting_phase: SMALLINT
    It represents the phase of batting, such as powerplay or middle overs.

  - against_bowler: INT
    It stores the unique identifier of the bowler against whom the batsman is playing.

  - bowler_team_id: INT
    This column stores the unique identifier of the team to which the bowler belongs.

  - innings: SMALLINT
    It represents the innings number in the match.

  - runs: SMALLINT
    It stores the runs scored on the ball.

  - ball_runs: SMALLINT
    It represents the runs scored on the ball by the batsman.

  - is_one, is_two, is_three, is_four, is_six: TINYINT
    These columns store boolean values (0 or 1) indicating whether the ball resulted in a specific number of runs.

  - is_dot_ball: TINYINT
    It represents whether the ball resulted in no run.

  - extras: SMALLINT
    It stores the extra runs scored on the ball.

  - is_extra, is_wide, is_no_ball, is_bye, is_leg_bye: TINYINT
    These columns store boolean values (0 or 1) indicating whether specific types of extras were scored.

  - is_wicket: TINYINT
    It represents whether a wicket fell on the ball.

  - wicket_type: VARCHAR
    This column stores the type of wicket, such as "caught", "bowled", or "run out".

  - is_bowler_wicket: TINYINT
    It indicates whether the wicket was taken by the bowler.

  - out_batsman_id: INT
    It represents the unique identifier of the batsman who got out.

  - is_maiden: TINYINT
    It indicates whether the over is a maiden over (no runs scored).

  - bowl_type: VARCHAR
    This column stores the type of delivery bowled, such as "fast", "spin", or "medium pace".

  - shot_type: VARCHAR
    It represents the type of shot played by the batsman.

  - bowl_line: VARCHAR
    It stores the line of the delivery, such as "off-stump", "leg-stump", or "outside off".

  - bowl_length: VARCHAR
    It represents the length of the delivery, such as "short", "good length", or "full length".

  - x_pitch, y_pitch: DECIMAL
    These columns store the coordinates of the pitch where the ball landed.

  - fielder_angle: DECIMAL
    It represents the angle at which the fielder is positioned.

  - fielder_length_ratio: DECIMAL
    It stores the length ratio of the fielder.

  - is_beaten, is_uncomfortable: TINYINT
    These columns store boolean values (0 or 1) indicating whether the batsman was beaten or felt uncomfortable.

  - bowling_direction: VARCHAR
    It represents the direction of the bowler, such as "right-arm", "left-arm", or "off-spin".

  - video_file: VARCHAR
    This column stores the file name or path of the associated video file.

  - load_timestamp: TIMESTAMP
    It represents the timestamp when the record was loaded into the table.

- Primary Key:
  The primary key of the table consists of the combination of columns (competition_name, season, match_id) along with the id column. This means that each record in the table is uniquely identified by the combination of these values.

The schema appears to be designed to store detailed information about each ball bowled in a cricket match. It includes information about the batsmen, bowlers, runs scored, extras, wickets, shot types, pitch coordinates, fielding angles, and other relevant attributes. The primary key ensures efficient retrieval of data by combining the competition, season, match, and unique identifier of each ball.