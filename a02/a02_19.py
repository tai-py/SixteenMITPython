import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import random

    mo.md("# Массивы и словари для динамического создания виджетов")
    return mo, random


@app.cell
def _(mo, random):
    array = mo.ui.array([mo.ui.text(placeholder="Введите данные") \
                        for i in range(random.randint(2, 5))])
    dictionary = mo.ui.dictionary({str(i): mo.ui.text(placeholder='Введите данные') \
              for i in range(random.randint(1, 5))})
    mo.hstack([array, dictionary], justify="start")
    return array, dictionary


@app.cell
def _(array, dictionary, mo):
    mo.hstack([array.value, dictionary.value], justify="start")
    return


@app.cell
def _(array):
    len(array.value), array.value[1]
    return


if __name__ == "__main__":
    app.run()
