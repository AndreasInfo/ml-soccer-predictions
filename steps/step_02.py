import pandas as pd
import datetime as dt
import random

import modules.secretary as secr
import modules.translator as trans
import modules.visualizer as vis


class DataMonitor:
    def __init__(self):
        pass

    def do(self):
        base = secr.load_base_update()
        additional = secr.load_additional()
        coaches = secr.load_coaches()
        promotions = secr.load_promotions()

        print("Check additional.csv".center(40, "-"))

        # repair known errors in additional
        known_errors = {
            "2020-09-13Paris Saint-GermainOlympique Marseille": [1.5, 5, 5.5],
            "2020-10-18AS MonacoHSC Montpellier": [1.48, 4.75, 6],
            "2020-10-18Udinese CalcioParma Calcio": [1.8, 3.6, 4.6],
            "2020-10-19Hellas VeronaCFC Genua": [2.05, 3.4, 3.75],
            "2022-01-10FC TurinAC Florenz": [3, 3.3, 2.4],
        }

        for key, value in known_errors.items():
            game = additional.loc[additional["Primary Key"] == key]
            additional.loc[game.index, "Home Odds"] = value[0]
            additional.loc[game.index, "Deuce Odds"] = value[1]
            additional.loc[game.index, "Away Odds"] = value[2]

        wrong = "2022-04-02AS Saint-ÉtienneOlympique Marseille"
        right = "2022-04-03AS Saint-ÉtienneOlympique Marseille"
        game = additional.loc[additional["Primary Key"] == wrong]
        additional.loc[game.index, "Primary Key"] = right

        additional.reset_index(inplace=True, drop=True)

        secr.save_additional(additional)

        vis.print_null(additional)

        print("Check base.csv".center(40, "-"))

        vis.print_null(base)

        print('\nRemove known games with result = "UNKNOWN"')
        cols = [
            "Competition",
            "Date",
            "Primary Key",
            "Result",
            "Matchweek",
            "Season",
            "Notes",
        ]

        ignore = pd.DataFrame()

        # ignore canceled games (e. g. Ligue 1 season 2019-2020 aborted after matchweek 27)
        canceled_games = base.loc[base["Notes"].str.contains("^.*Spiel abgesagt.*$")][
            cols
        ]
        print(f"No. canceled games: {len(canceled_games)}")
        ignore = ignore.append(canceled_games)

        # ignore postponed games
        postponed_games = base.loc[base["Notes"] == "Spiel verschoben"][cols]
        print(f"No. postponed games: {len(postponed_games)}")
        ignore = ignore.append(postponed_games)

        # ignore future games
        upcomming_games = base.loc[
            base["Date"]
            >= dt.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        ]
        print(f"No. upcoming games: {len(upcomming_games)}")
        ignore = ignore.append(upcomming_games)

        # ignore aborted games
        aborted_games = base.loc[base["Notes"] == "Spiel abgebrochen"][cols]
        print(f"No. aborted games: {len(aborted_games)}")
        ignore = ignore.append(aborted_games)

        # ignore games decided at the green table
        green_table = base.loc[base["Notes"].str.contains("zum Sieger erklärt")][cols]
        print(f"No. green table: {len(green_table)}")
        ignore = ignore.append(green_table)

        base.drop(ignore.index, inplace=True)
        base.reset_index(inplace=True, drop=True)
        secr.save_base_update(base, False)

        print('\n- Check unknown games with result = "UNKNOWN"')
        tmp = base.loc[base["Result"] == "UNKNOWN"]
        tmp = tmp.loc[~tmp.index.isin(ignore.index)]

        print(tmp[["Primary Key", "Result", "Competition"]])

        print("\n- Check Primary Keys for duplicates\n")
        duplicates = base.duplicated(subset=["Primary Key"], keep=False)

        assert ~base.duplicated(subset=["Primary Key"], keep=False).any()

        print("- Check random matchweeks for games played")

        result = {
            "Premier League": 10,
            "Bundesliga": 9,
            "La Liga": 10,
            "Serie A": 10,
            "Ligue 1": 10,
        }

        for competition, games in result.items():
            year = random.randrange(2017, 2021)
            season = f"{year}-{year + 1}"

            matchweek = -1
            if competition == "Bundesliga":
                matchweek = random.randrange(1, 35)
            elif competition == "Ligue 1" and year == 2019:
                matchweek = random.randrange(1, 29)
            elif competition == "Serie A" and year == 2020:
                matchweek = random.randrange(2, 39)
            else:
                matchweek = random.randrange(1, 39)

            tmp = base.loc[
                (base["Competition"] == competition)
                & (base["Season"] == season)
                & (base["Matchweek"] == matchweek)
            ]

            print(
                f"{competition} {season} Matchweek {matchweek} TARGET:{len(tmp)} ACTUAL:{games}"
            )
            assert len(tmp) == games

        tmp = base.loc[
            (base["Competition"].isin(trans.competitions()))
            & (base["Season"] == "2020-2021")
        ]

        print("\n- Check games played in 2020-2021\n")

        # bundesliga + 4 * (each Premier League, La Liga, Serie A, Ligue 1) - invalid game
        assert len(tmp) == (306 + 4 * 380 - 1)

        tmp = base.loc[
            (base["Competition"].isin(trans.competitions()))
            & (base["Date"] > dt.datetime(2017, 7, 1))
        ]
        tmp = tmp.loc[~tmp.index.isin(ignore.index)]

        print("- Check invalid values")

        for feature, unknown_value in trans.fbref_com_features().items():
            print_me = tmp.loc[tmp[feature] == unknown_value]

            if len(print_me) > 0:
                print(f"{feature:} contains {unknown_value} : {len(print_me)}")
