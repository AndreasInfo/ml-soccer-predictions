import datetime as dt

import numpy as np
import pandas as pd
import pytest

import modules.engineer as eng

BASE_PATH = "./tests/sources/data/test_base.csv"
COACHES_PATH = "./tests/sources/data/test_coaches.csv"
PROMOTIONS_PATH = "./tests/sources/data/test_promotions.csv"


def test_add_Days_Since_Last_Game():
    with pytest.raises(KeyError):
        data = {
            "col": ["2017-08-19VfL WolfsburgBorussia Dortmund"],
            "Home Team": ["VfL Wolfsburg"],
            "Away Team": ["Borussia Dortmund"],
            "Date": [dt.datetime(2017, 8, 19)],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Days_Since_Last_Game(df)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19VfL WolfsburgBorussia Dortmund"],
            "col": ["VfL Wolfsburg"],
            "Away Team": ["Borussia Dortmund"],
            "Date": [dt.datetime(2017, 8, 19)],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Days_Since_Last_Game(df)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19VfL WolfsburgBorussia Dortmund"],
            "Home Team": ["VfL Wolfsburg"],
            "col": ["Borussia Dortmund"],
            "Date": [dt.datetime(2017, 8, 19)],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Days_Since_Last_Game(df)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19VfL WolfsburgBorussia Dortmund"],
            "Home Team": ["VfL Wolfsburg"],
            "Away Team": ["Borussia Dortmund"],
            "col": [dt.datetime(2017, 8, 19)],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Days_Since_Last_Game(df)

    with pytest.raises(ValueError):
        data = {
            "Primary Key": ["2017-08-19VfL WolfsburgBorussia Dortmund"],
            "Home Team": ["VfL Wolfsburg"],
            "Away Team": ["Borussia Dortmund"],
            "Date": ["A"],
            "Season": ["2017-2018"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Days_Since_Last_Game(df)

    df = pd.read_csv(
        BASE_PATH,
        index_col=0,
        parse_dates=["Date"],
        date_parser=lambda x: dt.datetime.strptime(x, "%Y-%m-%d"),
    )

    df = eng.add_Days_Since_Last_Game(df)
    col_home = "Home Days Since Last Game"
    col_away = "Away Days Since Last Game"

    game_key = "2017-08-19VfL WolfsburgBorussia Dortmund"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == -1
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == -1

    game_key = "2017-09-17Bayer 04 LeverkusenSC Freiburg"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == 8
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == 8


def test_add_Coach():
    with pytest.raises(KeyError):
        data = {
            "col": ["Borussia Dortmund"],
            "Away Team": ["VfL Wolfsburg"],
            "Date": [dt.datetime(2017, 8, 19)],
        }
        df = pd.DataFrame(data=data)
        data = {
            "Team": ["Borussia Dortmund", "VfL Wolfsburg"],
            "Coach": ["Peter Bosz", "Andries Jonker"],
            "Started": [dt.datetime(2017, 7, 1), dt.datetime(2017, 2, 27)],
            "Ended": [dt.datetime(2017, 12, 9), dt.datetime(2017, 9, 17)],
        }
        df_coach = pd.DataFrame(data=data)
        df = eng.add_Coach(df, df_coach)

    with pytest.raises(KeyError):
        data = {
            "Home Team": ["Borussia Dortmund"],
            "col": ["VfL Wolfsburg"],
            "Date": [dt.datetime(2017, 8, 19)],
        }
        df = pd.DataFrame(data=data)
        data = {
            "Team": ["Borussia Dortmund", "VfL Wolfsburg"],
            "Coach": ["Peter Bosz", "Andries Jonker"],
            "Started": [dt.datetime(2017, 7, 1), dt.datetime(2017, 2, 27)],
            "Ended": [dt.datetime(2017, 12, 9), dt.datetime(2017, 9, 17)],
        }
        df_coach = pd.DataFrame(data=data)
        df = eng.add_Coach(df, df_coach)

    with pytest.raises(KeyError):
        data = {
            "Home Team": ["Borussia Dortmund"],
            "Away Team": ["VfL Wolfsburg"],
            "col": [dt.datetime(2017, 8, 19)],
        }
        df = pd.DataFrame(data=data)
        data = {
            "Team": ["Borussia Dortmund", "VfL Wolfsburg"],
            "Coach": ["Peter Bosz", "Andries Jonker"],
            "Started": [dt.datetime(2017, 7, 1), dt.datetime(2017, 2, 27)],
            "Ended": [dt.datetime(2017, 12, 9), dt.datetime(2017, 9, 17)],
        }
        df_coach = pd.DataFrame(data=data)
        df = eng.add_Coach(df, df_coach)

    with pytest.raises(TypeError):
        data = {
            "Home Team": ["Borussia Dortmund"],
            "Away Team": ["VfL Wolfsburg"],
            "Date": ["2017-08-19"],
        }
        df = pd.DataFrame(data=data)
        data = {
            "Team": ["Borussia Dortmund", "VfL Wolfsburg"],
            "Coach": ["Peter Bosz", "Andries Jonker"],
            "Started": [dt.datetime(2017, 7, 1), dt.datetime(2017, 2, 27)],
            "Ended": [dt.datetime(2017, 12, 9), dt.datetime(2017, 9, 17)],
        }
        df_coach = pd.DataFrame(data=data)
        eng.add_Coach(df, df_coach)

    with pytest.raises(KeyError):
        data = {
            "Home Team": ["Borussia Dortmund"],
            "Away Team": ["VfL Wolfsburg"],
            "Date": [dt.datetime(2017, 8, 19)],
        }
        df = pd.DataFrame(data=data)
        data = {
            "col": ["Borussia Dortmund", "VfL Wolfsburg"],
            "Coach": ["Peter Bosz", "Andries Jonker"],
            "Started": [dt.datetime(2017, 7, 1), dt.datetime(2017, 2, 27)],
            "Ended": [dt.datetime(2017, 12, 9), dt.datetime(2017, 9, 17)],
        }
        df_coach = pd.DataFrame(data=data)
        df = eng.add_Coach(df, df_coach)

    with pytest.raises(KeyError):
        data = {
            "Home Team": ["Borussia Dortmund"],
            "Away Team": ["VfL Wolfsburg"],
            "Date": [dt.datetime(2017, 8, 19)],
        }
        df = pd.DataFrame(data=data)
        data = {
            "Team": ["Borussia Dortmund", "VfL Wolfsburg"],
            "col": ["Peter Bosz", "Andries Jonker"],
            "Started": [dt.datetime(2017, 7, 1), dt.datetime(2017, 2, 27)],
            "Ended": [dt.datetime(2017, 12, 9), dt.datetime(2017, 9, 17)],
        }
        df_coach = pd.DataFrame(data=data)
        df = eng.add_Coach(df, df_coach)

    with pytest.raises(KeyError):
        data = {
            "Home Team": ["Borussia Dortmund"],
            "Away Team": ["VfL Wolfsburg"],
            "Date": [dt.datetime(2017, 8, 19)],
        }
        df = pd.DataFrame(data=data)
        data = {
            "Team": ["Borussia Dortmund", "VfL Wolfsburg"],
            "Coach": ["Peter Bosz", "Andries Jonker"],
            "col": [dt.datetime(2017, 7, 1), dt.datetime(2017, 2, 27)],
            "Ended": [dt.datetime(2017, 12, 9), dt.datetime(2017, 9, 17)],
        }
        df_coach = pd.DataFrame(data=data)
        df = eng.add_Coach(df, df_coach)

    with pytest.raises(KeyError):
        data = {
            "Home Team": ["Borussia Dortmund"],
            "Away Team": ["VfL Wolfsburg"],
            "Date": [dt.datetime(2017, 8, 19)],
        }
        df = pd.DataFrame(data=data)
        data = {
            "Team": ["Borussia Dortmund", "VfL Wolfsburg"],
            "Coach": ["Peter Bosz", "Andries Jonker"],
            "Started": [dt.datetime(2017, 7, 1), dt.datetime(2017, 2, 27)],
            "col": [dt.datetime(2017, 12, 9), dt.datetime(2017, 9, 17)],
        }
        df_coach = pd.DataFrame(data=data)
        df = eng.add_Coach(df, df_coach)

    with pytest.raises(TypeError):
        data = {
            "Home Team": ["Borussia Dortmund"],
            "Away Team": ["VfL Wolfsburg"],
            "Date": [dt.datetime(2017, 8, 19)],
        }
        df = pd.DataFrame(data=data)
        data = {
            "Team": ["Borussia Dortmund", "VfL Wolfsburg"],
            "Coach": ["Peter Bosz", "Andries Jonker"],
            "Started": ["2017-07-01", "2017-02-27"],
            "Ended": [dt.datetime(2017, 12, 9), dt.datetime(2017, 9, 17)],
        }
        df_coach = pd.DataFrame(data=data)
        df = eng.add_Coach(df, df_coach)

    with pytest.raises(TypeError):
        data = {
            "Home Team": ["Borussia Dortmund"],
            "Away Team": ["VfL Wolfsburg"],
            "Date": [dt.datetime(2017, 8, 19)],
        }
        df = pd.DataFrame(data=data)
        data = {
            "Team": ["Borussia Dortmund", "VfL Wolfsburg"],
            "Coach": ["Peter Bosz", "Andries Jonker"],
            "Started": [dt.datetime(2017, 7, 1), dt.datetime(2017, 2, 27)],
            "Ended": ["2017-12-09", "2017-09-17"],
        }
        df_coach = pd.DataFrame(data=data)
        df = eng.add_Coach(df, df_coach)

    df = pd.read_csv(
        BASE_PATH,
        index_col=0,
        parse_dates=["Date"],
        date_parser=lambda x: dt.datetime.strptime(x, "%Y-%m-%d"),
    )
    df_coach = pd.read_csv(
        COACHES_PATH,
        index_col=0,
        parse_dates=["Started", "Ended"],
        date_parser=lambda x: dt.datetime.strptime(x, "%Y-%m-%d"),
    )

    df = eng.add_Coach(df, df_coach)
    col_home = "Home Coach"
    col_away = "Away Coach"

    game_key = "2017-08-19VfL WolfsburgBorussia Dortmund"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == "UNKNOWN"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == "Peter Bosz"

    game_key = "2017-08-26Borussia DortmundHertha BSC"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == "Peter Bosz"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == "UNKNOWN"

    game_key = "2017-09-17Borussia Dortmund1. FC Köln"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == "Peter Bosz"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == "Peter Stöger"

    game_key = "2017-09-17Bayer 04 LeverkusenSC Freiburg"
    assert len(df.loc[df["Primary Key"] == game_key]) == 1
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == "Heiko Herrlich"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == "JOHN DOE"


def test_add_Coach_Substituted_Within_Last_OFFSET_Games():
    with pytest.raises(KeyError):
        data = {
            "col": ["2017-2018VfL WolfsburgBorussia Dortmund"],
            "Season": ["2017-2018"],
            "Home Team": ["VfL Wolfsburg"],
            "Home Coach": ["Andries Jonker"],
            "Away Team": ["Borussia Dortmund"],
            "Away Coach": ["Peter Bosz"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Coach_Substituted_Within_Last_OFFSET_Games(df, 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-2018VfL WolfsburgBorussia Dortmund"],
            "col": ["2017-2018"],
            "Home Team": ["VfL Wolfsburg"],
            "Home Coach": ["Andries Jonker"],
            "Away Team": ["Borussia Dortmund"],
            "Away Coach": ["Peter Bosz"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Coach_Substituted_Within_Last_OFFSET_Games(df, 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-2018VfL WolfsburgBorussia Dortmund"],
            "Season": ["2017-2018"],
            "col": ["VfL Wolfsburg"],
            "Home Coach": ["Andries Jonker"],
            "Away Team": ["Borussia Dortmund"],
            "Away Coach": ["Peter Bosz"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Coach_Substituted_Within_Last_OFFSET_Games(df, 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-2018VfL WolfsburgBorussia Dortmund"],
            "Season": ["2017-2018"],
            "Home Team": ["VfL Wolfsburg"],
            "col": ["Andries Jonker"],
            "Away Team": ["Borussia Dortmund"],
            "Away Coach": ["Peter Bosz"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Coach_Substituted_Within_Last_OFFSET_Games(df, 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-2018VfL WolfsburgBorussia Dortmund"],
            "Season": ["2017-2018"],
            "Home Team": ["VfL Wolfsburg"],
            "Home Coach": ["Andries Jonker"],
            "col": ["Borussia Dortmund"],
            "Away Coach": ["Peter Bosz"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Coach_Substituted_Within_Last_OFFSET_Games(df, 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-2018VfL WolfsburgBorussia Dortmund"],
            "Season": ["2017-2018"],
            "Home Team": ["VfL Wolfsburg"],
            "Home Coach": ["Andries Jonker"],
            "Away Team": ["Borussia Dortmund"],
            "col": ["Peter Bosz"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Coach_Substituted_Within_Last_OFFSET_Games(df, 3)

    df = pd.read_csv(BASE_PATH, index_col=0, dtype={"Matchweek": np.int32})

    df = eng.add_Coach_Substituted_Within_Last_OFFSET_Games(df, 3)
    col_home = "Home Coach Substituted Within Last 3 Games"
    col_away = "Away Coach Substituted Within Last 3 Games"

    game_key = "2017-08-19VfL WolfsburgBorussia Dortmund"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == False
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == False

    game_key = "2017-09-17Bayer 04 LeverkusenSC Freiburg"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == False
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == True


def test_add_Points():
    with pytest.raises(KeyError):
        data = {"col": ["H"]}
        df = pd.DataFrame(data=data)
        df = eng.add_Points(df)

    with pytest.raises(ValueError):
        data = {"Result": ["X"]}
        df = pd.DataFrame(data=data)
        df = eng.add_Points(df)

    df = pd.read_csv(BASE_PATH, index_col=0)

    df = eng.add_Points(df)
    col_home = "Home Points"
    col_away = "Away Points"

    game_key = "2017-08-19VfL WolfsburgBorussia Dortmund"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == 0
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == 3

    game_key = "2017-08-26Borussia DortmundHertha BSC"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == 3
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == 0

    game_key = "2017-09-09SC FreiburgBorussia Dortmund"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == 1
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == 1

    game_key = "2017-09-17Borussia Dortmund1. FC Köln"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == -1
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == -1


def test_add_feat_Current_Position_Before_Matchday():
    with pytest.raises(KeyError):
        data = {
            "col": [""],
            "Away Team": [""],
            "Home Points": [""],
            "Away Points": [""],
            "Home Goals": [""],
            "Away Goals": [""],
            "Season": [""],
            "Competition": [""],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Current_Position_Before_Matchday(df, 3)

    with pytest.raises(KeyError):
        data = {
            "Home Team": [""],
            "col": [""],
            "Home Points": [""],
            "Away Points": [""],
            "Home Goals": [""],
            "Away Goals": [""],
            "Season": [""],
            "Competition": [""],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Current_Position_Before_Matchday(df, 3)

    with pytest.raises(KeyError):
        data = {
            "Home Team": [""],
            "Away Team": [""],
            "col": [""],
            "Away Points": [""],
            "Home Goals": [""],
            "Away Goals": [""],
            "Season": [""],
            "Competition": [""],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Current_Position_Before_Matchday(df, 3)

    with pytest.raises(KeyError):
        data = {
            "Home Team": [""],
            "Away Team": [""],
            "Home Points": [""],
            "col": [""],
            "Home Goals": [""],
            "Away Goals": [""],
            "Season": [""],
            "Competition": [""],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Current_Position_Before_Matchday(df, 3)

    with pytest.raises(KeyError):
        data = {
            "Home Team": [""],
            "Away Team": [""],
            "Home Points": [""],
            "Away Points": [""],
            "col": [""],
            "Away Goals": [""],
            "Season": [""],
            "Competition": [""],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Current_Position_Before_Matchday(df, 3)

    with pytest.raises(KeyError):
        data = {
            "Home Team": [""],
            "Away Team": [""],
            "Home Points": [""],
            "Away Points": [""],
            "Home Goals": [""],
            "col": [""],
            "Season": [""],
            "Competition": [""],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Current_Position_Before_Matchday(df, 3)

    with pytest.raises(KeyError):
        data = {
            "Home Team": [""],
            "Away Team": [""],
            "Home Points": [""],
            "Away Points": [""],
            "Home Goals": [""],
            "Away Goals": [""],
            "col": [""],
            "Competition": [""],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Current_Position_Before_Matchday(df, 3)

    with pytest.raises(KeyError):
        data = {
            "Home Team": [""],
            "Away Team": [""],
            "Home Points": [""],
            "Away Points": [""],
            "Home Goals": [""],
            "Away Goals": [""],
            "Season": [""],
            "col": [""],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Current_Position_Before_Matchday(df, 3)

    with pytest.raises(ValueError):
        data = {
            "Home Team": ["VfL Wolfsburg"],
            "Away Team": ["Borussia Dortmund"],
            "Home Points": ["A"],
            "Away Points": [3],
            "Home Goals": [0],
            "Away Goals": [3],
            "Season": ["2017-2018"],
            "Competition": ["Bundesliga"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Current_Position_Before_Matchday(df, 3)

    with pytest.raises(ValueError):
        data = {
            "Home Team": ["VfL Wolfsburg"],
            "Away Team": ["Borussia Dortmund"],
            "Home Points": [1],
            "Away Points": ["A"],
            "Home Goals": [0],
            "Away Goals": [3],
            "Season": ["2017-2018"],
            "Competition": ["Bundesliga"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Current_Position_Before_Matchday(df, 3)

    with pytest.raises(ValueError):
        data = {
            "Home Team": ["VfL Wolfsburg"],
            "Away Team": ["Borussia Dortmund"],
            "Home Points": [1],
            "Away Points": [3],
            "Home Goals": ["A"],
            "Away Goals": [3],
            "Season": ["2017-2018"],
            "Competition": ["Bundesliga"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Current_Position_Before_Matchday(df, 3)

    with pytest.raises(ValueError):
        data = {
            "Home Team": ["VfL Wolfsburg"],
            "Away Team": ["Borussia Dortmund"],
            "Home Points": [1],
            "Away Points": [3],
            "Home Goals": [0],
            "Away Goals": ["A"],
            "Season": ["2017-2018"],
            "Competition": ["Bundesliga"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_Current_Position_Before_Matchday(df, 3)

    df = pd.read_csv(BASE_PATH, index_col=0)

    df = eng.add_Current_Position_Before_Matchday(df, 3)
    home = "Home Current Position Before Matchday"
    away = "Away Current Position Before Matchday"

    game_key = "2017-08-19VfL WolfsburgBorussia Dortmund"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][home] == -1
    assert df.loc[df["Primary Key"] == game_key].iloc[0][away] == -1

    game_key = "2017-09-17Bayer 04 LeverkusenSC Freiburg"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][home] == 17
    assert df.loc[df["Primary Key"] == game_key].iloc[0][away] == 15

    game_key = "2017-09-17Borussia Dortmund1. FC Köln"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][home] == "UNKNOWN"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][away] == "UNKNOWN"


def test_add_Kick_Off_Before_17_00():
    with pytest.raises(KeyError):
        data = {"col": [""]}
        df = pd.DataFrame(data=data)
        df = eng.add_Kick_Off_Before_17_00(df)

    with pytest.raises(ValueError):
        data = {"Kick Off": ["15:30:00"]}
        df = pd.DataFrame(data=data)
        df = eng.add_Kick_Off_Before_17_00(df)

    df = pd.read_csv(BASE_PATH, index_col=0)

    df = eng.add_Kick_Off_Before_17_00(df)
    col = "Kick Off Before 17:00"

    game_key = "2017-08-19Hertha BSCVfB Stuttgart"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col] == True

    game_key = "2017-09-17Borussia Dortmund1. FC Köln"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col] == False


def test_add_Promoted_Last_Year():
    with pytest.raises(KeyError):
        data = {
            "col": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Season": "2017-2018",
        }
        df = pd.DataFrame(data=data)
        data = {"Team": ["VfB Stuttgart"], "Is Promoted": ["2017-2018"]}
        df_promotions = pd.DataFrame(data=data)
        df = eng.add_Promoted_Last_Year(df, df_promotions)

    with pytest.raises(KeyError):
        data = {
            "Home Team": ["Hertha BSC"],
            "col": ["VfB Stuttgart"],
            "Season": "2017-2018",
        }
        df = pd.DataFrame(data=data)
        data = {"Team": ["VfB Stuttgart"], "Is Promoted": ["2017-2018"]}
        df_promotions = pd.DataFrame(data=data)
        df = eng.add_Promoted_Last_Year(df, df_promotions)

    with pytest.raises(KeyError):
        data = {
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "col": "2017-2018",
        }
        df = pd.DataFrame(data=data)
        data = {"Team": ["VfB Stuttgart"], "Is Promoted": ["2017-2018"]}
        df_promotions = pd.DataFrame(data=data)
        df = eng.add_Promoted_Last_Year(df, df_promotions)

    with pytest.raises(ValueError):
        data = {
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Season": "2017-2018a",
        }
        df = pd.DataFrame(data=data)
        data = {"Team": ["VfB Stuttgart"], "Is Promoted": ["2017-2018"]}
        df_promotions = pd.DataFrame(data=data)
        df = eng.add_Promoted_Last_Year(df, df_promotions)

    with pytest.raises(KeyError):
        data = {
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Season": "2017-2018",
        }
        df = pd.DataFrame(data=data)
        data = {"col": ["VfB Stuttgart"], "Is Promoted": ["2017-2018"]}
        df_promotions = pd.DataFrame(data=data)
        df = eng.add_Promoted_Last_Year(df, df_promotions)

    with pytest.raises(KeyError):
        data = {
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Season": "2017-2018",
        }
        df = pd.DataFrame(data=data)
        data = {"Team": ["VfB Stuttgart"], "col": ["2017-2018"]}
        df_promotions = pd.DataFrame(data=data)
        df = eng.add_Promoted_Last_Year(df, df_promotions)

    with pytest.raises(ValueError):
        data = {
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Season": "2017-2018",
        }
        df = pd.DataFrame(data=data)
        data = {"Team": ["VfB Stuttgart"], "Is Promoted": ["2017-2018a"]}
        df_promotions = pd.DataFrame(data=data)
        df = eng.add_Promoted_Last_Year(df, df_promotions)

    df = pd.read_csv(BASE_PATH, index_col=0)
    df_promotions = pd.read_csv(PROMOTIONS_PATH, index_col=0)

    df = eng.add_Promoted_Last_Year(df, df_promotions)
    col_home = "Home Promoted Last Year"
    col_away = "Away Promoted Last Year"

    game_key = "2017-08-19Hertha BSCVfB Stuttgart"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == False
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == True

    game_key = "2017-09-17Borussia Dortmund1. FC Köln"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == "UNKNOWN"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == "UNKNOWN"


def test_add_MA_FEAT_Last_OFFSET_Games_Before_Matchday():
    with pytest.raises(KeyError):
        data = {
            "col": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MA_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "col": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MA_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "col": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MA_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "col": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MA_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "col": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MA_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "col": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MA_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(ValueError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": ["A"],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MA_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(ValueError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": ["A"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MA_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    df = pd.read_csv(BASE_PATH, index_col=0)

    df = eng.add_MA_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)
    col_home = "Home MA Test Last 3 Games Before Matchday"
    col_away = "Away MA Test Last 3 Games Before Matchday"

    game_key = "2017-08-19Hertha BSCVfB Stuttgart"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == -1.0
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == -1.0

    game_key = "2017-08-251. FC KölnHamburger SV"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == 3
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == 3

    game_key = "2017-09-17Bayer 04 LeverkusenSC Freiburg"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == round(7 / 3, 2)
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == round(12 / 3, 2)


def test_add_MA_FEAT_Against_Last_OFFSET_Games_Before_Matchday():
    with pytest.raises(KeyError):
        data = {
            "col": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "col": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "col": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "col": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "col": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "col": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(ValueError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": ["A"],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(ValueError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": ["A"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    df = pd.read_csv(BASE_PATH, index_col=0)

    df = eng.add_MA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)
    col_home = "Home MA Test Against Last 3 Games Before Matchday"
    col_away = "Away MA Test Against Last 3 Games Before Matchday"

    game_key = "2017-08-19Hertha BSCVfB Stuttgart"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == -1.0
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == -1.0

    game_key = "2017-08-251. FC KölnHamburger SV"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == 1
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == 2

    game_key = "2017-09-17Bayer 04 LeverkusenSC Freiburg"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == round(7 / 3, 2)
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == round(6 / 3, 2)


def test_add_EWMA_FEAT_Last_OFFSET_Games_Before_Matchday():
    with pytest.raises(KeyError):
        data = {
            "col": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_EWMA_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "col": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_EWMA_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "col": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_EWMA_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "col": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_EWMA_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "col": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_EWMA_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "col": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_EWMA_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(ValueError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": ["A"],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_EWMA_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(ValueError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": ["A"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_EWMA_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    df = pd.read_csv(BASE_PATH, index_col=0)

    df = eng.add_EWMA_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)
    col_home = "Home EWMA Test Last 3 Games Before Matchday"
    col_away = "Away EWMA Test Last 3 Games Before Matchday"

    game_key = "2017-08-19Hertha BSCVfB Stuttgart"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == -1
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == -1

    game_key = "2017-08-251. FC KölnHamburger SV"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == 3
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == 3

    game_key = "2017-09-17Bayer 04 LeverkusenSC Freiburg"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == 2.14
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == 4.0


def test_add_EWMA_FEAT_Against_Last_OFFSET_Games_Before_Matchday():
    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "col": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_EWMA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "col": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_EWMA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "col": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_EWMA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "col": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_EWMA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "col": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_EWMA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(ValueError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": ["A"],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_EWMA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(ValueError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": ["A"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_EWMA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    df = pd.read_csv(BASE_PATH, index_col=0)

    df = eng.add_EWMA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)
    col_home = "Home EWMA Test Against Last 3 Games Before Matchday"
    col_away = "Away EWMA Test Against Last 3 Games Before Matchday"

    game_key = "2017-08-19Hertha BSCVfB Stuttgart"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == -1
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == -1

    game_key = "2017-08-251. FC KölnHamburger SV"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == 1
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == 2

    game_key = "2017-09-17Bayer 04 LeverkusenSC Freiburg"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == 1.71
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == 1.71


def test_add_MAX_FEAT_Last_OFFSET_Games_Before_Matchday():
    with pytest.raises(KeyError):
        data = {
            "col": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MAX_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "col": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MAX_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "col": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MAX_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "col": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MAX_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "col": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MAX_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "col": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MAX_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(ValueError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": ["A"],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MAX_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(ValueError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": ["A"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MAX_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    df = pd.read_csv(BASE_PATH, index_col=0)

    df = eng.add_MAX_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)
    col_home = "Home MAX Test Last 3 Games Before Matchday"
    col_away = "Away MAX Test Last 3 Games Before Matchday"

    game_key = "2017-08-19Hertha BSCVfB Stuttgart"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == -1.0
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == -1.0

    game_key = "2017-08-251. FC KölnHamburger SV"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == 3
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == 3

    game_key = "2017-09-17Bayer 04 LeverkusenSC Freiburg"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == 5
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == 4


def test_add_MAX_FEAT_Against_Last_OFFSET_Games_Before_Matchday():
    with pytest.raises(KeyError):
        data = {
            "col": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MAX_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "col": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MAX_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "col": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MAX_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "col": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MAX_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "col": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MAX_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "col": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MAX_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(ValueError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": ["A"],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MAX_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(ValueError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": ["A"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MAX_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    df = pd.read_csv(BASE_PATH, index_col=0)

    df = eng.add_MAX_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)
    col_home = "Home MAX Test Against Last 3 Games Before Matchday"
    col_away = "Away MAX Test Against Last 3 Games Before Matchday"

    game_key = "2017-08-19Hertha BSCVfB Stuttgart"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == -1.0
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == -1.0

    game_key = "2017-08-251. FC KölnHamburger SV"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == 1
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == 2

    game_key = "2017-09-17Bayer 04 LeverkusenSC Freiburg"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == 4
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == 3


def test_add_MIN_FEAT_Last_OFFSET_Games_Before_Matchday():
    with pytest.raises(KeyError):
        data = {
            "col": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MIN_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "col": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MIN_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "col": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MIN_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "col": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MIN_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "col": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MIN_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "col": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MIN_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(ValueError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": ["A"],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MIN_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(ValueError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": ["A"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MIN_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    df = pd.read_csv(BASE_PATH, index_col=0)

    df = eng.add_MIN_FEAT_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)
    col_home = "Home MIN Test Last 3 Games Before Matchday"
    col_away = "Away MIN Test Last 3 Games Before Matchday"

    game_key = "2017-08-19Hertha BSCVfB Stuttgart"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == -1.0
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == -1.0

    game_key = "2017-08-251. FC KölnHamburger SV"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == 3
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == 3

    game_key = "2017-09-17Bayer 04 LeverkusenSC Freiburg"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == 1
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == 4


def test_add_MIN_FEAT_Against_Last_OFFSET_Games_Before_Matchday():
    with pytest.raises(KeyError):
        data = {
            "col": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MIN_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "col": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MIN_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "col": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MIN_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "col": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MIN_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "col": [4],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MIN_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(KeyError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "col": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MIN_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(ValueError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": ["A"],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MIN_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    with pytest.raises(ValueError):
        data = {
            "Primary Key": ["2017-08-19Hertha BSCVfB Stuttgart"],
            "Season": ["2017-2018"],
            "Home Team": ["Hertha BSC"],
            "Away Team": ["VfB Stuttgart"],
            "Home Test": [4],
            "Away Test": ["A"],
        }
        df = pd.DataFrame(data=data)
        df = eng.add_MIN_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)

    df = pd.read_csv(BASE_PATH, index_col=0)

    df = eng.add_MIN_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, "Test", 3)
    col_home = "Home MIN Test Against Last 3 Games Before Matchday"
    col_away = "Away MIN Test Against Last 3 Games Before Matchday"

    game_key = "2017-08-19Hertha BSCVfB Stuttgart"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == -1.0
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == -1.0

    game_key = "2017-08-251. FC KölnHamburger SV"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == 1
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == 2

    game_key = "2017-09-17Bayer 04 LeverkusenSC Freiburg"
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_home] == 1
    assert df.loc[df["Primary Key"] == game_key].iloc[0][col_away] == 1


def test_set_maximum():
    with pytest.raises(KeyError):
        data = {
            "col": [1],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.set_maximum(df, "Test", 1)

    with pytest.raises(KeyError):
        data = {
            "Home Test": [1],
            "col": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.set_maximum(df, "Test", 1)

    with pytest.raises(ValueError):
        data = {
            "Home Test": [np.nan],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.set_maximum(df, "Test", 1)

    with pytest.raises(ValueError):
        data = {
            "Home Test": [1],
            "Away Test": [np.nan],
        }
        df = pd.DataFrame(data=data)
        df = eng.set_maximum(df, "Test", 1)

    with pytest.raises(ValueError):
        data = {
            "Home Test": ["A"],
            "Away Test": [1],
        }
        df = pd.DataFrame(data=data)
        df = eng.set_maximum(df, "Test", 1)

    with pytest.raises(ValueError):
        data = {
            "Home Test": [1],
            "Away Test": ["A"],
        }
        df = pd.DataFrame(data=data)
        df = eng.set_maximum(df, "Test", 1)

    data = {
        "Home Test": [1, 2, 10, 20, -1],
        "Away Test": [4, 3, 2, 200, -4],
    }
    df = pd.DataFrame(data=data)
    df = eng.set_maximum(df, "Test", 8)

    home = [1, 2, 8, 8, -1]
    for row, result in zip(df.iterrows(), home):
        assert row[1]["Home Test"] == result
    away = [4, 3, 2, 8, -4]
    for row, result in zip(df.iterrows(), away):
        assert row[1]["Away Test"] == result
