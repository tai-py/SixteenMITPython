import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    mo.md("""
    # Научная визуализация с помощью matplotlib
    ## Используем объект изображения matplotlib
    """)
    return mo, np, plt


@app.cell
def _(np, plt):
    def sinx_x(a=3, ab=(0, 5), n=1000, figsize=(3,3)):
        t = np.linspace(ab[0], ab[1], n)
        y = np.sinc(a*t)
        fig = plt.figure(figsize=figsize)
        plt.plot(t, y, lw=3)
        plt.grid()
        plt.xlabel('t')
        plt.ylabel('y')
        return fig

    sinx_x()
    return (sinx_x,)


@app.cell
def _(mo, sinx_x):
    mo.md(
        f"""
    ## Интегрируем рисунок matplotlib в Mardown
    {mo.as_html(sinx_x(a=5))}
    """
    )
    return


if __name__ == "__main__":
    app.run()
