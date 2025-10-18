import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    # ячейка 0
    import marimo as mo

    mo.md("# Реактивные переменные в marimo")
    return (mo,)


@app.cell
def _(a):
    # ячейка 1
    a
    return


@app.cell
def _():
    # ячейка 2
    a = 42
    return (a,)


@app.cell
def _():
    # ячейка 3
    #a = 43
    return


@app.cell
def _(mo):
    # ячейка 4
    import numpy as np
    import matplotlib.pyplot as plt

    def sinx_x(b, n=300, ab=(0, 3), figsize=(3,3)):
        x = np.linspace(ab[0], ab[1], n)
        y = np.sinc(b*x)
        fig = plt.figure(figsize=figsize)
        plt.plot(x, y, lw=3)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid()
        return fig

    b_slider = mo.ui.slider(start=1., stop=5., step=0.1, 
                           debounce=False)
    return b_slider, sinx_x


@app.cell
def _(b_slider, mo, sinx_x):
    # ячейка 5
    mo.md(f'''
    ## Связываем график с реактивной переменной b
    {b_slider } b = {b_slider.value:4.1f}

    {mo.as_html(sinx_x(b_slider.value))}
    ''')
    return


@app.cell
def _(mo):
    # ячейка 6
    # функции для получения и задания состояния
    get_state, set_state = mo.state(1.)
    return get_state, set_state


@app.cell
def _(get_state, mo, set_state):
    # ячейка 7
    # первый слайдер
    s1 = mo.ui.slider(1., 10., 0.1, value=get_state(), on_change=set_state)
    return (s1,)


@app.cell
def _(get_state, mo, set_state):
    # ячейка 8
    # второй слайдер
    s2 = mo.ui.slider(1., 10., 0.1, value=get_state(), on_change=set_state)
    return (s2,)


@app.cell
def _(mo, s1, s2):
    # ячейка 9
    # пользовательский интерфейс
    mo.md(f'''
    ## Синхронизация состояния двух слайдеров
    s1 {s1} {s1.value:5.1f} s2 {s2} {s2.value:5.1f}
    ''')
    return


if __name__ == "__main__":
    app.run()
