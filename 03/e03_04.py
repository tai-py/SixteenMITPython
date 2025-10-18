import marimo

__generated_with = "0.16.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import mpmath as mp

    mo.md("# Работаем с библиотекой mpmath")
    mp.dps = 50
    return mp, np, plt


@app.cell
def _(mp):
    def theta(x):
        return (mp.mpf(1) - mp.cos(x))/x**2

    mp.mp.dps  = 100; mp.pretty = True
    theta(1e-9), mp.mp
    return (theta,)


@app.cell
def _(mp, np, theta):
    def failture(dps=7):
        mp.mp.dps = dps
        mantissa = 7, 5, 2, 1
        minexp, maxexp = 1, 100
        for exp in range(minexp, maxexp):
            for m in mantissa: 
                x_str = f"{m}e-{exp}"
                x = mp.mpf( x_str )
                y = theta(x)
                if abs(y - 0.5)>.1:
                    return np.float64(x_str)

    failture(3), failture(7), failture(15), failture(100)
    return (failture,)


@app.cell
def _(failture, plt):
    dpss = 3,5,7, 10, 12, 15, 18, 20, 25, 30, 40, 50, 70, 80, 100
    fail = []
    for dps in dpss:
        f = failture(dps)
        fail.append(f)

    _fig = plt.figure(figsize=(3,3))
    plt.plot(dpss, fail, 'k-', lw=3)
    plt.yscale('log')
    plt.grid()
    plt.xlabel("Значащих цифр")
    plt.ylabel("0.5 превращается в 0.0")
    plt.tight_layout()
    plt.savefig("03_04.png", dpi=300, facecolor='white')
    _fig
    return


if __name__ == "__main__":
    app.run()
