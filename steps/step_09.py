import datetime as dt

import modules.features as feat
import modules.secretary as secr


class PredictionMaker:
    def __init__(self, models):
        self.models = models
        pass

    def do(self):
        print(f"Start: {dt.datetime.now()}")

        df = secr.load_prediction()

        for col in feat.num_features():
            df[col] = df[col].astype(float)

        for col in feat.cat_features():
            df[col] = df[col].astype(object)

        for key, model in self.models.items():
            df[key] = model.predict(df)
            df[
                [f"{key}_proba_a", f"{key}_proba_d", f"{key}_proba_h"]
            ] = model.predict_proba(df)
            df[[f"{key}_proba_a", f"{key}_proba_d", f"{key}_proba_h"]] = df[
                [f"{key}_proba_a", f"{key}_proba_d", f"{key}_proba_h"]
            ].round(6)

        regex = [
            "MA",
            "Days Since Last Game",
            "Coach Substituted Within Last 3 Games",
            "Promoted Last Year",
            "Kick Off Before 17:00",
            "Current Position Before Matchday",
        ]
        for r in regex:
            df.drop(list(df.filter(regex=f"^.*{r}.*$")), axis=1, inplace=True)

        secr.save_bets(df)

        print(f"Stop: {dt.datetime.now()}")
