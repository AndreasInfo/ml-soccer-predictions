import datetime as dt

import modules.engineer as eng
import modules.secretary as secr
import modules.translator as trans


class ProductionMaker:
    def __init__(self, starting_season):
        self.starting_season = starting_season
        pass

    def do(self):
        print(f"Start: {dt.datetime.now()}")

        base = secr.load_base_update()
        additional = secr.load_additional()
        coaches = secr.load_coaches()
        promotions = secr.load_promotions()
        squads = secr.load_squads()

        df = base.merge(additional, on="Primary Key", how="left")

        seasons = [f"{x}-{x + 1}" for x in range(self.starting_season, 2022)]
        df = df.loc[df["Season"].isin(seasons)]
        df = df.loc[df["Result"] != "UNKNOWN"]

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
            offset = 3
            df = eng.add_MA_FEAT_Last_OFFSET_Games_Before_Matchday(df, feature, offset)
            df = eng.add_MA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, feature, offset)
            df = eng.add_EWMA_FEAT_Last_OFFSET_Games_Before_Matchday(df, feature, offset)
            df = eng.add_EWMA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, feature, offset)
            df = eng.add_MAX_FEAT_Last_OFFSET_Games_Before_Matchday(df, feature, offset)
            df = eng.add_MAX_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, feature, offset)
            df = eng.add_MIN_FEAT_Last_OFFSET_Games_Before_Matchday(df, feature, offset)
            df = eng.add_MIN_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, feature, offset)

            offset = 5
            df = eng.add_MA_FEAT_Last_OFFSET_Games_Before_Matchday(df, feature, offset)
            df = eng.add_MA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, feature, offset)
            df = eng.add_EWMA_FEAT_Last_OFFSET_Games_Before_Matchday(df, feature, offset)
            df = eng.add_EWMA_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, feature, offset)
            df = eng.add_MAX_FEAT_Last_OFFSET_Games_Before_Matchday(df, feature, offset)
            df = eng.add_MAX_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, feature, offset)
            df = eng.add_MIN_FEAT_Last_OFFSET_Games_Before_Matchday(df, feature, offset)
            df = eng.add_MIN_FEAT_Against_Last_OFFSET_Games_Before_Matchday(df, feature, offset)

        df = df.merge(
            squads.add_prefix("Home "),
            left_on=["Home Team", "Season"],
            right_on=["Home club_name", "Home season"],
            how="left",
        )

        df = df.merge(
            squads.add_prefix("Away "),
            left_on=["Away Team", "Season"],
            right_on=["Away club_name", "Away season"],
            how="left",
        )

        secr.save_production_update(df, True)

        print(f"Stop: {dt.datetime.now()}")
