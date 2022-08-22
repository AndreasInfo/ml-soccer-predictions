import datetime as dt
import re

import bs4
import modules.collector as coll
import modules.helper as helper
import modules.secretary as secr
import modules.translator as trans
import pandas as pd
from selenium import webdriver


class GamesScraper:
    def __init__(self, matchweeks, season, year):
        self.matchweeks = matchweeks
        self.season = season
        self.year = year

    def scrape_games(self, matchweeks, season, year):
        driver = webdriver.Chrome()

        urls = [
            "https://www.soccerbase.com/matches/home.sd?type=1",
            "https://www.soccerbase.com/matches/home.sd?type=2",
        ]

        df = pd.DataFrame()

        for index, url in enumerate(urls):
            driver.get(url)

            soup = bs4.BeautifulSoup(driver.page_source, "html.parser")

            nations = {}
            if index == 0:
                nations = {"": "Premier League"}
            if index == 1:
                nations = {
                    "German ": "Bundesliga",
                    "Spanish ": "La Liga",
                    "French ": "Ligue 1",
                    "Italian ": "Serie A",
                }

            for nation, competition in nations.items():

                entries = soup.find_all("h2", string=f"{nation}{competition}")

                for c in entries:
                    if not c:
                        continue
                    for game in c.find_parent("tbody").find_all(
                        "tr", {"class": "match"}
                    ):
                        if game.find("span", text="postponed"):
                            continue

                        if not re.compile(r"^\d{2}:\d{2}$").search(
                            game.find("span", {"class": "time"}).string
                        ):
                            continue

                        date_gmt = dt.datetime.strptime(
                            game.find("span", {"class": "time"}).string, "%H:%M"
                        )

                        if game.find("a", text="TODAY"):
                            now = dt.datetime.now()
                            date_gmt = date_gmt.replace(day=now.day)
                            date_gmt = date_gmt.replace(month=now.month)
                            date_gmt = date_gmt.replace(year=now.year)
                        else:
                            tmp = (
                                game.find("span", {"class": "date"})
                                .contents[0]
                                .string[-5:]
                            )
                            day = int(tmp[:2])
                            month = tmp[2:]

                            date_gmt = date_gmt.replace(day=day)
                            date_gmt = date_gmt.replace(
                                month=trans.month_eng_str_to_int().get(month)
                            )
                            date_gmt = date_gmt.replace(year=year)

                        def gmt_to_cet(gmt):
                            cet = ""
                            if competition in [
                                "Bundesliga",
                                "La Liga",
                                "Ligue 1",
                                "Serie A",
                            ]:
                                cet = gmt + dt.timedelta(hours=1)
                            elif competition in ["Premier League"]:
                                cet = gmt
                            return cet

                        date_cet = gmt_to_cet(date_gmt)

                        home = game.find("td", {"class": "homeTeam"}).a.string
                        home = helper.invert_dictionary(
                            trans.soccerbase_com_translations()
                        ).get(home)
                        away = game.find("td", {"class": "awayTeam"}).a.string
                        away = helper.invert_dictionary(
                            trans.soccerbase_com_translations()
                        ).get(away)

                        odds_h = -1
                        odds_d = -1
                        odds_a = -1
                        for i, b in enumerate(game.find_all("button")):
                            if i == 0:
                                odds_h = b["data-price-decimal"]
                            elif i == 1:
                                odds_d = b["data-price-decimal"]
                            elif i == 2:
                                odds_a = b["data-price-decimal"]

                        day = trans.day_int_to_ger_str().get(date_cet.weekday())

                        primary_key = f"{date_cet.strftime('%Y-%m-%d')}{home}{away}"

                        df = df.append(
                            {
                                "Home Team": home,
                                "Away Team": away,
                                "Kick Off": date_cet.strftime("%H:%M"),
                                "Home Odds": odds_h,
                                "Deuce Odds": odds_d,
                                "Away Odds": odds_a,
                                "Day": day,
                                "Competition": competition,
                                "Primary Key": primary_key,
                                "Date": date_cet,
                                "Matchweek": matchweeks.get(competition),
                                "Season": season,
                            },
                            ignore_index=True,
                        )

        driver.quit()

        df.reset_index(inplace=True, drop=True)

        return df

    def do(self):
        df = self.scrape_games(self.matchweeks, self.season, self.year)

        df = coll.prepare_Matchweek(df, "Matchweek", "Competition")
        df = coll.prepare_Day(df, "Day")

        secr.save_games(df)
