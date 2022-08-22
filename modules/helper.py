import datetime as dt

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def invert_dictionary(dictionary):
    """
    Inverts a dictionary. Keys will be values and vice versa.

    Parameters
    ----------
    dictionary : dict

    Returns
    -------
    result : dict

    Raises
    ------
    ValueError
        when values contain duplicates
    """
    values = list(dictionary.values())
    duplicates = set([x for x in values if values.count(x) > 1])
    if len(duplicates) != 0:
        raise ValueError

    result = {}
    for k, v in dictionary.items():
        result.update({v: k})
    return result


def calculate_brier_multi(targets, probabilities):
    """
    Calculates Brier score. Important: OneHotEncoder transforms targets to a
    sparse matrix and sorts columns alphabetically - this means, probabilities
    should be sorted as well!

    Parameters
    ----------
    targets : numpy.ndarray or pandas.core.series.Series
    probs : numpy.ndarray

    Returns
    -------
    result : float
    """
    ohe_targets = OneHotEncoder().fit_transform(np.array(targets).reshape(-1, 1))
    result = np.mean(np.sum(np.square(probabilities - ohe_targets), axis=1))
    return round(result, 4)


def extract_feature_per_team(df, feature, team, against):
    """
    Extracts feature for per team from columns, that comes in pairs of two
    like:
    >>> data = {
    ...     "Home Team": ["A", "B", "C", "B", "A"],
    ...     "Away Team": ["B", "A", "A", "A", "D"],
    ...     "Home Feat": [1, 2, 0, 10, 7],
    ...     "Away Feat": [2, 3, 0, 5, 1],
    ... }
    >>> index = [1, 2, 5, 9, 29]
    >>> df = pd.DataFrame(index=index, data=data)
    >>> helper.extract_feature_per_team(df, "Feat", "A", False)
        Game Team   Feat
    0     1    A      1
    1     2    A      3
    2     5    A      0
    3     9    A      5
    4    29    A      7
    >>> helper.extract_feature_per_team(df, "Feat", "A", True)
        Game Team   Feat
    0     1    A      2
    1     2    A      2
    2     5    A      0
    3     9    A     10
    4    29    A      1

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    feature : string
    team : string
    against : boolean

    Returns
    -------
    result : pandas.core.frame.DataFrame
    """
    tmp = df[["Home Team", "Away Team", f"Home {feature}", f"Away {feature}"]]
    tmp.columns = tmp.columns.str.split(n=1, expand=True)
    values = []
    if not against:
        values = tmp.stack(0).loc[lambda x: x["Team"] == team, feature].tolist()
    else:
        values = tmp.stack(0).loc[lambda x: x["Team"] != team, feature].tolist()

    result = pd.DataFrame(index=tmp.index, data={"Team": team, feature: values})
    result.index = result.index.set_names("Game")
    result.reset_index(inplace=True)
    return result


def get_periods(start, time_delta, no_of_iterations):
    """
    Gets periods for a given start, time_delta in days and no_of_iterations
    like:

    >>> helper.get_periods(dt.datetime(2021, 1, 1), 7, 4)
    [[datetime.datetime(2021, 1, 1, 0, 0), datetime.datetime(2021, 1, 8, 0, 0)],
     [datetime.datetime(2021, 1, 8, 0, 0), datetime.datetime(2021, 1, 15, 0, 0)],
     [datetime.datetime(2021, 1, 15, 0, 0), datetime.datetime(2021, 1, 22, 0, 0)]]

    Parameters
    ----------
    start : datetime.date
    time_delta : integer
    no_of_iterations : integer

    Returns
    -------
    result : float
    """
    dates = [start + dt.timedelta(days=time_delta) * x for x in range(no_of_iterations)]

    periods = []
    last = ""
    for date in dates:

        if date == dates[0]:
            last = date
            continue

        periods.append([last, date])
        last = date

    return periods
