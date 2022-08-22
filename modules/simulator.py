import matplotlib.pyplot as plt

VALID_CLASSIFIER = ["lrc", "rfc", "mlp", "knc", "svc", "abc", "qda", "gnb"]


def addictive(df, model, bet, combined):
    """
    Bet on each game with outcome calculated by model. Use a constant bet. It
    can package games to bundles with size combined.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    model : string
    bet : integer
    combine : integer

    Raises
    ------
    ValueError
        when model is not in VALID_CLASSIFIER
    """
    if model not in VALID_CLASSIFIER:
        raise ValueError

    correct = 0
    counter = 0
    balance = 0
    balances = []
    odds = 1
    hits = 0

    for index, row in df.iterrows():
        result = row["Result"]
        prediction = row[model]

        counter += 1

        if result == prediction:
            correct += 1

        if prediction == "H":
            odds *= row["Home Odds"]
        elif prediction == "A":
            odds *= row["Away Odds"]
        elif prediction == "D":
            odds *= row["Deuce Odds"]
        odds = round(odds, 2)

        if (index + 1) % combined == 0:
            if correct == counter:
                balance += odds * bet - bet
                hits += 1
            else:
                balance -= bet

            balance = round(balance, 2)
            balances.append(balance)
            counter = 0
            correct = 0
            odds = 1

    print(f"Hits: {hits}/{len(balances)} ({round(hits / len(balances) * 100, 2)} %)")
    print(f"Min: {min(balances)}")
    print(f"Max: {max(balances)}")
    print(f"Investment: {len(balances) * bet}")
    print(f"Balance: {round(balances[-1], 2)}")
    print(f"Return: {round(balances[-1] / (len(balances) * bet) * 100, 2)} %")

    plt.plot(list(range(len(balances))), balances)


def bookie(df, bet, combined):
    """
    Bet on each game with outcome calculated by bookie. Use a constant bet. It
    can package games to bundles with size combine.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    model : string
    bet : integer
    combine : integer
    """

    correct = 0
    counter = 0
    balance = 0
    balances = []
    odds = 1
    hits = 0

    for index, row in df.iterrows():
        result = row["Result"]
        prediction = ""

        favorite = min(row["Home Odds"], row["Deuce Odds"], row["Away Odds"])
        if row["Home Odds"] == favorite:
            prediction = "H"
        if row["Away Odds"] == favorite:
            prediction = "A"
        if row["Deuce Odds"] == favorite:
            prediction = "D"

        counter += 1

        if result == prediction:
            correct += 1

        if prediction == "H":
            odds *= row["Home Odds"]
        elif prediction == "A":
            odds *= row["Away Odds"]
        elif prediction == "D":
            odds *= row["Deuce Odds"]
        odds = round(odds, 2)

        if (index + 1) % combined == 0:
            if correct == counter:
                balance += odds * bet - bet
                hits += 1
            else:
                balance -= bet

            balance = round(balance, 2)
            balances.append(balance)

            counter = 0
            correct = 0
            odds = 1

    print(f"Hits: {hits}/{len(balances)} ({round(hits / len(balances) * 100, 2)} %)")
    print(f"Min: {min(balances)}")
    print(f"Max: {max(balances)}")
    print(f"Investment: {len(balances) * bet}")
    print(f"Balance: {round(balances[-1], 2)}")
    print(f"Return: {round(balances[-1] / (len(balances) * bet) * 100, 2)} %")

    plt.plot(list(range(len(balances))), balances)


def millionaire(df, model, bet, alpha):
    """
    Bet on games with favored odds calculated by model. Odds are favored, when
    calculated probabilities are bigger than bookie's probabilities + alhpa
    for the same outcome [H, D, A]. alpha is theoretical between 0-1 but
    practical between 0.01-0.2. It uses a constant bet.


    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    model : string
    bet : integer
    alpha : float


    Raises
    ------
    ValueError
        when model is not in VALID_CLASSIFIER
    """
    if model not in VALID_CLASSIFIER:
        raise ValueError

    balance = 0
    balances = []

    for index, row in df.iterrows():
        home = 1 / row["Home Odds"] + alpha < row[f"{model}_proba_h"]
        deuce = 1 / row["Deuce Odds"] + alpha < row[f"{model}_proba_d"]
        away = 1 / row["Away Odds"] + alpha < row[f"{model}_proba_a"]

        if home:
            balance -= bet
            if row["Result"] == "H":
                balance += row["Home Odds"] * bet
            balances.append(balance)

        if deuce:
            balance -= bet
            if row["Result"] == "D":
                balance += row["Deuce Odds"] * bet
            balances.append(balance)

        if away:
            balance -= bet
            if row["Result"] == "A":
                balance += row["Away Odds"] * bet
            balances.append(balance)

    plt.plot(list(range(len(balances))), balances)
    print(f"Min: {round(min(balances), 2)}")
    print(f"Max: {round(max(balances), 2)}")
    print(f"Investment: {len(balances) * bet}")
    print(f"Balance: {round(balances[-1], 2)}")
    print(f"Return: {round(balances[-1] / (len(balances) * bet) * 100, 2)} %")


def billionaire(df, model, budget, security, alpha):
    """
    Bet on games with favored odds calculated by model. Odds are favored, when
    calculated probabilities are bigger than bookie's probabilities + alhpa
    for the same outcome [H, D, A]. alpha is theoretical between 0-1 but
    practical between 0.01-0.2. It uses a percentaged bet of overall budget
    (Kelly-Criterion). The bet is divided by a security factor.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
    model : string
    budget : integer
    security : integer
    alpha : float

    Raises
    ------
    ValueError
        when model is not in VALID_CLASSIFIER
    """
    if model not in VALID_CLASSIFIER:
        raise ValueError

    bet = 0
    balance = budget
    balances = []
    bets = []

    for index, row in df.iterrows():
        home = 1 / row["Home Odds"] + alpha < row[f"{model}_proba_h"]
        deuce = 1 / row["Deuce Odds"] + alpha < row[f"{model}_proba_d"]
        away = 1 / row["Away Odds"] + alpha < row[f"{model}_proba_a"]

        if home:
            bet = (
                (
                    row[f"{model}_proba_h"]
                    + (row[f"{model}_proba_h"] - 1) / row["Home Odds"]
                )
                * balance
                / security
            )
            bets.append(bet)
            balance -= bet
            if row["Result"] == "H":
                balance += row["Home Odds"] * bet
            balances.append(balance)

        if deuce:
            bet = (
                (
                    row[f"{model}_proba_d"]
                    + (row[f"{model}_proba_d"] - 1) / row["Deuce Odds"]
                )
                * balance
                / security
            )
            bets.append(bet)
            balance -= bet
            if row["Result"] == "D":
                balance += row["Deuce Odds"] * bet
            balances.append(balance)

        if away:
            bet = (
                (
                    row[f"{model}_proba_a"]
                    + (row[f"{model}_proba_a"] - 1) / row["Away Odds"]
                )
                * balance
                / security
            )
            bets.append(bet)
            balance -= bet
            if row["Result"] == "A":
                balance += row["Away Odds"] * bet
            balances.append(balance)

    print(f"Min: {round(min(balances), 2)}")
    print(f"Max: {round(max(balances), 2)}")
    print(f"Investment: {round(sum(bets))}")
    print(f"Balance: {round(balances[-1], 2)}")
    print(f"Return: {round((balances[-1] - budget) / sum(bets) * 100, 2)} %")

    plt.plot(list(range(len(balances))), balances)
    plt.plot(list(range(len(bets))), bets)
