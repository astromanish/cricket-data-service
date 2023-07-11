**Table: Teams**

| Column Name | Data Type    | Description              |
|-------------|--------------|--------------------------|
| team_id     | INT          |                          |
| src_team_id | VARCHAR      | schedule                 |
| team_name   | VARCHAR      | schedule                 |
| team_short_name | varchar  | squad                    |
| competition_name | varchar | summary                  |
| team_image_url | VARCHAR   | summary                  |
| playoffs    | INT          | schedule                 |
| seasons_played | LIST<INT> | summary                  |
| titles      | INT          | schedule                 |
| load_timestamp | timestamp  |                          |

**Table: Players**

| Column Name | Data Type    | Description              |
|-------------|--------------|--------------------------|
| player_id   | INT          |                          |
| src_player_id | VARCHAR    |                          |
| player_name | VARCHAR      |                          |
| player_image_url | VARCHAR |                          |
| team_id     | INT          |                          |
| competition_name | VARCHAR |                          |
| season      | INT          |                          |
| player_type | varchar      |                          |
| batting_type | varchar     |                          |
| bowling_type | varchar     |                          |
| bowl_major_type | varchar  |                          |
| player_skill | varchar     |                          |
| is_captain  | TINYINT      |                          |
| is_batsman  | TINYINT      |                          |
| is_bowler   | TINYINT      |                          |
| is_wicket_keeper | TINYINT |                          |
| load_timestamp | timestamp  |                          |

**Table: Venue**

| Column Name | Data Type    | Description              |
|-------------|--------------|--------------------------|
| venue_id    | INT          |                          |
| src_venue_id | varchar     |                          |
| stadium_name | VARCHAR     |                          |
| city        | VARCHAR      |                          |
| country     | VARCHAR      |                          |
| load_timestamp | timestamp  |                          |

**Table: Matches**

| Column Name | Data Type    | Description              |
|-------------|--------------|--------------------------|
| match_id    | INT          |                          |
| src_match_id | VARCHAR     |                          |
| match_name  | VARCHAR      |                          |
| competition_name | VARCHAR |                          |
| venue       | INT          |                          |
| is_playoff  | TINYINT      |                          |
| is_title    | TINYINT      |                          |
| team1       | INT          |                          |
| team2       | INT          |                          |
| toss_team   | INT          |                          |
| toss_decision | VARCHAR    |                          |
| match_date  | VARCHAR      |                          |
| match_time  | varchar      |                          |
| season      | INT          |                          |
| team1_players | list<INT>  |                          |
| team2_players | list<INT>  |                          |
| team1_score | INT          |                          |
| team1_wickets | INT         |                          |
| team1_overs | DECIMAL      |                          |
| team2_score | INT          |                          |
| team2_wickets | INT         |                          |
| team2_overs | DECIMAL      |                          |
| team2_target | INT         |                          |
| winning_team | INT         |                          |
| match_result | VARCHAR     |                          |
| nature_of_wicket | VARCHAR |                          |
| overall_nature | VARCHAR   |                          |
| dew         | VARCHAR      |                          |
| match_date_form | DATE      |                          |
| load_timestamp | timestamp  |                          |

**Table: MatchBallSummary**

| Column Name | Data Type    | Description              |
|-------------|--------------|--------------------------|
| id          | INT          |                          |
| competition_name | VARCHAR |                          |
| season      | INT          |                          |
| match_id    | INT          |            done              |
| over_number | INT          |                          |
| ball_number | INT          |                          |
| over_text   | VARCHAR      |                          |
| batsman_id  | INT          |                          |
| non_striker_id | INT       |             done             |
| batting_position | SMALLINT |                          |
| batsman_team_id | INT      |                          |
| batting_phase | SMALLINT   |                          |
| against_bowler | INT       |                          |
| bowler_team_id | INT       |                          |
| innings     | SMALLINT     |                          |
| runs        | SMALLINT     |               done           |
| ball_runs   | SMALLINT     |               done           |
| is_one      | TINYINT      |           done               |
| is_two      | TINYINT      |            done              |
| is_three    | TINYINT      |            done              |
| is_four     | TINYINT      |                          |
| is_six      | TINYINT      |                          |
| is_dot_ball | TINYINT      |                          |
| extras      | SMALLINT     |                          |
| is_extra    | TINYINT      |                          |
| is_wide     | TINYINT      |                          |
| is_no_ball  | TINYINT      |                          |
| is_bye      | TINYINT      |                          |
| is_leg_bye  | TINYINT      |                          |
| is_wicket   | TINYINT      |                          |
| wicket_type | VARCHAR      |                          |
| is_bowler_wicket | TINYINT |                          |
| out_batsman_id | INT       |                          |
| is_maiden   | TINYINT      |                          |
| bowl_type   | VARCHAR      |                          |
| shot_type   | VARCHAR      |                          |
| bowl_line   | VARCHAR      |                          |
| bowl_length | VARCHAR      |                          |
| x_pitch     | decimal      |                          |
| y_pitch     | decimal      |                          |
| fielder_angle | decimal    |                          |
| fielder_length_ratio | decimal |                      |
| is_beaten   | TINYINT      |                          |
| is_uncomfortable | TINYINT |                          |
| bowling_direction | VARCHAR |                          |
| video_file  | varchar      |                          |
| load_timestamp | timestamp  |                          |
