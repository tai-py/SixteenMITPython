import marimo

__generated_with = "0.11.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.express as px

    mo.md("# SQL-запрос в marimo")
    return mo, pd, px


@app.cell
def _(px):
    # подготавливаем данные
    df = px.data.iris()
    df.columns
    return (df,)


@app.cell
def _(df, mo):
    _df = mo.sql(
        f"""
        SELECT sepal_length, petal_width, species FROM df
        """
    )
    return


if __name__ == "__main__":
    app.run()
