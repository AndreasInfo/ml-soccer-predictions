import datetime as dt

import numpy as np
import pandas as pd
import pytest

import modules.collector as coll


def test_prepare_Kick_Off():
    with pytest.raises(KeyError):
        data = {"col": ["15:30"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Kick_Off(df)

    with pytest.raises(ValueError):
        data = {"Uhrzeit": ["abcdefg"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Kick_Off(df)

    data = {"Uhrzeit": ["15:30", "18:30 (19:30)", np.nan]}
    df = pd.DataFrame(data=data)
    result = ["15:30", "18:30", "UNKNOWN"]
    df = coll.prepare_Kick_Off(df)
    for value, result in zip(df["Kick Off"], result):
        assert value == result


def test_prepare_Result():
    with pytest.raises(KeyError):
        data = {"col": ["S"], "Spielort": ["Heim"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Result(df)

    with pytest.raises(KeyError):
        data = {"Ergebnis": ["S"], "col": ["Heim"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Result(df)

    with pytest.raises(ValueError):
        data = {"Ergebnis": ["X"], "Spielort": ["Heim"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Result(df)

    with pytest.raises(ValueError):
        data = {"Ergebnis": ["S"], "Spielort": ["XXX"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Result(df)

    data = {
        "Ergebnis": ["S", "U", "N", "N", "S", "U", np.nan, np.nan, np.nan],
        "Spielort": [
            "Heim",
            "Neutral",
            "Auswärts",
            "Heim",
            "Neutral",
            "Auswärts",
            "Heim",
            "Neutral",
            "Auswärts",
        ],
    }
    df = pd.DataFrame(data=data)
    result = ["H", "D", "H", "A", "H", "D", "UNKNOWN", "UNKNOWN", "UNKNOWN"]
    df = coll.prepare_Result(df)
    for value, result in zip(df["Result"], result):
        assert value == result


def test_prepare_Teams():
    with pytest.raises(KeyError):
        data = {
            "col": ["Borussia Dortmund"],
            "Gegner": ["VfL Wolfsburg"],
            "Spielort": ["Heim"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_Teams(df)

    with pytest.raises(KeyError):
        data = {
            "Mannschaft": ["Borussia Dortmund"],
            "col": ["VfL Wolfsburg"],
            "Spielort": ["Heim"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_Teams(df)

    with pytest.raises(KeyError):
        data = {
            "Mannschaft": ["Borussia Dortmund"],
            "Gegner": ["VfL Wolfsburg"],
            "col": ["Heim"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_Teams(df)

    with pytest.raises(ValueError):
        data = {
            "Mannschaft": ["Borussia Dortmund"],
            "Gegner": ["VfL Wolfsburg"],
            "Spielort": ["XXX"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_Teams(df)

    data = {
        "Mannschaft": [
            "Borussia Dortmund",
            "VfL Wolfsburg",
            "FC Bayern München",
            np.nan,
            "Borussia Dortmund",
        ],
        "Gegner": [
            "VfL Wolfsburg",
            "FC Bayern München",
            "Borussia Dortmund",
            "VfL Wolfsburg",
            np.nan,
        ],
        "Spielort": ["Heim", "Neutral", "Auswärts", "Heim", "Neutral"],
    }
    df = pd.DataFrame(data=data)
    result_home = [
        "Borussia Dortmund",
        "VfL Wolfsburg",
        "Borussia Dortmund",
        "UNKNOWN",
        "Borussia Dortmund",
    ]
    df = coll.prepare_Teams(df)
    for value, result in zip(df["Home Team"], result_home):
        assert value == result

    result_away = [
        "VfL Wolfsburg",
        "FC Bayern München",
        "FC Bayern München",
        "VfL Wolfsburg",
        "UNKNOWN",
    ]
    for value, result in zip(df["Away Team"], result_away):
        assert value == result


def test_prepare_Possesions():
    with pytest.raises(KeyError):
        data = {
            "col": [50],
            "Spielort": ["Heim"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_Possesions(df)

    with pytest.raises(KeyError):
        data = {
            "Besitz": [50],
            "col": ["Heim"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_Possesions(df)

    with pytest.raises(ValueError):
        data = {
            "Besitz": ["50.0"],
            "Spielort": ["Heim"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_Possesions(df)

    with pytest.raises(ValueError):
        data = {
            "Besitz": [50],
            "Spielort": ["XXX"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_Possesions(df)

    data = {
        "Besitz": [50, 60, 70, np.nan],
        "Spielort": ["Heim", "Neutral", "Auswärts", "Heim"],
    }
    df = pd.DataFrame(data=data)
    result_home = [50.0, 60.0, 30.0, -1.0]
    df = coll.prepare_Possesions(df)
    for value, result in zip(df["Home Possesion"], result_home):
        assert value == result

    result_away = [50.0, 40.0, 70.0, -1.0]
    for value, result in zip(df["Away Possesion"], result_away):
        assert value == result


def test_prepare_xGs():
    with pytest.raises(KeyError):
        data = {
            "col": [1.0],
            "xGA": [1.0],
            "Spielort": ["Heim"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_xGs(df)

    with pytest.raises(KeyError):
        data = {
            "xG": [1.0],
            "col": [1.0],
            "Spielort": ["Heim"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_xGs(df)

    with pytest.raises(KeyError):
        data = {
            "xG": [1.0],
            "xGA": [1.0],
            "col": ["Heim"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_xGs(df)

    with pytest.raises(ValueError):
        data = {
            "xG": ["1.0"],
            "xGA": [1.0],
            "Spielort": ["Heim"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_xGs(df)

    with pytest.raises(ValueError):
        data = {
            "xG": [1.0],
            "xGA": ["1.0"],
            "Spielort": ["Heim"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_xGs(df)

    with pytest.raises(ValueError):
        data = {
            "xG": [1.0],
            "xGA": [1.0],
            "Spielort": ["XXX"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_xGs(df)

    data = {
        "xG": [1.0, 1.5, 1.7, np.nan],
        "xGA": [1.0, 0.5, np.nan, 1.0],
        "Spielort": ["Heim", "Neutral", "Auswärts", "Heim"],
    }
    df = pd.DataFrame(data=data)
    result_home = [1.0, 1.5, -1.0, -1.0]
    df = coll.prepare_xGs(df)
    for value, result in zip(df["Home xG"], result_home):
        assert value == result

    result_away = [1.0, 0.5, 1.7, 1.0]
    for value, result in zip(df["Away xG"], result_away):
        assert value == result


def test_prepare_Goals():
    with pytest.raises(KeyError):
        data = {
            "col": [0],
            "Tk": [0],
            "Spielort": ["Heim"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_Goals(df)

    with pytest.raises(KeyError):
        data = {
            "Tf": [0],
            "col": [0],
            "Spielort": ["Heim"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_Goals(df)

    with pytest.raises(KeyError):
        data = {
            "Tf": [0],
            "Tk": [0],
            "col": ["Heim"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_Goals(df)

    with pytest.raises(ValueError):
        data = {
            "Tf": ["A"],
            "Tk": [0],
            "Spielort": ["Heim"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_Goals(df)

    with pytest.raises(ValueError):
        data = {
            "Tf": [0],
            "Tk": ["A"],
            "Spielort": ["Heim"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_Goals(df)

    with pytest.raises(ValueError):
        data = {
            "Tf": [0],
            "Tk": [0],
            "Spielort": ["XXX"],
        }
        df = pd.DataFrame(data=data)
        df = coll.prepare_Goals(df)

    data = {
        "Tf": [1, 2, 3, np.nan],
        "Tk": [4, 5, np.nan, "0 (6)"],
        "Spielort": ["Heim", "Neutral", "Auswärts", "Heim"],
    }
    df = pd.DataFrame(data=data)
    result_home = [1.0, 2.0, -1.0, -1.0]
    df = coll.prepare_Goals(df)
    for value, result in zip(df["Home Goals"], result_home):
        assert value == result

    result_away = [4.0, 5.0, 3.0, 6.0]
    for value, result in zip(df["Away Goals"], result_away):
        assert value == result


def test_prepare_Date():
    with pytest.raises(KeyError):
        data = {"col": ["01.01.2022"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Date(df, "Datum")

    with pytest.raises(ValueError):
        data = {"Datum": ["01/01/20222"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Date(df, "Datum")

    data = {"Datum": ["01.01.2022", "01/01/2022", "01/01/22", np.nan]}
    df = pd.DataFrame(data=data)
    result = [
        dt.datetime(2022, 1, 1),
        dt.datetime(2022, 1, 1),
        dt.datetime(2022, 1, 1),
        "UNKNOWN",
    ]
    df = coll.prepare_Date(df, "Datum")
    for value, result in zip(df["Date"], result):
        assert value == result


def test_prepare_Matchweek():
    with pytest.raises(KeyError):
        data = {"Wett": ["Bundesliga"], "col": ["Spielwoche 1"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Matchweek(df, "Runde", "Wett")

    with pytest.raises(KeyError):
        data = {"col": ["Bundesliga"], "Runde": ["Spielwoche 1"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Matchweek(df, "Runde", "Wett")

    with pytest.raises(ValueError):
        data = {"Wett": ["Bundesliga"], "Runde": [""]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Matchweek(df, "Runde", "Wett")

    with pytest.raises(ValueError):
        data = {"Wett": ["Bundesliga"], "Runde": ["Spielwoche 0"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Matchweek(df, "Runde", "Wett")

    with pytest.raises(ValueError):
        data = {"Wett": ["Bundesliga"], "Runde": ["Spielwoche 1a"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Matchweek(df, "Runde", "Wett")

    with pytest.raises(ValueError):
        data = {"Wett": ["Bundesliga"], "Runde": ["Spielwoche 100"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Matchweek(df, "Runde", "Wett")

    data = {
        "Wett": [
            "Bundesliga",
            "Premier League",
            "La Liga",
            "Serie A",
            "Ligue 1",
            "Champions League",
        ],
        "Runde": [
            "Spielwoche 1",
            "Spielwoche 2",
            "Spielwoche 3",
            "Spielwoche 98",
            "Spielwoche 99",
            "Finale",
        ],
    }
    df = pd.DataFrame(data=data)
    result = [1, 2, 3, 98, 99, -1]
    df = coll.prepare_Matchweek(df, "Runde", "Wett")
    for value, result in zip(df["Matchweek"], result):
        assert value == result


def test_prepare_Day():
    with pytest.raises(KeyError):
        data = {"col": ["Mo."]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Day(df, "Tag")

    with pytest.raises(ValueError):
        data = {"Tag": ["XXX"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Day(df, "Tag")

    data = {"Tag": ["Mo.", "Di.", "Mi.", "Do.", "Fr.", "Sa.", "So.", np.nan]}
    df = pd.DataFrame(data=data)
    result = ["MO", "TU", "WE", "TH", "FR", "SA", "SU", "UNKNOWN"]
    df = coll.prepare_Day(df, "Tag")
    for value, result in zip(df["Day"], result):
        assert value == result


def test_prepare_Season():
    with pytest.raises(KeyError):
        data = {"col": ["2021-2022"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Season(df, "Saison")

    with pytest.raises(ValueError):
        data = {"Saison": ["XXX"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Season(df, "Saison")

    with pytest.raises(ValueError):
        data = {"Saison": ["2021-2023"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Season(df, "Saison")

    data = {"Saison": ["2021-2022", np.nan]}
    df = pd.DataFrame(data=data)
    result = ["2021-2022", "UNKNOWN"]
    df = coll.prepare_Season(df, "Saison")
    for value, result in zip(df["Season"], result):
        assert value == result


def test_prepare_Competition():
    with pytest.raises(KeyError):
        data = {"col": ["Bundesliga"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Competition(df, "Wett")

    data = {
        "Wett": [
            "Bundesliga",
            "Premier League",
            "La Liga",
            "Serie A",
            "Ligue 1",
            "XXX",
            np.nan,
        ]
    }
    df = pd.DataFrame(data=data)
    result = [
        "Bundesliga",
        "Premier League",
        "La Liga",
        "Serie A",
        "Ligue 1",
        "UNKNOWN",
        "UNKNOWN",
    ]
    df = coll.prepare_Competition(df, "Wett")
    for value, result in zip(df["Competition"], result):
        assert value == result


def test_prepare_Notes():
    with pytest.raises(KeyError):
        data = {"col": ["ABC"]}
        df = pd.DataFrame(data=data)
        df = coll.prepare_Notes(df, "Hinweise")

    data = {
        "Hinweise": [
            "Test",
            "ABC",
            "123",
            np.nan,
        ]
    }
    df = pd.DataFrame(data=data)
    result = [
        "Test",
        "ABC",
        "123",
        "UNKNOWN",
    ]
    df = coll.prepare_Notes(df, "Hinweise")
    for value, result in zip(df["Notes"], result):
        assert value == result


def test_introduce_Primary_Key():
    with pytest.raises(KeyError):
        data = {
            "col": [dt.datetime(2022, 1, 1)],
            "Home Team": ["Borussia Dortmund"],
            "Away Team": ["VfL Wolfsburg"],
        }
        df = pd.DataFrame(data=data)
        df = coll.introduce_Primary_Key(df, "Date", "Home Team", "Away Team")

    with pytest.raises(KeyError):
        data = {
            "Date": [dt.datetime(2022, 1, 1)],
            "col": ["Borussia Dortmund"],
            "Away Team": ["VfL Wolfsburg"],
        }
        df = pd.DataFrame(data=data)
        df = coll.introduce_Primary_Key(df, "Date", "Home Team", "Away Team")

    with pytest.raises(KeyError):
        data = {
            "Date": [dt.datetime(2022, 1, 1)],
            "Home Team": ["Borussia Dortmund"],
            "col": ["VfL Wolfsburg"],
        }
        df = pd.DataFrame(data=data)
        df = coll.introduce_Primary_Key(df, "Date", "Home Team", "Away Team")

    with pytest.raises(ValueError):
        data = {
            "Date": ["2022-01-01"],
            "Home Team": ["Borussia Dortmund"],
            "Away Team": ["VfL Wolfsburg"],
        }
        df = pd.DataFrame(data=data)
        df = coll.introduce_Primary_Key(df, "Date", "Home Team", "Away Team")

    data = {
        "Date": [
            dt.datetime(2022, 1, 1),
            dt.datetime(2022, 1, 2),
            dt.datetime(2022, 1, 3),
        ],
        "Home Team": ["Borussia Dortmund", "VfL Wolfsburg", np.nan],
        "Away Team": ["VfL Wolfsburg", np.nan, "SC Freiburg"],
    }
    df = pd.DataFrame(data=data)
    df = coll.introduce_Primary_Key(df, "Date", "Home Team", "Away Team")

    result = [
        "2022-01-01Borussia DortmundVfL Wolfsburg",
        "2022-01-02VfL WolfsburgUNKNOWN",
        "2022-01-03UNKNOWNSC Freiburg",
    ]
    for value, result in zip(df["Primary Key"], result):
        assert value == result
