import pandas as pd
import datetime as dt
from pandas.errors import EmptyDataError

DIRECTORY = "./sources/data"

PRODUCTION = f"{DIRECTORY}/production.csv"
PRODUCTION_UPDATE = f"{DIRECTORY}/production_update.csv"
BASE = f"{DIRECTORY}/base.csv"
BASE_UPDATE = f"{DIRECTORY}/base_update.csv"
ADDITIONAL = f"{DIRECTORY}/additional.csv"
COACHES = f"{DIRECTORY}/coaches.csv"
PROMOTIONS = f"{DIRECTORY}/promotions.csv"
MODEL = f"{DIRECTORY}/model.csv"
GAMES = f"{DIRECTORY}/games.csv"
PREDICTION = f"{DIRECTORY}/prediction.csv"
SQUADS = f"{DIRECTORY}/squads.csv"


def save_base_update(df, update):
    if update:
        df_old = pd.DataFrame()
        try:
            df_old = pd.read_csv(BASE, index_col=0, parse_dates=["Date"])
        except (EmptyDataError, FileNotFoundError):
            pass

        df_new = df_old.append(df)
        df_new.drop_duplicates(subset=["Primary Key"], keep="last", inplace=True)
        df_new.sort_values(by=["Primary Key"], inplace=True)
        df_new.reset_index(inplace=True, drop=True)

        df_new.to_csv(path_or_buf=BASE_UPDATE)
    else:
        df.to_csv(path_or_buf=BASE_UPDATE)


def load_base_update():
    return pd.read_csv(BASE_UPDATE, index_col=0, parse_dates=["Date"])


def save_additional(df):
    df.to_csv(path_or_buf=ADDITIONAL)


def load_additional():
    return pd.read_csv(ADDITIONAL, index_col=0)


def save_coaches(df):
    df.to_csv(path_or_buf=COACHES)


def load_coaches():
    return pd.read_csv(
        f"./sources/data/coaches.csv",
        index_col=0,
        parse_dates=["Started", "Ended"],
        date_parser=lambda x: dt.datetime.strptime(x, "%Y-%m-%d"),
    )


def load_promotions():
    return pd.read_csv(PROMOTIONS, index_col=0)


def load_production_update():
    return pd.read_csv(PRODUCTION_UPDATE, index_col=0, parse_dates=["Date"])


def save_production_update(df, update):
    if update:
        df_old = pd.DataFrame()
        try:
            df_old = pd.read_csv(PRODUCTION, index_col=0, parse_dates=["Date"])
        except (EmptyDataError, FileNotFoundError):
            pass
        df_new = df_old.append(df)
        df_new.drop_duplicates(subset=["Primary Key"], keep="last", inplace=True)
        df_new.sort_values(by=["Primary Key"], inplace=True)
        df_new.reset_index(inplace=True, drop=True)

        df_new.to_csv(path_or_buf=PRODUCTION_UPDATE)
    else:
        df.to_csv(path_or_buf=PRODUCTION_UPDATE)


def load_model():
    return pd.read_csv(MODEL, index_col=0)


def save_model(df):
    df.to_csv(path_or_buf=MODEL)


def load_games():
    return pd.read_csv(GAMES, index_col=0, parse_dates=["Date"])


def save_games(df):
    df.to_csv(path_or_buf=GAMES)


def save_bets(df):
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    df.to_csv(path_or_buf=f"./sources/archive/{stamp}_bet.csv")


def save_prediction(df):
    df.to_csv(path_or_buf=PREDICTION)


def load_prediction():
    return pd.read_csv(PREDICTION, index_col=0)


def save_squads(df):
    df.to_csv(path_or_buf=SQUADS)


def load_squads():
    return pd.read_csv(SQUADS, index_col=0)
