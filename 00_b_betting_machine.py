#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 10:55:08 2022

@author: Hannes
"""
import pandas as pd

pot = 50
safety_factor = 5

print("pot size:", pot)
print("safety factor:", safety_factor)
print()

predictions = pd.read_csv("./sources/archive/20220318-110728_bet.csv", index_col=0)

days = ["SU"]

for day in days:
    for i, row in predictions.iterrows():
        if row["Day"] != day:
            continue
        if row["Home Team"] != "AS Rom":
            continue

        print("%%%%%")

        print(row["Home Team"], " vs ", row["Away Team"])
        home_odds = float(input("Enter Home odds: "))
        deuce_odds = float(input("Enter Deuce odds: "))
        away_odds = float(input("Enter Away odds: "))
        print()

        bet_something = False

        if home_odds - 1 > (1 - row["mlp_proba_h"]) / row["mlp_proba_h"]:
            bet_size = (
                (row["mlp_proba_h"] + (row["mlp_proba_h"] - 1) / (home_odds - 1))
                * pot
                / safety_factor
            )
            pot -= bet_size
            print("bet ", round(bet_size, 2), " on", row["Home Team"])
            print(
                "edge: ",
                round(home_odds - 1 - (1 - row["mlp_proba_h"]) / row["mlp_proba_h"], 2),
            )
            print("probability to win: ", round(row["mlp_proba_h"] * 100, 2), "%")
            print("possible win: ", round(home_odds * bet_size, 2))
            print()
            bet_something = True

        if deuce_odds - 1 > (1 - row["mlp_proba_d"]) / row["mlp_proba_d"]:
            bet_size = (
                (row["mlp_proba_d"] + (row["mlp_proba_d"] - 1) / (deuce_odds - 1))
                * pot
                / safety_factor
            )
            pot -= bet_size
            print("bet ", round(bet_size, 2), " on Deuce")
            print(
                "edge: ",
                round(
                    deuce_odds - 1 - (1 - row["mlp_proba_d"]) / row["mlp_proba_d"], 2
                ),
            )
            print("probability to win: ", round(row["mlp_proba_d"] * 100, 2), "%")
            print("possible win: ", round(deuce_odds * bet_size, 2))
            print()

            bet_something = True

        if away_odds - 1 > (1 - row["mlp_proba_a"]) / row["mlp_proba_a"]:
            bet_size = (
                (row["mlp_proba_a"] + (row["mlp_proba_a"] - 1) / (away_odds - 1))
                * pot
                / safety_factor
            )
            pot -= bet_size
            print("bet ", round(bet_size, 2), " on", row["Away Team"])
            print(
                "edge: ",
                round(away_odds - 1 - (1 - row["mlp_proba_a"]) / row["mlp_proba_a"], 2),
            )
            print("probability to win: ", round(row["mlp_proba_a"] * 100, 2), "%")
            print("possible win: ", round(away_odds * bet_size, 2))
            print()

            bet_something = True

        if not bet_something:
            print("bet nothing")
