import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    mo.md("#Строим гистограммы")
    return mo, np, pd, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Рост и вес студентов
    """)
    return


@app.cell
def _(np):
    data = np.array([
        [189, 177, 179, 183, 180, 185, 178, 186, 176, 185, 184, 180, 180, 188, 183, 195, 194, 188, 182, 195],
        [ 90,  80,  73,  73,  85,  83,  75,  75,  77,  73,  76,  74,   68,  81,  79,  88,  75,  79,  85,  80],
    ])

    height, weight = data[0, :], data[1, :]
    minheight,minweight, maxheight, maxweight = (np.min(height), np.min(weight),
                                                 np.max(height), np.max(weight))
    return height, weight


@app.cell
def _(mo):
    mo.md(r"""
    ##Гистограммы matplotlib для роста студентов
    """)
    return


@app.cell
def _(height, plt):
    _fig, _axs = plt.subplots(nrows=1, ncols=2, figsize=(12,4))
    _axs[0].hist(height, density=True)
    _axs[0].set_xlabel('Рост')
    _axs[0].set_ylabel('Частота')
    _axs[1].hist(height, density=True, cumulative=True)
    _axs[1].set_xlabel('Рост')
    _axs[1].set_ylabel('Частота')
    plt.tight_layout()
    plt.savefig('06_14.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ##Гистограммы matplotlib для веса студентов
    """)
    return


@app.cell
def _(plt, weight):
    _fig, _axs = plt.subplots(nrows=1, ncols=2, figsize=(12,4))
    _axs[0].hist(weight, density=True)
    _axs[0].set_xlabel('Вес')
    _axs[0].set_ylabel('Частота')
    _axs[1].hist(weight, density=True, cumulative=True)
    _axs[1].set_xlabel('Вес')
    _axs[1].set_ylabel('Частота')
    plt.tight_layout()
    plt.savefig('06_15.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ##Гистограммы seaborn для роста и веса студентов
    """)
    return


@app.cell
def _(height, plt, sns, weight):
    _fig, _axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

    sns.histplot(height, kde=True, stat="density", ax=_axs[0, 0])
    _axs[0, 0].set_xlabel("Рост")
    _axs[0, 0].set_ylabel("Частота")

    sns.histplot(height, cumulative=True, kde=True, stat="density", ax=_axs[0, 1])
    _axs[0, 1].set_xlabel("Рост")
    _axs[0, 1].set_ylabel("Частота")

    sns.histplot(weight, kde=True, stat="density", ax=_axs[1, 0])
    _axs[1, 0].set_xlabel("Вес")
    _axs[1, 0].set_ylabel("Частота")

    sns.histplot(height, cumulative=True, kde=True, stat="density", ax=_axs[1, 1])
    _axs[1, 1].set_xlabel("Вес")
    _axs[1, 1].set_ylabel("Частота")    

    plt.tight_layout()
    plt.savefig('06_16.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Двумерная гистограмма
    """)
    return


@app.cell
def _(height, pd, plt, sns, weight):
    height_weight = pd.DataFrame({'рост':height, 'вес':weight})
    _fig, _ax = plt.subplots(nrows=1, ncols=1, figsize=(7, 6))
    sns.histplot(data=height_weight, x='рост', y='вес', 
                 cmap='viridis',cbar=True, stat="density", ax=_ax)
    plt.savefig('06_17.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Трехмерная гистограмма
    [3D гистограмма в Matplotlib](https://labex.io/ru/tutorials/python-matplotlib-3d-histogram-48768)

    [Гистограммы и графики распределения в Python](https://habr.com/ru/companies/skillfactory/articles/683738/)
    """)
    return


@app.cell
def _(height, np, plt, weight):

    _fig = plt.figure(figsize=(11, 6))
    _ax = _fig.add_subplot(111, projection='3d')
    hist, xedges, yedges = np.histogram2d(height, weight, density=True)

    ## Construct arrays for the anchor positions 
    xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = 0

    ## Construct arrays with the dimensions for the 16 bars.
    dx = dy = 0.5 * np.ones_like(zpos)
    dz = hist.ravel()

    _ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')
    _ax.set_xlabel('Рост')
    _ax.set_ylabel('Вес')
    _ax.set_zlabel('Частота')
    plt.tight_layout()
    plt.savefig('06_18.png', dpi=300, facecolor='white')
    _fig
    return


if __name__ == "__main__":
    app.run()
