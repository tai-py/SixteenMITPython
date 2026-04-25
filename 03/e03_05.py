import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    from Ivl import Ivl

    mo.md("# Работаем с интервалами для чисел с произвольным числом значащих цифр")
    return Ivl, mo, np


@app.cell
def _(Ivl):
    Ivl.env(dps=15, pretty=False)
    iv0 = Ivl(0, eps=0.1)
    iv0, type(iv0), iv0.data, type(iv0.data)
    return


@app.cell
def _(Ivl):
    Ivl.env(dps=15, pretty=True)
    iv1 = Ivl(0, eps=0.1)
    iv1, type(iv1), iv1.data, type(iv1.data)
    return (iv1,)


@app.cell
def _(Ivl):
    iv02 = Ivl([1,2,3], eps=0.2)
    iv02
    return (iv02,)


@app.cell
def _(iv02):
    iv02[1]
    return


@app.cell
def _(iv02):
    # свойства интервала
    iv02, iv02.a, iv02.b, iv02.mid, iv02.delta
    return


@app.cell
def _(Ivl):
    Ivl.zeros((2,3)), Ivl.ones((3,2))
    return


@app.cell
def _(iv1):
    # вычтем из ноля ноль:
    iv1, iv1 - iv1
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Вычисляем значение интеграла методом прямоугольников для данных с порешностями
    """)
    return


@app.cell
def _(Ivl, np):
    from scipy.integrate import quad

    def integral(f, ab=(0,1), n=10, epsx=0., epsf=0., dps=15):
        x = np.linspace(*ab, n+1) # разбиение ab на n частей
        h = (ab[1] - ab[0])/n
        xc = x + h/2
        xc = xc[:-1]
        Ivl.env(dps=dps)
        xci = Ivl(xc, eps=epsx)
        yi = xci.apply(f, delta=epsf)    
        sum = yi.aggregate(np.sum)*h # суммируем
        # погрешность
        err = np.abs(sum.mid - quad(f, ab[0], ab[1])[0])
        return sum, err, sum.delta

    (integral(lambda x: x**3, n=10, epsx=1e-3, epsf=1e-3),
     integral(lambda x: x**3, n=1000, epsx=1e-3, epsf=1e-3),
    )
    return (integral,)


@app.cell
def _(integral):
    (integral(lambda x: x**3, n=10, epsx=1e-6, epsf=1e-6),
     integral(lambda x: x**3, n=1000, epsx=1e-6, epsf=1e-6),
    )
    return


if __name__ == "__main__":
    app.run()
