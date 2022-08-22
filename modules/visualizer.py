import math
import matplotlib.pyplot as plt
import numpy as np

# overview of all features
def info_me(df):
    df.info(verbose=True, show_counts=True)


# describes numerical features
def describe_me(df):
    nr = len(df.describe().columns)
    cols = df.describe().columns
    rows = ["mean", "std", "min", "25%", "50%", "75%", "max"]

    fig, ax = plt.subplots(nrows=math.ceil(nr / 3), ncols=3, figsize=(15, math.ceil(nr / 3) * 5))
    row_counter = 0
    col_counter = 0

    for col in cols:
        Y = []
        for row in rows:
            Y.append(df.describe()[col][row])

        color = "tab:blue"
        ax[row_counter, col_counter].set_ylabel(col, fontsize=14)
        ax[row_counter, col_counter].plot(rows, Y, color=color)
        ax[row_counter, col_counter].tick_params(axis="y", labelsize=14)
        ax[row_counter, col_counter].tick_params(axis="x", rotation=60, labelsize=14)

        col_counter += 1
        if col_counter % 3 == 0:
            col_counter = 0
            row_counter += 1

    fig.tight_layout()


# correlation matrix of numerical features
def corr_me(df):
    size = len(df.corr().columns) * 0.7
    matrix = np.around(df.corr().values, decimals=2)
    labels = df.corr().columns

    fig, ax = plt.subplots(figsize=(size, size))
    im = ax.imshow(matrix)

    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))

    ax.set_xticklabels(labels, fontsize=14)
    ax.set_yticklabels(labels, fontsize=14)

    plt.setp(ax.get_xticklabels(), rotation=60, ha="right", rotation_mode="anchor")

    for i in range(len(labels)):
        for j in range(len(labels)):
            text = ax.text(j, i, matrix[i, j], ha="center", va="center", color="w", fontsize=14)

    fig.tight_layout()


def print_null(df):
    print("- Check null")
    for index, row in df.iterrows():
        if row.isnull().any():
            print(row)
            print()
