import pytest

import modules.translator as trans


def test_fbref_com_translations():
    data = trans.fbref_com_translations()
    values = list(data.values())
    duplicates = set([x for x in values if values.count(x) > 1])
    assert len(duplicates) == 0


def test_fbref_com_links():
    data = trans.fbref_com_links()
    values = list(data.values())
    duplicates = set([x for x in values if values.count(x) > 1])
    assert len(duplicates) == 0


def test_football_data_co_uk_translations():
    data = trans.football_data_co_uk_translations()
    values = list(data.values())
    duplicates = set([x for x in values if values.count(x) > 1])
    assert len(duplicates) == 0


def test_weltfussball_de_links():
    data = trans.weltfussball_de_links()
    values = list(data.values())
    duplicates = set([x for x in values if values.count(x) > 1])
    assert len(duplicates) == 0


def test_get_following_season():
    season = "16-17"
    result = "17/18"
    assert trans.get_following_season(season) == result

    season = "98-99"
    result = "99/00"
    assert trans.get_following_season(season) == result

    season = "99-00"
    result = "00/01"
    assert trans.get_following_season(season) == result

    season = "00-01"
    result = "01/02"
    assert trans.get_following_season(season) == result

    season = "08-09"
    result = "09/10"
    assert trans.get_following_season(season) == result

    season = "09-10"
    result = "10/11"
    assert trans.get_following_season(season) == result

    with pytest.raises(ValueError):
        season = "98-00"
        trans.get_following_season(season)

    with pytest.raises(ValueError):
        season = "99-01"
        trans.get_following_season(season)

    with pytest.raises(ValueError):
        season = "16-ab"
        trans.get_following_season(season)

    with pytest.raises(ValueError):
        season = "16-16"
        trans.get_following_season(season)


def test_soccerbase_com_translations():
    data = trans.soccerbase_com_translations()
    values = list(data.values())
    duplicates = set([x for x in values if values.count(x) > 1])
    assert len(duplicates) == 0


def test_competitions():
    assert trans.competitions() == [
        "Bundesliga",
        "Premier League",
        "La Liga",
        "Serie A",
        "Ligue 1",
    ]


def test_month_eng_str_to_int():
    assert trans.month_eng_str_to_int().get("Jan") == 1
    assert trans.month_eng_str_to_int().get("Feb") == 2
    assert trans.month_eng_str_to_int().get("Mar") == 3
    assert trans.month_eng_str_to_int().get("Apr") == 4
    assert trans.month_eng_str_to_int().get("May") == 5
    assert trans.month_eng_str_to_int().get("Jun") == 6
    assert trans.month_eng_str_to_int().get("Jul") == 7
    assert trans.month_eng_str_to_int().get("Aug") == 8
    assert trans.month_eng_str_to_int().get("Sep") == 9
    assert trans.month_eng_str_to_int().get("Oct") == 10
    assert trans.month_eng_str_to_int().get("Nov") == 11
    assert trans.month_eng_str_to_int().get("Dec") == 12


def test_day_int_to_ger_str():
    assert trans.day_int_to_ger_str().get(0) == "Mo."
    assert trans.day_int_to_ger_str().get(1) == "Di."
    assert trans.day_int_to_ger_str().get(2) == "Mi."
    assert trans.day_int_to_ger_str().get(3) == "Do."
    assert trans.day_int_to_ger_str().get(4) == "Fr."
    assert trans.day_int_to_ger_str().get(5) == "Sa."
    assert trans.day_int_to_ger_str().get(6) == "So."


def day_ger_str_to_eng_str():
    assert trans.day_ger_str_to_eng_str().get("Mo.") == "MO"
    assert trans.day_ger_str_to_eng_str().get("Di.") == "TU"
    assert trans.day_ger_str_to_eng_str().get("Mi.") == "WE"
    assert trans.day_ger_str_to_eng_str().get("Do.") == "TH"
    assert trans.day_ger_str_to_eng_str().get("Fr.") == "FR"
    assert trans.day_ger_str_to_eng_str().get("Sa.") == "SA"
    assert trans.day_ger_str_to_eng_str().get("So.") == "SU"
