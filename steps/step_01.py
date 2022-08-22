import datetime as dt
import io
import re
import time

import bs4
import modules.collector as coll
import modules.helper as helper
import modules.secretary as secr
import modules.translator as trans
import pandas as pd
import requests
from selenium import webdriver
from selenium.common.exceptions import (
    MoveTargetOutOfBoundsException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


class DataScraper:
    def __init__(self, teams, no_of_seasons, no_of_recursions):
        self.teams = teams
        self.no_of_seasons = no_of_seasons
        self.no_of_recursions = no_of_recursions

    def scrape_base(self, teams, no_of_seasons, no_of_recursions):
        # add adblock plus
        path_to_extension = "/home/andreas/.config/chromium/Default/Extensions/cfhdojbkjhnklbpkdaibdccddilifddb/3.14_0"
        options = Options()
        options.add_argument("load-extension=" + path_to_extension)
        options.add_argument("--start-maximized")

        # use Chrome driver in usr/bin/ from https://chromedriver.chromium.org/downloads
        driver = webdriver.Chrome(options=options)
        actions = ActionChains(driver)

        # switch tab
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[0])

        SCROLL_INIT = 300
        SCROLL_STEP = 300
        SCROLL_LIMIT = 15
        SLEEPY_TIME = 1

        defective_urls = []

        df = pd.DataFrame()

        for team, link in teams:
            url = f"https://fbref.com/de/mannschaften/{link}"

            driver.get(url)

            # accept cookies
            try:
                xPath = """//span[text()='AGREE']
                        //parent::button"""
                element = driver.find_element(By.XPATH, xPath)
                element.click()
            except NoSuchElementException:
                print(f"- No cookie-dialog found on {driver.current_url} !")
                pass

            for i in range(no_of_seasons):
                scroll_to = SCROLL_INIT
                scroll_counter = 0

                driver.execute_script(f"window.scrollTo(0, {scroll_to})")
                time.sleep(SLEEPY_TIME)

                while True:
                    try:
                        xPath = """//h2[contains(text(),'Ergebnisse & Spiele')]
                                /following-sibling::*[1]
                                /child::*[1]
                                /child::*[1]
                                /child::*[1]"""
                        element = driver.find_element(By.XPATH, xPath)
                        actions.move_to_element(element).perform()

                        xPath = """//h2[contains(text(),'Ergebnisse & Spiele')]
                                /following-sibling::*[1]
                                /child::*[1]
                                /child::*[1]
                                /child::*[1]
                                /following-sibling::*[1]
                                /child::*[1]
                                /child::*[4]"""
                        element = driver.find_element(By.XPATH, xPath)
                        actions.move_to_element(element).click().perform()

                        # scrape data
                        html = driver.page_source
                        soup = bs4.BeautifulSoup(html, "html.parser")
                        csv = soup.find(id="csv_matchlogs_for").contents[2]
                        buffer = io.StringIO(csv)
                        tmp = pd.read_csv(buffer, sep=",")
                        tmp["Mannschaft"] = team
                        season = soup.h1.contents[1].string[-9:]
                        tmp["Saison"] = season
                        df = df.append(tmp)
                        time.sleep(SLEEPY_TIME)

                        print(f"Scraped {driver.current_url} !")
                        break
                    except (
                        MoveTargetOutOfBoundsException,
                        AttributeError,
                        NoSuchElementException,
                    ) as e:
                        scroll_to += SCROLL_STEP
                        driver.execute_script(f"window.scrollTo(0, {scroll_to})")
                        time.sleep(SLEEPY_TIME)
                        scroll_counter += 1

                        # skip page
                        if scroll_counter == SCROLL_LIMIT:
                            defective_urls.append(team)
                            print(
                                f"- Couldn't scrape {driver.current_url} ({type(e).__name__}) . Skip !"
                            )
                            break

                # next page
                driver.execute_script("window.scrollTo(0, 0)")
                time.sleep(SLEEPY_TIME)
                try:
                    xPath = "// div[contains(text(),'Letzte Saison')]/.."
                    element = driver.find_element(By.XPATH, xPath)
                    actions.move_to_element(element).click().perform()
                except (NoSuchElementException, TimeoutException) as e:
                    defective_urls.append(team)
                    print(
                        f'- Could not find button "Letzte Saison" ({type(e).__name__}). Skip {team} !'
                    )
                    break

        if len(defective_urls) == 0:
            print("- No more teams to scrape !")
        elif no_of_recursions <= 0:
            print("- No (more) recursion !")
        else:
            retry = []
            for item in trans.fbref_com_links().items():
                if item[0] in defective_urls:
                    retry.append(item)
            if len(retry) != 0:
                print(
                    f"- Retry {len(retry)} team(s): {retry} . {no_of_recursions - 1} recursions left !"
                )
                df = df.append(self.scrape_base(retry, no_of_seasons, (no_of_recursions - 1)))
            else:
                print("- Error, you should not be here. Call your admin !")

        print(f"- Close driver !")
        driver.quit()

        df.drop_duplicates(inplace=True)

        df.sort_values(by=["Datum"], inplace=True)

        df.reset_index(inplace=True, drop=True)

        return df

    def scrape_additional(self):
        base = "https://www.football-data.co.uk"

        data = [
            ["/germanym.php", "D1"],  # germany
            ["/englandm.php", "E0"],  # england
            ["/spainm.php", "SP1"],  # spain
            ["/italym.php", "I1"],  # italy
            ["/francem.php", "F1"],
        ]  # france

        links = []

        for x in data:
            site = x[0]
            regex = x[1]
            url = base + site
            req = requests.get(url)
            soup = bs4.BeautifulSoup(req.content, "html.parser")

            def relevant_links(href):
                season = "17|18|19|2|3|4|5"  # 2017-2059
                return href and re.compile(f"^mmz4281/({season}).*{regex}.*$").search(href)

            links += soup.find_all(href=relevant_links)

        df = pd.DataFrame()

        for link in links:
            new_url = base + "/" + link["href"]
            req = requests.get(new_url)
            soup = bs4.BeautifulSoup(req.content, "html.parser")

            data = io.StringIO(soup.string)
            tmp = pd.read_csv(data, sep=",")
            df = df.append(tmp)

        return df

    def scrape_coaches(self):
        df = pd.DataFrame(columns={"Team", "Coach", "Started", "Ended"})

        for team, link in trans.weltfussball_de_links().items():
            url = f"https://www.weltfussball.de/teams/{link}/9/"
            req = requests.get(url)
            soup = bs4.BeautifulSoup(req.content, "html.parser")
            tables = soup.findChildren("table")

            rows = tables[0].findChildren(["tr"])

            for row in rows:
                cells = row.findChildren("td")

                date = cells[0].string
                coach = cells[1].string

                if coach == "Trainer":
                    continue

                date_format = (
                    "(0[1-9]|[12]\d|3[01]).(0[1-9]|1[0-2]).(?!0{4})\d{4}"  # 01.01.0001 - 31.12.9999
                )
                if not re.compile(f"{date_format} - {date_format}").search(date):
                    continue

                beginning = dt.datetime.strptime(date[:10], "%d.%m.%Y")
                end = dt.datetime.strptime(date[13:], "%d.%m.%Y")

                df = df.append(
                    {"Team": team, "Coach": coach, "Started": beginning, "Ended": end},
                    ignore_index=True,
                )

        return df

    def do(self):
        print("Scrape base.csv".center(40, "-"))
        print(f"{dt.datetime.now()}")

        df = self.scrape_base(self.teams, self.no_of_seasons, self.no_of_recursions)

        df = coll.prepare_Kick_Off(df)
        df = coll.prepare_Result(df)
        df = coll.prepare_Teams(df)
        df = coll.prepare_Possesions(df)
        df = coll.prepare_xGs(df)
        df = coll.prepare_Goals(df)
        df = coll.prepare_Date(df, "Datum")
        df = coll.prepare_Matchweek(df, "Runde", "Wett")
        df = coll.prepare_Day(df, "Tag")
        df = coll.prepare_Season(df, "Saison")
        df = coll.prepare_Competition(df, "Wett")
        df = coll.prepare_Notes(df, "Hinweise")

        df["Home Team"].replace(
            helper.invert_dictionary(trans.fbref_com_translations()), inplace=True
        )
        df["Away Team"].replace(
            helper.invert_dictionary(trans.fbref_com_translations()), inplace=True
        )
        df = coll.introduce_Primary_Key(df, "Date", "Home Team", "Away Team")

        df.drop_duplicates(subset=["Primary Key"], inplace=True)
        df.sort_values(by=["Date"], inplace=True)
        df.reset_index(inplace=True, drop=True)

        df = df[trans.fbref_com_features().keys()]

        secr.save_base_update(df, True)

        print(f"{dt.datetime.now()}")
        print("Scrape base.csv".center(40, "-"))

        print("Scrape additional.csv".center(40, "-"))
        print(f"{dt.datetime.now()}")

        df = self.scrape_additional()

        df["HomeTeam"].replace(
            helper.invert_dictionary(trans.football_data_co_uk_translations()),
            inplace=True,
        )
        df["AwayTeam"].replace(
            helper.invert_dictionary(trans.football_data_co_uk_translations()),
            inplace=True,
        )

        df.reset_index(inplace=True, drop=True)

        df = coll.prepare_Date(df, "Date")
        df = coll.introduce_Primary_Key(df, "Date", "HomeTeam", "AwayTeam")

        df.sort_values(by=["Date"], inplace=True)
        df.reset_index(inplace=True, drop=True)

        df = df[trans.football_data_co_uk_columns().keys()]
        df.rename(columns=(trans.football_data_co_uk_columns()), inplace=True)

        secr.save_additional(df)

        print(f"{dt.datetime.now()}")
        print("Scrape additional.csv".center(40, "-"))

        print("Scrape coaches.csv".center(40, "-"))
        print(f"{dt.datetime.now()}")

        df = self.scrape_coaches()
        secr.save_coaches(df)

        print(f"{dt.datetime.now()}")
        print("Scrape coaches.csv".center(40, "-"))
