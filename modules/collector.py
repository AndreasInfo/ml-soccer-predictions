import datetime as dt
import re

import pandas as pd

import modules.translator as trans

ERR_MSG = "Something stinks. This should have been overwritten!"
UNKNOWN_STRING = "UNKNOWN"
UNKNOWN_FLOAT = -1.0
HASH_VALUE_1 = "4309875807432890756789243502387469874968743290743632460987890643"
HASH_VALUE_2 = "2987498579844444987237987888898234759237495087234095723498572345"


class BrokenAlgorithmException(Exception):
    pass


def prepare_Kick_Off(df):
    r"""
    Sets feature "Kick Off" based on "Uhrzeit" of a given dataframe. New
    values of feature is string in format ^\d{2}:\d{2}$. If "Uhrzeit" is null,
    value will be set to "UNKNOWN". "Uhrzeit" will be dropped.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Uhrzeit" is not present
    ValueError
        when "Uhrzeit" can not be repaired
    """

    col_old = "Uhrzeit"
    col_new = "Kick Off"

    if not set([col_old]).issubset(df.columns):
        raise KeyError

    df[col_new] = ERR_MSG

    for index, row in df.iterrows():
        time = row[col_old]

        if pd.isnull(time):
            df.at[index, col_new] = UNKNOWN_STRING
            continue

        if re.compile("^\d{2}:\d{2}$").match(time):
            df.at[index, col_new] = time
            continue

        new_time = time[:5]
        if not re.compile("^\d{2}:\d{2}$").match(new_time):
            raise ValueError
        df.at[index, col_new] = time[:5]

    df.drop(columns=[col_old], inplace=True)
    if (df[col_new] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


def prepare_Result(df):
    r"""
    Sets feature "Result" based on "Ergebnis" and "Spielort" of a given
    dataframe. New values of feature is in ["H", "D", "A"]. If "Ergebnis" is
    null, value will be set to "UNKNOWN". "Ergebnis" will be dropped.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Ergebnis" or "Spielort is not present
    ValueError
        when "Ergebnis" is not in ["S", "U", "N"]
    ValueError
        when "Spielort" is not in ["Heim", "Neutral", "Auswärts"]
    """

    col_old = "Ergebnis"
    col_new = "Result"

    if not set(["Ergebnis", "Spielort"]).issubset(df.columns):
        raise KeyError

    df[col_new] = ERR_MSG

    for index, row in df.iterrows():
        venue = row["Spielort"]
        result = row[col_old]

        if venue == "Heim" or venue == "Neutral":
            if pd.isnull(result):
                result = UNKNOWN_STRING
            elif result == "S":
                result = "H"
            elif result == "U":
                result = "D"
            elif result == "N":
                result = "A"
            else:
                raise ValueError
        elif venue == "Auswärts":
            if pd.isnull(result):
                result = UNKNOWN_STRING
            elif result == "S":
                result = "A"
            elif result == "U":
                result = "D"
            elif result == "N":
                result = "H"
            else:
                ValueError
        else:
            raise ValueError

        df.at[index, col_new] = result

    df.drop(columns=[col_old], inplace=True)
    if (df[col_new] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


def prepare_Teams(df):
    """
    Sets features "Home Team" and "Away Team" based on "Mannschaft", "Gegner"
    and "Spielort" of a given dataframe. New values of features are strings.
    If "Mannschaft" respectively "Gegner" are null, values will be set to
    "UNKNOWN". "Mannschaft" and "Gegner" will be dropped.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Mannschaft", "Gegner" or "Spielort" is not present
    ValueError
        when "Spielort" is not in ["Heim", "Neutral", "Auswärts"]
    """

    col_home = "Home Team"
    col_away = "Away Team"

    if not set(["Mannschaft", "Gegner", "Spielort"]).issubset(df.columns):
        raise KeyError

    df[col_home] = ERR_MSG
    df[col_away] = ERR_MSG

    home_team = ""
    away_team = ""
    for index, row in df.iterrows():
        venue = row["Spielort"]

        if venue == "Heim" or venue == "Neutral":
            if pd.isnull(row["Mannschaft"]):
                home_team = UNKNOWN_STRING
            else:
                home_team = row["Mannschaft"]
            if pd.isnull(row["Gegner"]):
                away_team = UNKNOWN_STRING
            else:
                away_team = row["Gegner"]
        elif venue == "Auswärts":
            if pd.isnull(row["Gegner"]):
                home_team = UNKNOWN_STRING
            else:
                home_team = row["Gegner"]
            if pd.isnull(row["Mannschaft"]):
                away_team = UNKNOWN_STRING
            else:
                away_team = row["Mannschaft"]
        else:
            raise ValueError

        df.at[index, col_home] = home_team
        df.at[index, col_away] = away_team

    df.drop(columns=["Mannschaft", "Gegner"], inplace=True)
    if (df[col_home] == ERR_MSG).any() or (df[col_away] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


def prepare_Possesions(df):
    """
    Sets features "Home Possesion" and "Away Possesion" based on "Besitz" and
    "Spielort" of a given dataframe. New values of features are floats. If
    "Besitz" is null, values will be set to -1. "Besitz" will be dropped.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Besitz" or "Spielort" is not present
    ValueError
        when "Besitz" is not type int or float
    ValueError
        when "Spielort" is not in ["Heim", "Neutral", "Auswärts"]
    """

    col_home = "Home Possesion"
    col_away = "Away Possesion"

    if not set(["Besitz", "Spielort"]).issubset(df.columns):
        raise KeyError

    df[col_home] = ERR_MSG
    df[col_away] = ERR_MSG

    home_possesion = ""
    away_possesion = ""
    for index, row in df.iterrows():
        venue = row["Spielort"]

        possesion = row["Besitz"]

        if venue == "Heim" or venue == "Neutral":
            if pd.isnull(possesion):
                home_possesion = UNKNOWN_FLOAT
                away_possesion = UNKNOWN_FLOAT
            elif not isinstance(possesion, (int, float)):
                raise ValueError
            else:
                home_possesion = possesion
                away_possesion = 100 - int(possesion)
        elif venue == "Auswärts":
            if pd.isnull(possesion):
                home_possesion = UNKNOWN_FLOAT
                away_possesion = UNKNOWN_FLOAT
            elif not isinstance(possesion, (int, float)):
                raise ValueError
            else:
                home_possesion = 100 - int(possesion)
                away_possesion = possesion
        else:
            raise ValueError

        df.at[index, col_home] = home_possesion
        df.at[index, col_away] = away_possesion

    df.drop(columns=["Besitz"], inplace=True)
    if (df[col_home] == ERR_MSG).any() or (df[col_away] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


def prepare_xGs(df):
    """
    Sets features "Home xG" and "Away xG" based on "xG" and "xGA" and
    "Spielort" of a given dataframe. New values of features are floats. If
    "xG" respectively "xGA" is null, values will be set to -1.0. "xG" and
    "xGA" will be dropped.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "xG", "xGA" or "Spielort" is not present
    ValueError
        when "xG" or "xGA" are not type int or float
    ValueError
        when "Spielort" is not in ["Heim", "Neutral", "Auswärts"]
    """

    col_home = "Home xG"
    col_away = "Away xG"

    if not set(["xG", "xGA", "Spielort"]).issubset(df.columns):
        raise KeyError

    df[col_home] = ERR_MSG
    df[col_away] = ERR_MSG

    home_xG = ""
    away_xG = ""
    for index, row in df.iterrows():
        venue = row["Spielort"]

        xG = row["xG"]
        xGA = row["xGA"]

        if venue == "Heim" or venue == "Neutral":
            if pd.isnull(xG):
                home_xG = UNKNOWN_FLOAT
            elif not isinstance(xG, (int, float)):
                raise ValueError
            else:
                home_xG = xG
            if pd.isnull(xGA):
                away_xG = UNKNOWN_FLOAT
            elif not isinstance(xGA, (int, float)):
                raise ValueError
            else:
                away_xG = xGA
        elif venue == "Auswärts":
            if pd.isnull(xGA):
                home_xG = UNKNOWN_FLOAT
            elif not isinstance(xGA, (int, float)):
                raise ValueError
            else:
                home_xG = xGA
            if pd.isnull(xG):
                away_xG = UNKNOWN_FLOAT
            elif not isinstance(xG, (int, float)):
                raise ValueError
            else:
                away_xG = xG
        else:
            raise ValueError

        df.at[index, col_home] = home_xG
        df.at[index, col_away] = away_xG

    df.drop(columns=["xG", "xGA"], inplace=True)
    if (df[col_home] == ERR_MSG).any() or (df[col_away] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


def prepare_Goals(df):
    """
    Sets features "Home Goals" and "Away Goals" based on "Tf" and "Tk" and
    "Spielort" of a given dataframe. New values of features are floats. If
    "Tf" respectively "Tk" is null, values will be set to -1.0. Penalties will
    be counted as well! "Tf" and "Tk" will be dropped.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Tf", Tk or "Spielort" is not present
    ValueError
        when "xG" or "xGA" are not type int or float
    ValueError
        when "Spielort" is not in ["Heim", "Neutral", "Auswärts"]
    """

    col_home = "Home Goals"
    col_away = "Away Goals"

    if not set(["Tf", "Tk", "Spielort"]).issubset(df.columns):
        raise KeyError

    df[col_home] = ERR_MSG
    df[col_away] = ERR_MSG

    home_goals = ""
    away_goals = ""
    for index, row in df.iterrows():
        regex_penalties = "^(\d{0,2} \(\d{1,2}\))$"
        regex_numeric = "^\d{1,2}(\.\d)?$"
        venue = row["Spielort"]

        # fix penalties, e.g format "0 (5)"
        tF = str(row["Tf"])
        if re.compile(regex_penalties).match(tF):
            tF = tF[tF.find("(") + 1 : tF.find(")")]
        tK = str(row["Tk"])
        if re.compile(regex_penalties).match(tK):
            tK = tK[tK.find("(") + 1 : tK.find(")")]

        if venue == "Heim" or venue == "Neutral":
            if tF == "nan":
                home_goals = UNKNOWN_FLOAT
            elif not re.compile(regex_numeric).match(tF):
                raise ValueError
            else:
                home_goals = float(tF)
            if tK == "nan":
                away_goals = UNKNOWN_FLOAT
            elif not re.compile(regex_numeric).match(tK):
                raise ValueError
            else:
                away_goals = float(tK)

        elif venue == "Auswärts":
            if tF == "nan":
                away_goals = UNKNOWN_FLOAT
            elif not re.compile(regex_numeric).match(tF):
                raise ValueError
            else:
                away_goals = float(tF)
            if tK == "nan":
                home_goals = UNKNOWN_FLOAT
            elif not re.compile(regex_numeric).match(tK):
                raise ValueError
            else:
                home_goals = float(tK)
        else:
            raise ValueError

        df.at[index, col_home] = home_goals
        df.at[index, col_away] = away_goals

    df.drop(columns=["Tf", "Tk"], inplace=True)
    if (df[col_home] == ERR_MSG).any() or (df[col_away] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


def prepare_Date(df, col_date):
    """
    Sets feature "Date" based on col_date (formatted as dd.mm.yyyy, dd/mm/yyyy
    or dd/mm/yy) of a given dataframe. New values of feature are type
    datetime. If col_date is null, values will be set to "UNKNOWN". col_date
    will be dropped.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    col_date : string

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when col_date is not present
    ValueError
        when col_date can not be parsed from %d.%m.%Y, "%d/%m/%Y" or
        "%d/%m/%y"
    """

    helper = HASH_VALUE_1

    if not set([col_date]).issubset(df.columns):
        raise KeyError

    df[helper] = ERR_MSG

    d_m_Y_dotted = "^\d{2}\.\d{2}\.\d{4}$"  # dd.mm.yyyy
    d_m_Y_slashed = "^\d{2}\/\d{2}\/\d{4}$"  # dd/mm/yyyy
    d_m_y_slashed = "^\d{2}\/\d{2}\/\d{2}$"  # dd/mm/yy

    for index, row in df.iterrows():
        date = row[col_date]

        if pd.isnull(date):
            date = UNKNOWN_STRING
        elif re.compile(d_m_Y_dotted).search(date):
            date = dt.datetime.strptime(date, "%d.%m.%Y")
        elif re.compile(d_m_Y_slashed).search(date):
            date = dt.datetime.strptime(date, "%d/%m/%Y")
        elif re.compile(d_m_y_slashed).search(date):
            date = dt.datetime.strptime(date, "%d/%m/%y")
        else:
            raise ValueError

        df.at[index, helper] = date

    df.drop(columns=[col_date], inplace=True)
    df.rename(columns={helper: "Date"}, inplace=True)
    if (df["Date"] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


def prepare_Matchweek(df, col_round, col_competition):
    r"""
    Sets feature "Matchweek" based on col_round and col_competition of a given
    dataframe. It cuts prefix "Spielwoche " from col_round, if col_competition
    is in modules.translator.competitions(). New values of feature are floats
    between 1-99 or -1, if col_competition is not in
    modules.translator.competitions().

    Parameters
    ----------
    df : pandas.core.frame.DataFrame

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when col_round or col_competition is not present

    ValueError
        when col_competition is in modules.translator.competitions() and
        col_round does not match regex ^Spielwoche [1-9]{1}\d{0,1}$
    """

    if not set([col_round, col_competition]).issubset(df.columns):
        raise KeyError

    df[HASH_VALUE_1] = ERR_MSG

    prefix = "Spielwoche "
    regex = r"^Spielwoche [1-9]{1}\d{0,1}$"

    for index, row in df.iterrows():
        matchweek = row[col_round]
        competition = row[col_competition]

        if competition not in trans.competitions():
            df.at[index, HASH_VALUE_1] = UNKNOWN_FLOAT
            continue
        if not re.compile(regex).search(str(matchweek)):
            raise ValueError

        df.at[index, HASH_VALUE_1] = float(matchweek[len(prefix) :])

    df.drop(columns=[col_round], inplace=True)
    df.rename(columns={HASH_VALUE_1: "Matchweek"}, inplace=True)
    if (df["Matchweek"] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


def prepare_Day(df, col_day):
    r"""
    Sets feature "Day" based on col_day of a given dataframe. New values of
    feature are strings in ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]. If
    col_day is null, values, will be set to "UNKNOWN". col_day will be
    deleted.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when col_day is not present

    ValueError
        when col_day is not in modules.translator.competitions()
    """

    if not set([col_day]).issubset(df.columns):
        raise KeyError

    df[HASH_VALUE_1] = ERR_MSG

    for index, row in df.iterrows():
        day = row[col_day]

        if pd.isnull(day):
            df.at[index, HASH_VALUE_1] = UNKNOWN_STRING
            continue

        result = trans.day_ger_str_to_eng_str().get(day)

        if result is None:
            raise ValueError
        else:
            df.at[index, HASH_VALUE_1] = result

    df.drop(columns=[col_day], inplace=True)
    df.rename(columns={HASH_VALUE_1: "Day"}, inplace=True)
    if (df["Day"] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


def prepare_Season(df, col_season):
    """
    Sets feature "Season" based on col_season (formatted as yyyy-yyyy) of a
    given dataframe. New values of feature are strings. If col_season is null,
    values will be set to "UNKNOWN". col_season will be dropped.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    col_season : string

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when col_season is not present
    ValueError
        when col_season can not be parsed from yyyy-yyyyy
    """

    helper = HASH_VALUE_1

    if not set([col_season]).issubset(df.columns):
        raise KeyError

    df[helper] = ERR_MSG

    regex = "^\d{4}-\d{4}$"  # yyyy-yyyy

    for index, row in df.iterrows():
        season = row[col_season]

        if pd.isnull(season):
            season = UNKNOWN_STRING
        elif re.compile(regex).search(season):
            start = season[:4]
            end = season[5:]
            if not int(start) == int(end) - 1:
                raise ValueError
        else:
            raise ValueError

        df.at[index, helper] = season

    df.drop(columns=[col_season], inplace=True)
    df.rename(columns={helper: "Season"}, inplace=True)
    if (df["Season"] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


def prepare_Competition(df, col_competition):
    """
    Sets feature "Competition" based on col_competition of a given dataframe.
    New values of feature are strings in modules.translator.competitions(). If
    col_competition is null or invalid, values will be set to "UNKNOWN".
    col_competition will be dropped.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    col_competition : string

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when col_competition is not present
    """

    helper = HASH_VALUE_1

    if not set([col_competition]).issubset(df.columns):
        raise KeyError

    df[helper] = ERR_MSG

    for index, row in df.iterrows():
        competition = row[col_competition]

        if pd.isnull(competition):
            competition = UNKNOWN_STRING
        elif not competition in trans.competitions():
            competition = UNKNOWN_STRING

        df.at[index, helper] = competition

    df.drop(columns=[col_competition], inplace=True)
    df.rename(columns={helper: "Competition"}, inplace=True)
    if (df["Competition"] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


def prepare_Notes(df, col_notes):
    """
    Sets feature "Notes" based on col_notes of a given dataframe. New values
    of feature are strings. If col_notes is null, values will be set to
    "UNKNOWN". col_notes will be dropped.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    col_notes : string

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when col_notes is not present
    """

    helper = HASH_VALUE_1

    if not set([col_notes]).issubset(df.columns):
        raise KeyError

    df[helper] = ERR_MSG

    for index, row in df.iterrows():
        competition = row[col_notes]

        if pd.isnull(competition):
            competition = UNKNOWN_STRING

        df.at[index, helper] = competition

    df.drop(columns=[col_notes], inplace=True)
    df.rename(columns={helper: "Notes"}, inplace=True)
    if (df["Notes"] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


def introduce_Primary_Key(df, col_date, col_home, col_away):
    """
    Sets feature "Primary Key" based on col_date, col_home and col_away of a
    given dataframe. New values of feature are strings. col_date, col_home and
    col_away are simply concatenated. If one value is null, it will be
    replaced by "UNKNOWN".

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    col_date : string
    col_home : string
    col_away : string

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when col_date, col_home or col_away is not present
    ValueError
        when col_date is not type datetime
    """

    helper = HASH_VALUE_1

    if not set([col_date, col_home, col_away]).issubset(df.columns):
        raise KeyError

    df[helper] = ERR_MSG

    for index, row in df.iterrows():
        date = row[col_date]

        if not isinstance(date, dt.datetime):
            raise ValueError
        else:
            date = date.strftime("%Y-%m-%d")

        home = row[col_home]
        if pd.isnull(home):
            home = UNKNOWN_STRING
        away = row[col_away]
        if pd.isnull(away):
            away = UNKNOWN_STRING

        df.at[index, helper] = f"{date}{home}{away}"

    df.rename(columns={helper: "Primary Key"}, inplace=True)
    if (df["Primary Key"] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df
