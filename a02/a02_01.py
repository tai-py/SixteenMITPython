import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    mo.md("# Наш первый блокнот `marimo`")
    return (mo,)


@app.cell
def _():
    a=42
    print("Значение переменной {a=}")
    a
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Заголовок
    """)
    return


@app.cell
def _():
    import pandas as pd

    df = pd.DataFrame({"x":[1,2,3,4], "y":[1,4,9,16]})
    df
    return


if __name__ == "__main__":
    app.run()
