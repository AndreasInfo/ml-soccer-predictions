import datetime as dt

import modules.secretary as secr


class PredictionMonitor:
    def __init__(self):
        pass

    def do(self):
        print(f"Stop: {dt.datetime.now()}")

        df = secr.load_prediction()

        drop = df[df.isnull().any(axis=1)]
        print(f"Dropped team which appear multiple times:")
        if drop.empty:
            print(None)
        else:
            print(drop)

        df.drop(drop.index, inplace=True)
        df.reset_index(inplace=True, drop=True)

        secr.save_prediction(df)

        print(f"Stop: {dt.datetime.now()}")
