import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md("# Кнопки и формы")
    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    ## Кнопка запуска
    """)
    return


@app.cell
def _(mo):
    btn1 = mo.ui.run_button(label="Запустить")
    btn1
    return (btn1,)


@app.cell
def _(btn1, mo):
    import random 

    mo.stop(
        not btn1.value,
        mo.md("Нажмите кнопку **Запустить**, чтобы сгенерировать случайное число"),
    )
    mo.md(f"**{random.randint(0, 100)}**")
    return


@app.cell
def _(mo):
    mo.md("""
    ## Форма с несколькими элементами
    """)
    return


@app.cell
def _(mo):
    form1 = mo.md(
       r"""
       Выберите параметры алгоритма:

       - $\varepsilon$: {epsilon}
       - $\delta$: {delta}
       """
    ).batch(epsilon=mo.ui.slider(0.1, 1, step=0.1), 
            delta=mo.ui.number(1, 10)
           ).form(submit_button_label="Передать")
    form1
    return (form1,)


@app.cell
def _(form1, mo):
    mo.hstack([
            mo.md(r'$\varepsilon$:'),
            form1.value['epsilon'],
            mo.md(r'$\delta$:'),
            form1.value['delta'],    
        ], justify="start") if form1.value else \
            mo.md("Нажмите кнопку **Передать**")
    return


if __name__ == "__main__":
    app.run()
