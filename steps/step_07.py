import datetime as dt

import modules.engineer as eng
import modules.secretary as secr
import modules.translator as trans


class PredictionMaker:
    def __init__(self, current_season):
        self.current_season = current_season

    def do(self):
        print(f"Start: {dt.datetime.now()}")

        production = secr.load_production_update()
        games = secr.load_games()
        coaches = secr.load_coaches()
        promotions = secr.load_promotions()

        df = production.append(games)
        df.reset_index(inplace=True, drop=True)

        df = df.loc[df["Season"] == self.current_season]

        df.sort_values(by=["Primary Key"], inplace=True)
        df.reset_index(inplace=True, drop=True)

        df = eng.add_Days_Since_Last_Game(df)
        df = eng.set_maximum(df, "Days Since Last Game", 21)
        df = df.loc[df["Competition"].isin(trans.competitions())]
        df.reset_index(inplace=True, drop=True)
        df = eng.add_Coach(df, coaches)
        df = eng.add_Coach_Substituted_Within_Last_OFFSET_Games(df, 3)
        df = eng.add_Points(df)
        df = eng.add_Promoted_Last_Year(df, promotions)
        df = eng.add_Kick_Off_Before_17_00(df)
        df = eng.add_Current_Position_Before_Matchday(df, 3)
        features = [
            "xG",
            "Possesion",
            "Goals",
            "Shots",
            "Shots on Target",
            "Fouls Committed",
            "Corners",
            "Yellow Cards",
            "Red Cards",
            "Points",
        ]
        for feature in features:
            df = eng.add_MA_FEAT_Last_OFFSET_Games_Before_Matchday(df, feature, 3)
            df = eng.add_MA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(
                df, feature, 3
            )
            df = eng.add_EWMA_FEAT_Last_OFFSET_Games_Before_Matchday(df, feature, 3)
            df = eng.add_EWMA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(
                df, feature, 3
            )

        df = df.loc[df["Result"].isnull()]
        df = eng.prepare_for_model(df)
        df.reset_index(inplace=True, drop=True)
        df.drop(columns=["Result"], inplace=True, errors="ignore")

        secr.save_prediction(df)

        print(f"Stop: {dt.datetime.now()}")
