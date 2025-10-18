import marimo

__generated_with = "0.11.22"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    mo.md("# Контейнеры гармошка и вкладки")
    return mo, np, plt


@app.cell
def _(mo):
    from time import sleep

    def item(text, dt):
        sleep(dt)
        return mo.md(f"**{text}**")

    mo.accordion(
        items ={
            "Дверь 1": item("Ничевошеньки!", dt=1),
            "Дверь 2": item("Ура! Приз!", dt=3),                           
            "Дверь 3": item("Опять ничего!", dt=1)
        },
        lazy=True,
    )
    return item, sleep


@app.cell
def _(item, mo):
    mo.ui.tabs(
        tabs = {
            "Дверь 1": mo.lazy(item("Ничевошеньки!", dt=1), 
                               show_loading_indicator=True),
            "Дверь 2": mo.lazy(item("Ура! Приз!", dt=5), 
                               show_loading_indicator=True), 
            "Дверь 3": mo.lazy(item("Опять ничего!", dt=1), 
                               show_loading_indicator=True),
        },
        #lazy="*",
        value="Дверь 3",

    )
    return


if __name__ == "__main__":
    app.run()
