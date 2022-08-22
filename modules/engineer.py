import datetime as dt

import numpy as np
import pandas as pd

import modules.helper as helper
import modules.features as feat

ERR_MSG = "Something stinks. This should have been overwritten!"


class BrokenAlgorithmException(Exception):
    pass


def report_execution_time(func):
    """
    Decorator that reports the execution time.
    """

    def wrap(*args, **kwargs):
        start = dt.datetime.now()
        result = func(*args, **kwargs)
        end = dt.datetime.now()

        print(f"{func.__name__: <60} -> {end - start}")
        return result

    return wrap


@report_execution_time
def add_Days_Since_Last_Game(df):
    """
    Adds features "Home Days Since Last Game" and "Away Days Since Last Game"
    based on "Primary Key", "Home Team", "Away Team" and "Date". Values of new
    features are positive integers. Values are set to -1, if last game is not
    present. This function DOES NOT prevent overlaps between seasons.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Primary Key", "Home Team", "Away Team", "Date" or "Season" are
        not present
    ValueError
        when "Date" is not type datetime or not convertable to datetime

    """
    FEATURE = "Date"
    DAY_IN_NS = 1 * 24 * 60 * 60 * 1e9

    cols = [
        "Primary Key",
        "Home Team",
        "Away Team",
        "Date",
    ]
    if not set(cols).issubset(df.columns):
        raise KeyError

    # raises ValueError
    df[FEATURE] = pd.to_datetime(df[FEATURE])
    # parse to ns since epoch
    df[FEATURE] = df[FEATURE].astype(np.int64)

    col_home = "Home Days Since Last Game"
    col_away = "Away Days Since Last Game"

    df[col_home] = ERR_MSG
    df[col_away] = ERR_MSG

    df.sort_values(by=["Primary Key"], inplace=True)
    df.reset_index(inplace=True, drop=True)

    for team in np.unique(df[["Home Team", "Away Team"]]):
        games = df.loc[((df["Home Team"] == team) | (df["Away Team"] == team))][cols]

        values = games[FEATURE].to_frame()
        values.reset_index(inplace=True)
        values.rename(columns={"index": "Game"}, inplace=True)
        values["Team"] = team

        # RESTRUCTURE GAMES
        games = (
            games.rename_axis(index="Game", columns="Venue").stack().rename("Team").reset_index()
        )

        # CALCULATE FEATURE
        values[FEATURE] = (values[FEATURE] - values[FEATURE].shift(1)).fillna(-DAY_IN_NS)

        # BUILD RESULT
        result = (
            games.merge(values, on=["Game", "Team"], how="left")
            .set_index(["Game", "Venue"])
            .unstack()
        )

        left = result["Team"].reset_index()
        right = (
            result[FEATURE][["Away Team", "Home Team"]]
            .rename(columns={"Home Team": col_home, "Away Team": col_away})
            .reset_index(drop=True)
        )
        result = pd.concat([left, right], axis=1)

        # UPDATE DF
        df.update(
            result.set_index("Primary Key").reindex(df.set_index("Primary Key").index).reset_index()
        )

    # parse ns to date/days
    df[FEATURE] = pd.to_datetime(df[FEATURE])
    df[col_home] = df[col_home] / 1e9 / 60 / 60 / 24
    df[col_away] = df[col_away] / 1e9 / 60 / 60 / 24

    if (df[col_home] == ERR_MSG).any() or (df[col_away] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


@report_execution_time
def add_Coach(df, df_coach):
    """
    Adds features "Home Coach" and "Away Coach" based on "Home Team", "Away
    Team" and "Date" of a given dataframe. A second dataframe with "Team",
    "Coach", "Started", "Ended" has to be provided. Values of new features are
    strings or "UNKNOWN", if no corresponding coach is present. If there are
    multiple coaches possible, the first one in the provided coaches will be
    selected. If features "Home Coach" and "Away Coach" already exist, they
    will be deleted first.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    df_coach : pandas.core.frame.DataFrame

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Home Team", "Away Team" or "Date" is not present in df
    TypeError
        when "Date" is not type datetime in df
    KeyError
        when "Team", "Coach", "Started", or "Ended" is not present in df_coach
    TypeError
        when "Started" or "Ended" is not type datetime in df_coach
    """
    if not set(["Home Team", "Away Team", "Date"]).issubset(df.columns):
        raise KeyError

    cols = ["Date"]
    if not set(cols).issubset(df.select_dtypes(include=["datetime"]).columns):
        raise TypeError

    if not set(["Team", "Coach", "Started", "Ended"]).issubset(df_coach.columns):
        raise KeyError

    cols = ["Started", "Ended"]
    if not set(cols).issubset(df_coach.select_dtypes(include=["datetime"]).columns):
        raise TypeError

    col_home = "Home Coach"
    col_away = "Away Coach"

    df[col_home] = ERR_MSG
    df[col_away] = ERR_MSG

    def do(df, df_coach, side):
        df.drop(columns=[f"{side} Coach"], errors="ignore", inplace=True)
        tmp = df.copy(deep=True)

        df = pd.merge(df, df_coach, how="left", left_on=f"{side} Team", right_on="Team")
        df = df.loc[
            (df["Started"] <= df["Date"])
            & (df["Date"] <= df["Ended"])
            & (df[f"{side} Team"] == df["Team"])
        ]
        rename_cols = {"Coach": f"{side} Coach"}
        df.rename(columns=rename_cols, inplace=True)
        df.drop(columns=["Team", "Started", "Ended"], inplace=True)

        df = pd.merge(tmp, df[["Primary Key", f"{side} Coach"]], on="Primary Key", how="left")
        df[f"{side} Coach"].fillna("UNKNOWN", inplace=True)

        return df

    df = do(df, df_coach, "Home")
    df = do(df, df_coach, "Away")

    df.drop_duplicates(subset=["Primary Key"], keep="first", inplace=True)

    df.sort_values(by=["Primary Key"], inplace=True)
    df.reset_index(inplace=True, drop=True)

    if (df[col_home] == ERR_MSG).any() or (df[col_away] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


@report_execution_time
def add_Coach_Substituted_Within_Last_OFFSET_Games(df, offset):
    """
    Adds features "Home Coach Substituted Within Last OFFSET Games" and "Away
    Coach Substituted Within Last OFFSET Games" based on "Primary Key", "Home
    Team", "Away Team", "Home Coach", "Away Coach" and "Season". Values of new
    features are booleans. For simplicity, the first offset rows of each
    season are set to False, because this function prevents overlaps between
    seasons.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    offset : integer

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Primary Key", "Home Team", "Away Team", "Home Coach", "Away
        Coach" or "Season" are not present
    """
    FEATURE = "Coach"

    cols = [
        "Primary Key",
        "Home Team",
        "Away Team",
        "Home Coach",
        "Away Coach",
        "Season",
    ]
    if not set(cols).issubset(df.columns):
        raise KeyError

    col_home = f"Home Coach Substituted Within Last {offset} Games"
    col_away = f"Away Coach Substituted Within Last {offset} Games"

    df[col_home] = ERR_MSG
    df[col_away] = ERR_MSG

    df.sort_values(by=["Primary Key"], inplace=True)
    df.reset_index(inplace=True, drop=True)

    for team in np.unique(df[["Home Team", "Away Team"]]):
        tmp = df.loc[((df["Home Team"] == team) | (df["Away Team"] == team))][cols]
        for season in tmp["Season"].unique():
            # GET DATA
            games = tmp.loc[tmp["Season"] == season]
            values = helper.extract_feature_per_team(games, FEATURE, team, False)

            # RESTRUCTURE GAMES
            games = (
                games.rename_axis(index="Game", columns="Venue")
                .stack()
                .rename("Team")
                .reset_index()
            )

            # CALCULATE FEATURE
            values[FEATURE] = values[FEATURE] != values[FEATURE].shift(offset)
            values.at[: offset - 1, FEATURE] = False

            # BUILD RESULT
            result = (
                games.merge(values, on=["Game", "Team"], how="left")
                .set_index(["Game", "Venue"])
                .unstack()
            )

            left = result["Team"].reset_index()
            right = (
                result[FEATURE][["Away Team", "Home Team"]]
                .rename(columns={"Home Team": col_home, "Away Team": col_away})
                .reset_index(drop=True)
            )
            result = pd.concat([left, right], axis=1)

            # UPDATE DF
            df.update(
                result.set_index("Primary Key")
                .reindex(df.set_index("Primary Key").index)
                .reset_index()
            )

    if (df[col_home] == ERR_MSG).any() or (df[col_away] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


@report_execution_time
def add_Points(df):
    """
    Adds features "Home Points" and "Away Points" based on "Result" of a given
    dataframe. Value of new features are integers in [0, 1, 3] or -1, if
    "Result" is "" or NaN.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Result" is not present
    ValueError
        when "Result" is not in ["H", "D", "A", "", NaN]
    """
    col_home = "Home Points"
    col_away = "Away Points"

    df[col_home] = ERR_MSG
    df[col_away] = ERR_MSG

    for index, row in df.iterrows():
        result = row["Result"]

        # checks string against NaN. wtf!
        if result != result:
            result = ""

        if result not in ["H", "D", "A", ""]:
            raise ValueError

        if result == "H":
            df.at[index, col_home] = 3
            df.at[index, col_away] = 0
        elif result == "D":
            df.at[index, col_home] = 1
            df.at[index, col_away] = 1
        elif result == "A":
            df.at[index, col_home] = 0
            df.at[index, col_away] = 3
        elif result == "":
            df.at[index, col_home] = -1
            df.at[index, col_away] = -1

    df[col_home] = df[col_home].astype(int)
    df[col_away] = df[col_away].astype(int)

    if (df[col_home] == ERR_MSG).any() or (df[col_away] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


@report_execution_time
def add_Promoted_Last_Year(df, df_promotions):
    """
    Adds features "Home Promoted Last Year" and "Away Promoted Last Year"
    based on "Home Team", "Away Team" and "Season" of a given dataframe. A
    second dataframe with "Team" and "Is Promoted" has to be provided. Values
    of new features are booleans or UNKNOWN, if features can not be
    determined.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    df_promotions : pandas.core.frame.DataFrame

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Home Team", "Away Team" or "Season" is not present in df
    ValueError
        when "Season" does not match regex ^\d{4}-\d{4}$ in df
    KeyError
        when "Team" and "Is Promoted" is not present in df_promotions
    ValueError
        when "Is Promoted" does not match regex ^\d{4}-\d{4}$ in df_promotions
    """
    regex = r"^\d{4}-\d{4}$"

    cols = ["Home Team", "Away Team", "Season"]
    if not set(cols).issubset(df.columns):
        raise KeyError

    if not df["Season"].str.contains(regex, regex=True).all():
        raise ValueError

    cols = ["Team", "Is Promoted"]
    if not set(cols).issubset(df_promotions.columns):
        raise KeyError

    if not df_promotions["Is Promoted"].str.contains(regex, regex=True).all():
        raise ValueError

    col_home = "Home Promoted Last Year"
    col_away = "Away Promoted Last Year"

    df[col_home] = ERR_MSG
    df[col_away] = ERR_MSG

    for index, row in df.iterrows():
        observed_season = row["Season"]
        helper = df_promotions.loc[(df_promotions["Is Promoted"] == observed_season)]

        observed_team = row["Home Team"]
        if helper.empty:
            df.at[index, col_home] = "UNKNOWN"
        elif observed_team in list(helper["Team"]):
            df.at[index, col_home] = True
        else:
            df.at[index, col_home] = False

        observed_team = row["Away Team"]
        if helper.empty:
            df.at[index, col_away] = "UNKNOWN"
        elif observed_team in list(helper["Team"]):
            df.at[index, col_away] = True
        else:
            df.at[index, col_away] = False

    if (df[col_home] == ERR_MSG).any() or (df[col_away] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


@report_execution_time
def add_Kick_Off_Before_17_00(df):
    """
    Adds feature "Kick Off Before 17:00" based on "Kick Off" of a given
    dataframe. Value of new feature is boolean.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Kick Off" is not present
    ValueError:
        when "Kick Off" does not match regex ^\d{2}:\d{2}$
        type int
    """
    cols = ["Kick Off"]
    if not set(cols).issubset(df.columns):
        raise KeyError

    regex = r"^\d{2}:\d{2}$"
    if not df["Kick Off"].str.contains(regex, regex=True).all():
        raise ValueError

    col = "Kick Off Before 17:00"

    df[col] = ERR_MSG
    border = 17

    for index, row in df.iterrows():
        kick_off = row["Kick Off"]
        if int(kick_off[:2]) < border:
            df.at[index, col] = True
        else:
            df.at[index, col] = False

    if (df[col] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


@report_execution_time
def add_Current_Position_Before_Matchday(df, offset):
    """
    Adds features "Home Current Position Before Matchday" and "Away Current
    Position Before Matchday" based on "Home Team", "Away Team", "Home
    Points", "Away Points", "Home Goals", "Away Goals", "Season" and
    "Competition" of a given dataframe. Values of new features are integers or
    -1, if Matchweek is less or equal than offset or "UNKNOWN", if feature
    could not have been calculated.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    offset : integer

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Home Team", "Away Team", "Home Points", "Away Points", "Home
        Goals", "Away Goals", "Season" or "Competition" are not present
    ValueError:
        when "Home Points", "Home Points", "Home Goals", "Home Goals" are not
        type int
    """
    cols = [
        "Home Team",
        "Away Team",
        "Home Points",
        "Away Points",
        "Home Goals",
        "Away Goals",
        "Season",
        "Competition",
    ]
    if not set(cols).issubset(df.columns):
        raise KeyError

    # raises ValueError
    df["Home Points"].fillna(-1, inplace=True)
    df["Home Points"] = df["Home Points"].astype(int)
    df["Away Points"].fillna(-1, inplace=True)
    df["Away Points"] = df["Away Points"].astype(int)
    df["Home Goals"].fillna(-1, inplace=True)
    df["Home Goals"] = df["Home Goals"].astype(int)
    df["Away Goals"].fillna(-1, inplace=True)
    df["Away Goals"] = df["Away Goals"].astype(int)

    home = "Home Current Position Before Matchday"
    away = "Away Current Position Before Matchday"

    cols = [home, away]

    df[cols] = ERR_MSG

    for index, row in df.iterrows():
        matchweek = row["Matchweek"]
        if matchweek <= offset:
            for col in cols:
                df.at[index, col] = -1
            continue

        home_team = row["Home Team"]
        away_team = row["Away Team"]
        season = row["Season"]
        league = row["Competition"]

        matches_played = df.loc[
            (df["Season"] == season) & (df["Matchweek"] < matchweek) & (df["Competition"] == league)
        ]

        if matches_played.empty:
            for col in cols:
                df.at[index, col] = "UNKNOWN"
            continue

        # position in home table
        home_cols = ["Home Team", "Home Points", "Home Goals", "Away Goals"]
        home_table = matches_played[home_cols].groupby(by="Home Team").sum()
        home_table.rename(columns={"Away Goals": "Home Goals Against"}, inplace=True)

        # position in away table
        away_cols = ["Away Team", "Away Points", "Away Goals", "Home Goals"]
        away_table = matches_played[away_cols].groupby(by="Away Team").sum()
        away_table.rename(columns={"Home Goals": "Away Goals Against"}, inplace=True)

        # table
        table = home_table.append(away_table)

        table.fillna(0, inplace=True)
        table["Points"] = table["Home Points"] + table["Away Points"]
        table.drop(columns=["Home Points", "Away Points"], inplace=True)
        table["Goals"] = table["Home Goals"] + table["Away Goals"]
        table.drop(columns=["Home Goals", "Away Goals"], inplace=True)
        table["Goals Against"] = table["Home Goals Against"] + table["Away Goals Against"]
        table.drop(columns=["Home Goals Against", "Away Goals Against"], inplace=True)

        table["diff"] = table["Goals"] - table["Goals Against"]
        table = table.groupby(table.index).sum()
        table = table.sort_values(by=["Points", "diff", "Goals"], ascending=False)

        df.at[index, home] = table.index.get_loc(home_team) + 1
        df.at[index, away] = table.index.get_loc(away_team) + 1

    for col in cols:
        if (df[col] == ERR_MSG).any():
            raise BrokenAlgorithmException
    return df


@report_execution_time
def add_MA_FEAT_Last_OFFSET_Games_Before_Matchday(df, feature, offset):
    """
    MA = moving average

    Adds features "Home MA {feature} Last {offset} Games Before Matchday" and
    "Away MA {feature} Last {offset} Games Before Matchday" based on "Primary
    Key" , "Home Team", "Away Team", "Home {feature}", "Away {feature}" and
    "Season" for a given dataframe and offset. Values of new features are
    floats (rounded to 2 decimals). First row with uncalculable value is set
    to -1.0. Furthermore, this function prevents overlaps between saisons.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    feature : string
    offset : integer

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Primary Key", "Home Team", "Away Team", "Home {feature}", "Away
        {feature}" or "Season" are not present
    ValueError:
        when "Home {feature}" or "Away {feature}" is not type float
    """
    cols = [
        "Season",
        "Home Team",
        "Away Team",
        f"Home {feature}",
        f"Away {feature}",
        "Primary Key",
    ]
    if not set(cols).issubset(df.columns):
        raise KeyError

    df[f"Home {feature}"] = df[f"Home {feature}"].astype(float)
    df[f"Away {feature}"] = df[f"Away {feature}"].astype(float)

    col_home = f"Home MA {feature} Last {offset} Games Before Matchday"
    col_away = f"Away MA {feature} Last {offset} Games Before Matchday"

    df[col_home] = ERR_MSG
    df[col_away] = ERR_MSG

    df.sort_values(by=["Primary Key"], inplace=True)
    df.reset_index(inplace=True, drop=True)

    new_feat = df[[col_home, col_away]].copy(deep=True)

    for team in np.unique(df[["Home Team", "Away Team"]]):
        tmp = df.loc[((df["Home Team"] == team) | (df["Away Team"] == team))][cols]
        for season in tmp["Season"].unique():
            # GET DATA
            games = tmp.loc[tmp["Season"] == season]
            values = helper.extract_feature_per_team(games, feature, team, False)

            # RESTRUCTURE GAMES
            games = (
                games.rename_axis(index="Game", columns="Venue")
                .stack()
                .rename("Team")
                .reset_index()
            )

            # AGGREGATE FEATURE
            values[feature] = (
                values[feature].rolling(offset, min_periods=1).mean().shift(1).round(2).fillna(-1)
            )

            # BUILD RESULT
            result = (
                games.merge(values, on=["Game", "Team"], how="left")
                .set_index(["Game", "Venue"])
                .unstack()
            )

            left = result["Team"].reset_index()
            right = (
                result[feature][["Away Team", "Home Team"]]
                .rename(columns={"Home Team": col_home, "Away Team": col_away})
                .reset_index(drop=True)
            )
            result = pd.concat([left, right], axis=1)

            # UPDATE DF
            new_feat.update(
                result.set_index("Primary Key")
                .reindex(df.set_index("Primary Key").index)
                .reset_index()
            )

    df.update(new_feat)

    if (df[col_home] == ERR_MSG).any() or (df[col_away] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


@report_execution_time
def add_MA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, feature, offset):
    """
    MA = moving average

    Adds features "Home MA {feature} Against Last {offset} Games Before
    Matchday" and "Away MA {feature} Against Last {offset} Games Before
    Matchday" based on "Primary Key" , "Home Team", "Away Team", "Home
    {feature}", "Away {feature}" and "Season" for a given dataframe and
    offset. Values of new features are floats (rounded to 2 decimals). First
    row with uncalculable value is set to -1.0. Furthermore, this function
    prevents overlaps between saisons.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    feature : string
    offset : integer

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Primary Key", "Home Team", "Away Team", "Home {feature}", "Away
        {feature}" or "Season" are not present
    ValueError:
        when "Home {feature}" or "Away {feature}" is not type float
    """
    cols = [
        "Season",
        "Home Team",
        "Away Team",
        f"Home {feature}",
        f"Away {feature}",
        "Primary Key",
    ]
    if not set(cols).issubset(df.columns):
        raise KeyError

    df[f"Home {feature}"] = df[f"Home {feature}"].astype(float)
    df[f"Away {feature}"] = df[f"Away {feature}"].astype(float)

    col_home = f"Home MA {feature} Against Last {offset} Games Before Matchday"
    col_away = f"Away MA {feature} Against Last {offset} Games Before Matchday"

    df[col_home] = ERR_MSG
    df[col_away] = ERR_MSG

    df.sort_values(by=["Primary Key"], inplace=True)
    df.reset_index(inplace=True, drop=True)

    new_feat = df[[col_home, col_away]].copy(deep=True)

    for team in np.unique(df[["Home Team", "Away Team"]]):
        tmp = df.loc[((df["Home Team"] == team) | (df["Away Team"] == team))][cols]
        for season in tmp["Season"].unique():
            # GET DATA
            games = tmp.loc[tmp["Season"] == season]
            values = helper.extract_feature_per_team(games, feature, team, True)

            # RESTRUCTURE GAMES
            games = (
                games.rename_axis(index="Game", columns="Venue")
                .stack()
                .rename("Team")
                .reset_index()
            )

            # AGGREGATE FEATURE
            values[feature] = (
                values[feature].rolling(offset, min_periods=1).mean().shift(1).round(2).fillna(-1)
            )

            # BUILD RESULT
            result = (
                games.merge(values, on=["Game", "Team"], how="left")
                .set_index(["Game", "Venue"])
                .unstack()
            )

            left = result["Team"].reset_index()
            right = (
                result[feature][["Away Team", "Home Team"]]
                .rename(columns={"Home Team": col_home, "Away Team": col_away})
                .reset_index(drop=True)
            )
            result = pd.concat([left, right], axis=1)

            # UPDATE DF
            new_feat.update(
                result.set_index("Primary Key")
                .reindex(df.set_index("Primary Key").index)
                .reset_index()
            )

    df.update(new_feat)

    if (df[col_home] == ERR_MSG).any() or (df[col_away] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


@report_execution_time
def add_EWMA_FEAT_Last_OFFSET_Games_Before_Matchday(df, feature, offset):
    """
    EWMA = exponentially weighted moving average

    Adds features "Home EWMA {feature} Last {offset} Games Before Matchday"
    and "Away EWMA {feature} Last {offset} Games Before Matchday" based on
    "Primary Key" , "Home Team", "Away Team", "Home {feature}", "Away
    {feature}" and "Season" for a given dataframe and offset. Values of new
    features are floats (rounded to 2 decimals). First row with uncalculable
    value is set to -1.0. Furthermore, this function prevents overlaps between
    saisons.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    feature : string
    offset : integer

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Primary Key", "Home Team", "Away Team", "Home {feature}", "Away
        {feature}" or "Season" are not present
    ValueError:
        when "Home {feature}" or "Away {feature}" is not type float
    """
    cols = [
        "Season",
        "Home Team",
        "Away Team",
        f"Home {feature}",
        f"Away {feature}",
        "Primary Key",
    ]
    if not set(cols).issubset(df.columns):
        raise KeyError

    df[f"Home {feature}"] = df[f"Home {feature}"].astype(float)
    df[f"Away {feature}"] = df[f"Away {feature}"].astype(float)

    col_home = f"Home EWMA {feature} Last {offset} Games Before Matchday"
    col_away = f"Away EWMA {feature} Last {offset} Games Before Matchday"

    df[col_home] = ERR_MSG
    df[col_away] = ERR_MSG

    df.sort_values(by=["Primary Key"], inplace=True)
    df.reset_index(inplace=True, drop=True)

    new_feat = df[[col_home, col_away]].copy(deep=True)

    for team in np.unique(df[["Home Team", "Away Team"]]):
        tmp = df.loc[((df["Home Team"] == team) | (df["Away Team"] == team))][cols]
        for season in tmp["Season"].unique():
            # GET DATA
            games = tmp.loc[tmp["Season"] == season]
            values = helper.extract_feature_per_team(games, feature, team, False)

            # RESTRUCTURE GAMES
            games = (
                games.rename_axis(index="Game", columns="Venue")
                .stack()
                .rename("Team")
                .reset_index()
            )

            # AGGREGATE FEATURE
            values[feature] = values[feature].ewm(span=offset).mean().shift(1).round(2).fillna(-1)

            # BUILD RESULT
            result = (
                games.merge(values, on=["Game", "Team"], how="left")
                .set_index(["Game", "Venue"])
                .unstack()
            )

            left = result["Team"].reset_index()
            right = (
                result[feature][["Away Team", "Home Team"]]
                .rename(columns={"Home Team": col_home, "Away Team": col_away})
                .reset_index(drop=True)
            )
            result = pd.concat([left, right], axis=1)

            # UPDATE DF
            new_feat.update(
                result.set_index("Primary Key")
                .reindex(df.set_index("Primary Key").index)
                .reset_index()
            )

    df.update(new_feat)

    if (df[col_home] == ERR_MSG).any() or (df[col_away] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


@report_execution_time
def add_EWMA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, feature, offset):
    """
    EWMA = exponentially weighted moving average

    Adds features "Home EWMA {feature} Against Last {offset} Games Before
    Matchday" and "Away EWMA {feature} Against Last {offset} Games Before
    Matchday" based on "Primary Key" , "Home Team", "Away Team", "Home
    {feature}", "Away {feature}" and "Season" for a given dataframe and
    offset. Values of new features are floats (rounded to 2 decimals). First
    row with uncalculable value is set to -1.0. Furthermore, this function
    prevents overlaps between saisons.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    feature : string
    offset : integer

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Primary Key", "Home Team", "Away Team", "Home {feature}", "Away
        {feature}" or "Season" are not present
    ValueError:
        when "Home {feature}" or "Away {feature}" is not type float
    """
    cols = [
        "Season",
        "Home Team",
        "Away Team",
        f"Home {feature}",
        f"Away {feature}",
        "Primary Key",
    ]
    if not set(cols).issubset(df.columns):
        raise KeyError

    df[f"Home {feature}"] = df[f"Home {feature}"].astype(float)
    df[f"Away {feature}"] = df[f"Away {feature}"].astype(float)

    col_home = f"Home EWMA {feature} Against Last {offset} Games Before Matchday"
    col_away = f"Away EWMA {feature} Against Last {offset} Games Before Matchday"

    df[col_home] = ERR_MSG
    df[col_away] = ERR_MSG

    df.sort_values(by=["Primary Key"], inplace=True)
    df.reset_index(inplace=True, drop=True)

    new_feat = df[[col_home, col_away]].copy(deep=True)

    for team in np.unique(df[["Home Team", "Away Team"]]):
        tmp = df.loc[((df["Home Team"] == team) | (df["Away Team"] == team))][cols]
        for season in tmp["Season"].unique():
            # GET DATA
            games = tmp.loc[tmp["Season"] == season]
            values = helper.extract_feature_per_team(games, feature, team, True)

            # RESTRUCTURE GAMES
            games = (
                games.rename_axis(index="Game", columns="Venue")
                .stack()
                .rename("Team")
                .reset_index()
            )

            # AGGREGATE FEATURE
            values[feature] = values[feature].ewm(span=offset).mean().shift(1).round(2).fillna(-1)

            # BUILD RESULT
            result = (
                games.merge(values, on=["Game", "Team"], how="left")
                .set_index(["Game", "Venue"])
                .unstack()
            )

            left = result["Team"].reset_index()
            right = (
                result[feature][["Away Team", "Home Team"]]
                .rename(columns={"Home Team": col_home, "Away Team": col_away})
                .reset_index(drop=True)
            )
            result = pd.concat([left, right], axis=1)

            # UPDATE DF
            new_feat.update(
                result.set_index("Primary Key")
                .reindex(df.set_index("Primary Key").index)
                .reset_index()
            )

    df.update(new_feat)

    if (df[col_home] == ERR_MSG).any() or (df[col_away] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


@report_execution_time
def add_MAX_FEAT_Last_OFFSET_Games_Before_Matchday(df, feature, offset):
    """
    Adds features "Home MAX {feature} Last {offset} Games Before Matchday" and
    "Away MAX {feature} Last {offset} Games Before Matchday" based on "Primary
    Key" , "Home Team", "Away Team", "Home {feature}", "Away {feature}" and
    "Season" for a given dataframe and offset. Values of new features are
    integers. First row with uncalculable value is set to -1.0. Furthermore,
    this function prevents overlaps between saisons.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    feature : string
    offset : integer

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Primary Key", "Home Team", "Away Team", "Home {feature}", "Away
        {feature}" or "Season" are not present
    ValueError:
        when "Home {feature}" or "Away {feature}" is not type float
    """
    cols = [
        "Season",
        "Home Team",
        "Away Team",
        f"Home {feature}",
        f"Away {feature}",
        "Primary Key",
    ]
    if not set(cols).issubset(df.columns):
        raise KeyError

    df[f"Home {feature}"] = df[f"Home {feature}"].astype(float)
    df[f"Away {feature}"] = df[f"Away {feature}"].astype(float)

    col_home = f"Home MAX {feature} Last {offset} Games Before Matchday"
    col_away = f"Away MAX {feature} Last {offset} Games Before Matchday"

    df[col_home] = ERR_MSG
    df[col_away] = ERR_MSG

    df.sort_values(by=["Primary Key"], inplace=True)
    df.reset_index(inplace=True, drop=True)

    new_feat = df[[col_home, col_away]].copy(deep=True)

    for team in np.unique(df[["Home Team", "Away Team"]]):
        tmp = df.loc[((df["Home Team"] == team) | (df["Away Team"] == team))][cols]
        for season in tmp["Season"].unique():
            # GET DATA
            games = tmp.loc[tmp["Season"] == season]
            values = helper.extract_feature_per_team(games, feature, team, False)

            # RESTRUCTURE GAMES
            games = (
                games.rename_axis(index="Game", columns="Venue")
                .stack()
                .rename("Team")
                .reset_index()
            )

            # AGGREGATE FEATURE
            values[feature] = (
                values[feature].rolling(offset, min_periods=1).max().shift(1).round(2).fillna(-1)
            )

            # BUILD RESULT
            result = (
                games.merge(values, on=["Game", "Team"], how="left")
                .set_index(["Game", "Venue"])
                .unstack()
            )

            left = result["Team"].reset_index()
            right = (
                result[feature][["Away Team", "Home Team"]]
                .rename(columns={"Home Team": col_home, "Away Team": col_away})
                .reset_index(drop=True)
            )
            result = pd.concat([left, right], axis=1)

            # UPDATE DF
            new_feat.update(
                result.set_index("Primary Key")
                .reindex(df.set_index("Primary Key").index)
                .reset_index()
            )

    df.update(new_feat)

    if (df[col_home] == ERR_MSG).any() or (df[col_away] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


@report_execution_time
def add_MAX_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, feature, offset):
    """
    Adds features "Home MAX {feature} Against Last {offset} Games Before
    Matchday" and "Away MAX {feature} Against Last {offset} Games Before
    Matchday" based on "Primary Key" , "Home Team", "Away Team", "Home
    {feature}", "Away {feature}" and "Season" for a given dataframe and
    offset. Values of new features are integers. First row with uncalculable
    value is set to -1.0. Furthermore, this function prevents overlaps between
    saisons.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    feature : string
    offset : integer

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Primary Key", "Home Team", "Away Team", "Home {feature}", "Away
        {feature}" or "Season" are not present
    ValueError:
        when "Home {feature}" or "Away {feature}" is not type float
    """
    cols = [
        "Season",
        "Home Team",
        "Away Team",
        f"Home {feature}",
        f"Away {feature}",
        "Primary Key",
    ]
    if not set(cols).issubset(df.columns):
        raise KeyError

    df[f"Home {feature}"] = df[f"Home {feature}"].astype(float)
    df[f"Away {feature}"] = df[f"Away {feature}"].astype(float)

    col_home = f"Home MAX {feature} Against Last {offset} Games Before Matchday"
    col_away = f"Away MAX {feature} Against Last {offset} Games Before Matchday"

    df[col_home] = ERR_MSG
    df[col_away] = ERR_MSG

    df.sort_values(by=["Primary Key"], inplace=True)
    df.reset_index(inplace=True, drop=True)

    new_feat = df[[col_home, col_away]].copy(deep=True)

    for team in np.unique(df[["Home Team", "Away Team"]]):
        tmp = df.loc[((df["Home Team"] == team) | (df["Away Team"] == team))][cols]
        for season in tmp["Season"].unique():
            # GET DATA
            games = tmp.loc[tmp["Season"] == season]
            values = helper.extract_feature_per_team(games, feature, team, True)

            # RESTRUCTURE GAMES
            games = (
                games.rename_axis(index="Game", columns="Venue")
                .stack()
                .rename("Team")
                .reset_index()
            )

            # AGGREGATE FEATURE
            values[feature] = (
                values[feature].rolling(offset, min_periods=1).max().shift(1).round(2).fillna(-1)
            )

            # BUILD RESULT
            result = (
                games.merge(values, on=["Game", "Team"], how="left")
                .set_index(["Game", "Venue"])
                .unstack()
            )

            left = result["Team"].reset_index()
            right = (
                result[feature][["Away Team", "Home Team"]]
                .rename(columns={"Home Team": col_home, "Away Team": col_away})
                .reset_index(drop=True)
            )
            result = pd.concat([left, right], axis=1)

            # UPDATE DF
            new_feat.update(
                result.set_index("Primary Key")
                .reindex(df.set_index("Primary Key").index)
                .reset_index()
            )

    df.update(new_feat)

    if (df[col_home] == ERR_MSG).any() or (df[col_away] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


@report_execution_time
def add_MIN_FEAT_Last_OFFSET_Games_Before_Matchday(df, feature, offset):
    """
    Adds features "Home MIN {feature} Last {offset} Games Before Matchday" and
    "Away MIN {feature} Last {offset} Games Before Matchday" based on "Primary
    Key" , "Home Team", "Away Team", "Home {feature}", "Away {feature}" and
    "Season" for a given dataframe and offset. Values of new features are
    integers. First row with uncalculable value is set to -1.0. Furthermore,
    this function prevents overlaps between saisons.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    feature : string
    offset : integer

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Primary Key", "Home Team", "Away Team", "Home {feature}", "Away
        {feature}" or "Season" are not present
    ValueError:
        when "Home {feature}" or "Away {feature}" is not type float
    """
    cols = [
        "Season",
        "Home Team",
        "Away Team",
        f"Home {feature}",
        f"Away {feature}",
        "Primary Key",
    ]
    if not set(cols).issubset(df.columns):
        raise KeyError

    df[f"Home {feature}"] = df[f"Home {feature}"].astype(float)
    df[f"Away {feature}"] = df[f"Away {feature}"].astype(float)

    col_home = f"Home MIN {feature} Last {offset} Games Before Matchday"
    col_away = f"Away MIN {feature} Last {offset} Games Before Matchday"

    df[col_home] = ERR_MSG
    df[col_away] = ERR_MSG

    df.sort_values(by=["Primary Key"], inplace=True)
    df.reset_index(inplace=True, drop=True)

    new_feat = df[[col_home, col_away]].copy(deep=True)

    for team in np.unique(df[["Home Team", "Away Team"]]):
        tmp = df.loc[((df["Home Team"] == team) | (df["Away Team"] == team))][cols]
        for season in tmp["Season"].unique():
            # GET DATA
            games = tmp.loc[tmp["Season"] == season]
            values = helper.extract_feature_per_team(games, feature, team, False)

            # RESTRUCTURE GAMES
            games = (
                games.rename_axis(index="Game", columns="Venue")
                .stack()
                .rename("Team")
                .reset_index()
            )

            # AGGREGATE FEATURE
            values[feature] = (
                values[feature].rolling(offset, min_periods=1).min().shift(1).round(2).fillna(-1)
            )

            # BUILD RESULT
            result = (
                games.merge(values, on=["Game", "Team"], how="left")
                .set_index(["Game", "Venue"])
                .unstack()
            )

            left = result["Team"].reset_index()
            right = (
                result[feature][["Away Team", "Home Team"]]
                .rename(columns={"Home Team": col_home, "Away Team": col_away})
                .reset_index(drop=True)
            )
            result = pd.concat([left, right], axis=1)

            # UPDATE DF
            new_feat.update(
                result.set_index("Primary Key")
                .reindex(df.set_index("Primary Key").index)
                .reset_index()
            )

    df.update(new_feat)

    if (df[col_home] == ERR_MSG).any() or (df[col_away] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


@report_execution_time
def add_MIN_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, feature, offset):
    """
    Adds features "Home MIN {feature} Against Last {offset} Games Before
    Matchday" and "Away MIN {feature} Against Last {offset} Games Before
    Matchday" based on "Primary Key" , "Home Team", "Away Team", "Home
    {feature}", "Away {feature}" and "Season" for a given dataframe and
    offset. Values of new features are integers. First row with uncalculable
    value is set to -1.0. Furthermore, this function prevents overlaps between
    saisons.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    feature : string
    offset : integer

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Primary Key", "Home Team", "Away Team", "Home {feature}", "Away
        {feature}" or "Season" are not present
    ValueError:
        when "Home {feature}" or "Away {feature}" is not type float
    """
    cols = [
        "Season",
        "Home Team",
        "Away Team",
        f"Home {feature}",
        f"Away {feature}",
        "Primary Key",
    ]
    if not set(cols).issubset(df.columns):
        raise KeyError

    df[f"Home {feature}"] = df[f"Home {feature}"].astype(float)
    df[f"Away {feature}"] = df[f"Away {feature}"].astype(float)

    col_home = f"Home MIN {feature} Against Last {offset} Games Before Matchday"
    col_away = f"Away MIN {feature} Against Last {offset} Games Before Matchday"

    df[col_home] = ERR_MSG
    df[col_away] = ERR_MSG

    df.sort_values(by=["Primary Key"], inplace=True)
    df.reset_index(inplace=True, drop=True)

    new_feat = df[[col_home, col_away]].copy(deep=True)

    for team in np.unique(df[["Home Team", "Away Team"]]):
        tmp = df.loc[((df["Home Team"] == team) | (df["Away Team"] == team))][cols]
        for season in tmp["Season"].unique():
            # GET DATA
            games = tmp.loc[tmp["Season"] == season]
            values = helper.extract_feature_per_team(games, feature, team, True)

            # RESTRUCTURE GAMES
            games = (
                games.rename_axis(index="Game", columns="Venue")
                .stack()
                .rename("Team")
                .reset_index()
            )

            # AGGREGATE FEATURE
            values[feature] = (
                values[feature].rolling(offset, min_periods=1).min().shift(1).round(2).fillna(-1)
            )

            # BUILD RESULT
            result = (
                games.merge(values, on=["Game", "Team"], how="left")
                .set_index(["Game", "Venue"])
                .unstack()
            )

            left = result["Team"].reset_index()
            right = (
                result[feature][["Away Team", "Home Team"]]
                .rename(columns={"Home Team": col_home, "Away Team": col_away})
                .reset_index(drop=True)
            )
            result = pd.concat([left, right], axis=1)

            # UPDATE DF
            new_feat.update(
                result.set_index("Primary Key")
                .reindex(df.set_index("Primary Key").index)
                .reset_index()
            )

    df.update(new_feat)

    if (df[col_home] == ERR_MSG).any() or (df[col_away] == ERR_MSG).any():
        raise BrokenAlgorithmException
    return df


def set_maximum(df, feature, threshold):
    """
    Sets maximum for "Home {feature}" and "Away {feature}}".

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    feature : string
    threshold : integer

    Returns
    -------
    df : pandas.core.frame.DataFrame

    Raises
    ------
    KeyError
        when "Home {feature}" or "Away {feature}" are not present
    ValueError:
        when "Home {feature}" or "Away {feature}" is NaN or not type float
    """
    cols = [
        f"Home {feature}",
        f"Away {feature}",
    ]
    if not set(cols).issubset(df.columns):
        raise KeyError

    # raises ValueError
    df[f"Home {feature}"] = df[f"Home {feature}"].astype(float)
    df[f"Away {feature}"] = df[f"Away {feature}"].astype(float)
    if (df[f"Home {feature}"].isnull()).any() or (df[f"Away {feature}"].isnull()).any():
        raise ValueError

    cols = [f"Home {feature}", f"Away {feature}"]
    df[cols] = df[cols].clip(upper=threshold)

    return df


def prepare_for_model(df, offset):
    """
    This method does two things:
    1) Deletes unusable features, which are unknown at prediction time (e.g.
    xGoals, Points, Possesion...)
    2) Cuts matchweeks by a given offset, which are corrupt due to further
    calculations (e.g. -1 in aggregated features for 1st matchweek)

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    offset : integer

    Returns
    -------
    df : pandas.core.frame.DataFrame
    """
    df = df.drop(columns=feat.unusable_features(), errors="ignore")

    df = df.loc[df["Matchweek"] > offset]

    return df
