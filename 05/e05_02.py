import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.integrate import solve_ivp # решение системы дифференциальных уравнений

    mo.md("# Решаем систему уравнений для маятника численно")
    return mo, np, plt, solve_ivp


@app.cell
def _(np):

    def pendulum1(t, y, g, L):
        α, β = y
        return [β, - g/L*np.sin(α)] # исходная система уравнений

    def pendulum2(t, y, g, L):
        α, β = y
        return [β, - g/L*α] # линеарисованная система

    return pendulum1, pendulum2


@app.cell
def _(np):
    t0, tmax = 0., np.pi # интервал времен
    g, L = 9.81, 1.
    α0, β0 = 2*np.pi/3, 0.
    n = 10_000
    t = np.linspace(t0, tmax, n)    
    return L, g, n, t, t0, tmax, α0, β0


@app.cell
def _(mo):
    mo.md(r"""
    ## Решение систем уравнений
    """)
    return


@app.cell
def _(L, g, pendulum1, pendulum2, solve_ivp, t, t0, tmax, α0, β0):
    y1 = solve_ivp(pendulum1, y0=(α0, β0), 
                   t_span=(t0, tmax), t_eval=t, args=(g, L))

    y2 = solve_ivp(pendulum2, y0=(α0, β0), 
                   t_span=(t0, tmax), t_eval=t, args=(g, L))

    y1.success, y2.success
    return y1, y2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Визуализация
    """)
    return


@app.cell
def _(plt, t, y1, y2):
    _fig, _axs = plt.subplots(nrows=2, ncols=1, figsize=(6, 8))
    _axs[0].plot(t, y1.y[0, :],lw=3, label=r"$исходная\ система\ уравнений$")
    _axs[0].plot(t, y2.y[0, :],lw=3, label=r"$линеаризованная\ система\ уравнений$")
    _axs[0].set_xlabel('$t$')
    _axs[0].set_ylabel(r'$\alpha(t)$')
    _axs[0].legend()
    _axs[1].plot(t, y1.y[1, :],lw=3, label=r"$исходная\ система\ уравнений$")
    _axs[1].plot(t, y2.y[1, :], lw=3, label=r"$линеаризованная\ система\ уравнений$")
    _axs[1].legend()
    _axs[1].set_xlabel('$t$')
    _axs[1].set_ylabel(r'$\beta(t)$')
    plt.tight_layout()
    plt.savefig('05_07.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(plt, y1, y2):
    _fig= plt.figure(figsize=(6, 6))
    plt.plot(y1.y[0, :], y1.y[1, :], lw=3, label=r"$исходная\ система\ уравнений$")
    plt.plot(y2.y[0, :], y2.y[1, :], lw=3, label=r"$линеаризованная\ система\ уравнений$")
    plt.xlabel(r'$\alpha(t)$')
    plt.ylabel(r'$\beta(t)$')
    plt.legend()
    plt.savefig('05_08.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Зависимость колебаний от начального угла $\alpha_0$
    """)
    return


@app.cell
def _(L, g, n, np, pendulum1, pendulum2, plt, solve_ivp, t0, β0):
    a0s = 10, 60, 132, 160, 171,  175, 179.9 # , 178.1, 179.15
    _n = len(a0s)
    _tmax=8.
    _fig, _axs = plt.subplots(nrows=_n, ncols=1, figsize=(6, 15))
    _t = np.linspace(t0, _tmax, n)
    for _, _a in enumerate(a0s):
        _α0 = _a/180*np.pi
        _y1 = solve_ivp(pendulum1, y0=(_α0, β0), 
                   t_span=(t0, _tmax), t_eval=_t, args=(g, L))

        _y2 = solve_ivp(pendulum2, y0=(_α0, β0), 
                   t_span=(t0, _tmax), t_eval=_t, args=(g, L))
        _axs[_].plot(_t, _y1.y[0, :], lw=3, label=r"$исходная\ система\ уравнений$")
        _axs[_].plot(_t, _y2.y[0, :], lw=3, label=r"$линеаризованная\ система\ уравнений$")
        _axs[_].set_title(rf"$\alpha_0=${_a}$^o$")
        _axs[_].set_xlabel('$t$')
        _axs[_].set_ylabel(r'$\alpha(t)$')
    plt.tight_layout()
    plt.savefig('05_09.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _():
    # Значения переменных
    R = 6371_000 # радиус Земли, м
    S = 3 # м^2
    m = 20_000 # вес поезда, кг
    ρ_air = 1.25 # сопротивление воздуха, кг/м^3
    k = 0.01 # коэффициент прпорциональностми
    f = 0.001 # коэффицент трения качения
    t_end = 50000 #500*60 # время интегрирования, с
    n_g = 100 # число разбиений интервала времени

    # начальные условия 
    x0 = -300_000 # начальное положение поезда, м
    v0 = 0. # начальная скорость поезда
    return


if __name__ == "__main__":
    app.run()
