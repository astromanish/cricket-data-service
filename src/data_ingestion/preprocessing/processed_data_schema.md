Teams
Players
Venues
Matches
Ball Summary 


**Table: Teams**

| Column Name | Data Type    | Description              |
|-------------|--------------|--------------------------|
| team_id     | INT          |    done                      |
| src_team_id | VARCHAR      | done                 |
| team_name   | VARCHAR      |      done            |
| team_short_name | varchar  |       done              |
| competition_name | varchar | done                  |
| team_image_url | VARCHAR   |      done             |
| playoffs    | INT          | done                 |
| seasons_played | LIST<INT> | done                  |
| titles      | INT          | done                 |
| load_timestamp | timestamp  |       done                   |

**Table: Players**

1. Merge with Teams DF you wrote

| Column Name | Data Type    | Description              |
|-------------|--------------|--------------------------|
| player_id   | INT          |      done                    |
| src_player_id | VARCHAR    |        done                  |
| player_name | VARCHAR      |        done                  |
| player_image_url | VARCHAR |                          |
| team_id     | INT          |         done                 |
| competition_name | VARCHAR |                          |
| season      | INT          |                          |
| player_type | varchar      |                          |
| batting_type | varchar     |             done             |
| bowling_type | varchar     |             done             |
| bowl_major_type | varchar  |              done            |
| player_skill | varchar     |             done             |
| is_captain  | TINYINT      |         done                 |
| is_batsman  | TINYINT      |          done                |
| is_bowler   | TINYINT      |           done               |
| is_wicket_keeper | TINYINT |           done               |
| load_timestamp | timestamp  |            done              |

**Table: Venue**

1. Find City and Country

| Column Name | Data Type    | Description              |
|-------------|--------------|--------------------------|
| venue_id    | INT          |        done                  |
| src_venue_id | varchar     |         done                 |
| stadium_name | VARCHAR     |         done                 |
| city        | VARCHAR      |                          |
| country     | VARCHAR      |                          |
| load_timestamp | timestamp  |          done                |

**Table: Matches**

1. get venue details

| Column Name | Data Type    | Description              |
|-------------|--------------|--------------------------|
| match_id    | INT          |           done               |
| src_match_id | VARCHAR     |            done              |
| match_name  | VARCHAR      |              done            |
| competition_name | VARCHAR |           done               |
| venue       | INT          |                          |
| is_playoff  | TINYINT      |             done             |
| is_title    | TINYINT      |             done             |
| team1       | INT          |             done             |
| team2       | INT          |                 done         |
| toss_team   | INT          |                          |
| toss_decision | VARCHAR    |                          |
| match_date  | VARCHAR      |           done               |
| match_time  | varchar      |          done                |
| season      | INT          |         done                 |
| team1_players | list<INT>  |                          |
| team2_players | list<INT>  |                          |
| team1_score | INT          |         done                 |
| team1_wickets | INT         |            done              |
| team1_overs | DECIMAL      |                 done         |
| team2_score | INT          |                     done     |
| team2_wickets | INT         |             done             |
| team2_overs | DECIMAL      |               done        |
| team2_target | INT         |                          |
| winning_team | INT         |          done                |
| match_result | VARCHAR     |                          |
| nature_of_wicket | VARCHAR |                          |
| overall_nature | VARCHAR   |                          |
| dew         | VARCHAR      |                          |
| match_date_form | DATE      |                          |
| load_timestamp | timestamp  |              done            |

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
