import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import datetime

    mo.md("# Анимация даты и времени")
    return datetime, mo


@app.cell
def _(mo):
    refresh = mo.ui.refresh(default_interval="1s")
    refresh
    return (refresh,)


@app.cell
def _(datetime, mo, refresh):
    dt = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    refresh
    mo.md(f'**{dt}**')
    return


@app.cell
def _(mo):
    mo.md(
        """
    >Обязательно должно быть установлено автоматическое, а не ленивое выполнение ячеек.
    > Для этого в правом верхнем углу блокнота необходимо  нажать кнопку **Settings**, затем ссылку **User settings** внизу появившегося диалога, выбрать **Runtime** из меню, далее установить **on cell change autorun **. Альтернативой **autorun** является **lazy**.
    """
    )
    return


@app.cell
def _(mo):
    import numpy as np
    import matplotlib.pyplot  as plt

    amin, amax, astep = 0.2, 3.0, 0.2
    xmin, xmax = 0., 3. 
    n = 300
    x = np.linspace(xmin, xmax, n)
    a_get, a_set = mo.state(amin) # состояние a

    def plot_sinc(figsize=(3,3)):
        a = a_get()    
        y = np.sinc(a*x)

        # рисуем
        fig = plt.figure(figsize=figsize)
        plt.plot(x, y, 'k-', lw=3)
        plt.grid()
        plt.title(f'y = sinc({a:4.1f}*x)')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.ylim(-.3, 1.1)

        # рассчитываем и сохраняем новое значение a
        a += astep
        a = amin if a>amax+astep else a
        a_set(a)

        return fig

    refresh2 = mo.ui.refresh(default_interval=.1,  options=[0.1, 0.2, 1, 2, 5],)
    refresh2
    return plot_sinc, refresh2


@app.cell
def _(plot_sinc, refresh2):
    refresh2
    plot_sinc()
    return


if __name__ == "__main__":
    app.run()
