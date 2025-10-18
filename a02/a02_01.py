import marimo

__generated_with = "0.10.18"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    mo.md("# Наш первый блокнот `marimo`")
    return (mo,)


@app.cell
def _():
    a=42
    b=24
    _c = 342
    return a, b


@app.cell
def _(a):
    y = a +2
    return (y,)


@app.cell
def _(mo):
    mo.md(r"""# Заголовок""")
    return


@app.cell
def _():
    import pandas as pd

    df = pd.DataFrame({"x":[1,2,3,4], "y":[1,4,9,16]})
    df
    return df, pd


if __name__ == "__main__":
    app.run()
