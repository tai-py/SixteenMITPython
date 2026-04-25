import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import sympy as smp
    import matplotlib.pyplot as plt

    mo.md("# Решаем уравнение маятника")
    return mo, np, plt, smp


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Делаем попытку аналитического решения
    """)
    return


@app.cell
def _(smp):
    # объявляем символьные переменные
    m, g, t, L,  α0 = smp.symbols('m, g, t, L, α0', positive=True)
    #m, g, t, L,  α0 = smp.symbols('m, g, t, L, α0')
    α,β = smp.Function('α'), smp.Function('β')
    return L, g, m, t, α, α0, β


@app.cell
def _():
    # Пытаемся решить исходную систему средствами sympy
    #smp.dsolve(smp.Eq(m*L*α(t).diff(t, 2), -m*g*smp.sin(α(t))))
    return


@app.cell
def _(mo):
    mo.md(r"""
    ###После часового запуска решение пришлось прервать
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Линеаризуем второе уравнение
    """)
    return


@app.cell
def _(L, g, m, smp, t, α, β):
    # Система дифференциальных уравнений
    eq1 = smp.Eq(α(t).diff(t),  β(t))
    eq2 = smp.Eq(m*L*β(t).diff(t), -m*g*α(t))
    return eq1, eq2


@app.cell
def _(eq1, eq2, smp, α, α0, β):
    # решаем систему уравнений
    result = smp.dsolve([eq1, eq2], ics={α(0):α0, β(0):0})
    result 
    return (result,)


@app.cell
def _(result):
    result[0].rhs, result[1].rhs
    return


@app.cell
def _(L, g, result, smp, t, α0):

    alpha = smp.lambdify((α0, g,t,L),result[0].rhs, 'numpy')
    beta = smp.lambdify((α0, g,t,L),result[1].rhs, 'numpy')
    return alpha, beta


@app.cell
def _(mo):
    mo.md(r"""
    ## Визуализация
    """)
    return


@app.cell
def _(alpha, beta, np, plt):
    tt = np.linspace(0, 10, 1000) # массивремен
    _fig, _ax = plt.subplots(nrows=1, ncols=1, figsize=(6,4))
    lns1 = _ax.plot(tt, alpha(1, 9.81, tt,1),'b-', lw=3, label=r'$\alpha(t)$')
    _ax2 = _ax.twinx()
    lns2 = _ax2.plot(tt, beta(1, 9.81, tt,1), 'r--', lw=3, label=r'$\frac{d\alpha(t)}{dt}$')
    _ax.set_xlabel(r'$t$')
    _ax.set_ylabel(r'$\alpha(t)$')
    _ax2.set_ylabel(r'$\frac{d\alpha(t)}{dt}$')
    lns = lns1+lns2
    labs = [l.get_label() for l in lns]
    _ax.legend(lns, labs, loc=4)
    plt.savefig('05_05.png', dpi=300, facecolor='white')
    _fig
    return (tt,)


@app.cell
def _(alpha, beta, plt, tt):
    Ls= .5, 1, 2 
    _fig = plt.figure(figsize=(6,6))

    for l in Ls:
        plt.plot(alpha(1, 9.81, tt,l), beta(1, 9.81, tt,l), label=f'$L={l}$')  
    plt.xlabel(r'$\alpha(t)$')
    plt.ylabel(r'$\frac{d\alpha(t)}{dt}$')
    plt.legend()
    plt.savefig('05_06.png', dpi=300, facecolor='white')
    plt.tight_layout()
    _fig
    return


if __name__ == "__main__":
    app.run()
