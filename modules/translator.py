import os.path
import re

import pandas as pd

this_directory = os.path.abspath(os.path.dirname(__file__))


def fbref_com_translations():
    """
    provides team translations from www.fbref.com

    returns: dictionary - official team names to corresponding identifiers from
    source

    raises: KeyError
    """
    data = pd.read_excel(f"{this_directory}/translator_data.ods")
    result = {}

    for index, row in data.iterrows():
        team = row["Team"]
        translation = row["www.fbref.com"]

        if team in result.keys():
            raise KeyError("Key already exists")

        if not isinstance(translation, float):
            result.update({team: translation})

    return result


def fbref_com_links():
    """
    provides partial links from www.fbref.com

    returns: dictionary - official team names to partial links from source

    raises: KeyError
    """
    data = pd.read_excel(f"{this_directory}/translator_data.ods")
    result = {}

    for index, row in data.iterrows():
        team = row["Team"]
        link = row["www.fbref.com Link"]

        if team in result.keys():
            raise KeyError("Key already exists")

        if not isinstance(link, float):
            result.update({team: link})

    return result


def fbref_com_features():
    """
    provides features from www.fbref.com plus corresponding invalid values

    returns: dictionary - feature identifier to invalid values
    """
    fbref_com_features = {
        "Home Team": "UNKNOWN",
        "Away Team": "UNKNOWN",
        "Home xG": -1.0,
        "Away xG": -1.0,
        "Home Possesion": -1.0,
        "Away Possesion": -1.0,
        "Home Goals": -1.0,
        "Away Goals": -1.0,
        "Result": "UNKNOWN",
        "Day": "UNKNOWN",
        "Kick Off": "UNKNOWN",
        "Matchweek": -1.0,
        "Competition": "UNKNOWN",
        "Date": "UNKNOWN",
        "Season": "UNKNOWN",
        "Primary Key": "2022-01-01UNKNOWNUNKNOWN",
        "Notes": "UNKNOWN",
    }
    return fbref_com_features


def football_data_co_uk_translations():
    """
    provides team translations from www.football-data.co.uk

    returns: dictionary - official team names to corresponding identifiers from
    source

    raises: KeyError
    """
    data = pd.read_excel(f"{this_directory}/translator_data.ods")
    result = {}

    for index, row in data.iterrows():
        team = row["Team"]
        translation = row["www.football-data.co.uk"]

        if team in result.keys():
            raise KeyError("Key already exists")

        if not isinstance(translation, float):
            result.update({team: translation})

    return result


def football_data_co_uk_columns():
    """
    provides column translations from www.football-data.co.uk

    returns: dictionary - identifier from source to target naming
    """
    football_data_co_uk_columns = {
        "HS": "Home Shots",
        "AS": "Away Shots",
        "HST": "Home Shots on Target",
        "AST": "Away Shots on Target",
        "HF": "Home Fouls Committed",
        "AF": "Away Fouls Committed",
        "HC": "Home Corners",
        "AC": "Away Corners",
        "HY": "Home Yellow Cards",
        "AY": "Away Yellow Cards",
        "HR": "Home Red Cards",
        "AR": "Away Red Cards",
        "B365H": "Home Odds",
        "B365D": "Deuce Odds",
        "B365A": "Away Odds",
        "Primary Key": "Primary Key",
    }
    return football_data_co_uk_columns


def weltfussball_de_links():
    """
    provides partial links from www.weltfussball.de

    returns: dictionary - official team names to partial links from source

    raises: KeyError
    """
    data = pd.read_excel(f"{this_directory}/translator_data.ods")
    result = {}

    for index, row in data.iterrows():
        team = row["Team"]
        link = row["www.weltfussball.de Link"]

        if team in result.keys():
            raise KeyError("Key already exists")

        if not isinstance(link, float):
            result.update({team: link})

    return result


def get_following_season(season):
    r"""
    calculates the following season, if format ^\d{2}.\d{2}$ (e. g. 16-17) is
    given

    returns: the following season in the proper format ^\d{2}/\d{2}$
    (e. g. 17/18)

    raises: ValueError
    """
    regex = r"^\d{2}.\d{2}$"
    if not re.compile(regex).search(season):
        raise ValueError

    start = int(season[:2])
    end = int(season[3:])

    if start == 98 and end != 99:
        raise ValueError
    if start == 98 and end == 99:
        return "99/00"

    if start == 99 and end != 0:
        raise ValueError
    if start == 99 and end == 0:
        return "00/01"

    if start + 1 != end:
        raise ValueError

    start = start + 1
    if start < 10:
        start = f"0{start}"
    end = end + 1
    if end < 10:
        end = f"0{end}"

    return f"{start}/{end}"


def soccerbase_com_translations():
    """
    provides team translations from www.soccerbase.com

    returns: dictionary - official team names to corresponding identifiers from
    source

    raises: KeyError
    """
    data = pd.read_excel(f"{this_directory}/translator_data.ods")
    result = {}

    for index, row in data.iterrows():
        team = row["Team"]
        translation = row["www.soccerbase.com"]

        if team in result.keys():
            raise KeyError("Key already exists")

        if not isinstance(translation, float):
            result.update({team: translation})

    return result


def competitions():
    """
    provides relevant competitions

    returns: ['Bundesliga, 'Premier League', 'La Liga', 'Serie A', 'Ligue 1']
    """
    competitions = ["Bundesliga", "Premier League", "La Liga", "Serie A", "Ligue 1"]
    return competitions


def month_eng_str_to_int():
    """
    translates month

    returns: dictionary - english string representation (Jan-Dec) to int
    representation (1-12)
    """
    month_eng_str_to_int = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }
    return month_eng_str_to_int


def day_int_to_ger_str():
    """
    translates day

    returns: dictionary - int representation (0-6) to german string
    representation (Mo.-So.)
    """
    day_int_to_ger_str = {
        0: "Mo.",
        1: "Di.",
        2: "Mi.",
        3: "Do.",
        4: "Fr.",
        5: "Sa.",
        6: "So.",
    }
    return day_int_to_ger_str


def day_ger_str_to_eng_str():
    """
    translates day

    returns: dictionary - german string representation (Mo.-So.) to english
    string representation (MO-SU)
    """
    day_ger_str_to_eng_str = {
        "Mo.": "MO",
        "Di.": "TU",
        "Mi.": "WE",
        "Do.": "TH",
        "Fr.": "FR",
        "Sa.": "SA",
        "So.": "SU",
    }
    return day_ger_str_to_eng_str
