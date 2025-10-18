import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    # ячейка 0
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import sympy as smp

    mo.md("# Кривизна кубической параболы. Стилизованный символ М")
    return mo, np, plt, smp


@app.cell
def _(mo, smp):
    # ячейка 1
    smp.init_printing() # вывод формул с помощью LaTeX
    x, y = smp.symbols('x y') # создаем символьные переменные
    y = x**3 # кубическая парабола
    ys = smp.diff(y, x)
    ys2 = smp.diff(y, (x, 2))
    mo.hstack([x, y, ys, ys2])
    return x, ys, ys2


@app.cell
def _(mo):
    mo.md(r"""## Кривизна кубической параболы""")
    return


@app.cell
def _(smp, ys, ys2):
    # ячейка 2
    K = smp.Abs(ys2)/(smp.sqrt(1 + ys**2))**3
    K
    return (K,)


@app.cell
def _(K, np, plt, smp, x):
    Kl = smp.lambdify(x, K, 'numpy')
    xmax, n = 1.5, 1000
    xx = np.linspace(-xmax, xmax, n)
    yy = Kl(xx)
    _fig = plt.figure(figsize=(3,3))
    plt.plot(xx, yy, 'b-', lw=10)
    plt.axis('off')
    plt.savefig('e01_00.png', dpi=300, facecolor='white')
    _fig
    return Kl, xx, yy


@app.cell
def _(mo):
    mo.md(r"""## Рисуем кубическую параболу и график ее кривизны на одном рисунке""")
    return


@app.cell
def _(plt, xx, yy):
    _fig = plt.figure(figsize=(5,3))
    # рисунок для кубической параболы
    _ax = plt.subplot(111) 
    _line1 = _ax.plot(xx, xx**3, 'r-', 
                    lw=3, label='$y(x)$') # рисуем y(x)
    _ax.set_ylim(-.2, 3.) # граничные значения по y
    # надписи на осях для первого графика
    _ax.set_xlabel("$x, м$")
    _ax.set_ylabel("$y(x), м$")
    _ax.grid() # сетка

    # график для кривизны
    _ax2 = _ax.twinx() # сдваиваем рисунки
    _line2 = _ax2.plot(xx, yy, 'b-', 
                     lw=3, label="$K(x)$")
    _ax2.set_ylabel("$К(x), м^{-1}$")
    # выводим легенду
    _lines = _line1 + _line2 # линии
    _labels = [_l.get_label() for _l in _lines]
    _ax.legend(_lines, _labels, loc='best')

    plt.tight_layout()

    plt.savefig('e01_01.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""## Строим графики  кубической  параболы и кривизны от длины кубической параболы""")
    return


@app.cell
def _(smp, x, ys):
    l, t = smp.symbols('l t')
    l = smp.integrate(smp.sqrt(1+ys**2), (t, 0,x))
    ll = smp.lambdify(x, l, 'numpy')

    l
    return (ll,)


@app.cell
def _():
    return


@app.cell
def _(Kl, ll, plt, xx, yy):
    _fig = plt.figure(figsize=(5,3))
    # зависимости от длины пути
    _ax = plt.subplot(111) 
    _line1 = _ax.plot(xx, xx**3, 'r-', 
                    lw=3, label='$y(x)$') # рисуем y(x)
    _ax.set_ylim(-.2, 3.) # граничные значения по y
    #_ax.set_xlim(-2, 2.) # граничные значения по x
    # надписи на осях для первого графика
    _ax.set_xlabel("$x, м$")
    _ax.set_ylabel("$y(x), м$")
    _ax.grid() # сетка

    # графики для кривизны
    _ax2 = _ax.twinx() # сдваиваем рисунки
    _line2 = _ax2.plot(xx, yy, 'b-', 
                     lw=3, label="$K(x)$")
    _line3 = _ax2.plot(xx, Kl(ll(xx)), 'g-', 
                     lw=3, label="$K(l)$")

    _ax2.set_ylabel("$К(x), м^{-1}$")
    # выводим легенду
    _lines = _line1 + _line2 + _line3 # линии
    _labels = [_l.get_label() for _l in _lines]
    _ax.legend(_lines, _labels, loc='best')

    plt.tight_layout()

    plt.savefig('e02_01.png', dpi=300, facecolor='white')
    _fig
    return


if __name__ == "__main__":
    app.run()
