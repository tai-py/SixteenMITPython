import marimo

__generated_with = "0.12.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    mo.md("# Отображаем массив NumPy 'от руки'")
    return (mo,)


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt

    x = np.linspace(-5, 5, 1000) 
    y = np.sinc(x) 

    fig = plt.figure(figsize=(4,3))
    with plt.xkcd():
        plt.plot(x, y,'k-', lw=3)
        plt.xlabel('x', fontsize=16)
        plt.ylabel(r'y', fontsize=16)
    
    fig               

    return fig, np, plt, x, y


if __name__ == "__main__":
    app.run()
