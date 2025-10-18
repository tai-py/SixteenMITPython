import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.integrate import solve_ivp # решение системы дифференциальных уравнений

    mo.md("# Решаем систему уравнений для гравитационного поезда")
    return mo, np, plt, solve_ivp


@app.cell
def _(np):
    # константы и переменные
    R = 6371_000. # Радиус Земли, м
    g = 9.81 # ускорение земного притяжения м/c^2
    m = 20_000 # масса поезда, кг
    S = 3 # площадь, учитывая при расчет сопротивления воздуха
    ρ_air = 1.25 # сопротивление воздуха, кг/м^3
    k = 0.01 # коэффициент пропорциональности
    f = 0.001 # коэффицент трения качения
    t_end =  420*60 # время интегрирования в c
    force = 0. # сила тяги поезда, Н

    n = 10_000 # число разбиений интервала времени
    t_eval = np.linspace(0, t_end, n)
    # начальные условия 
    x0 = -300_000 # начальное положение поезда, м
    v0 = 0. # начальная скорость поезда
    return R, S, f, force, g, k, m, t_end, t_eval, v0, x0, ρ_air


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Функция для вычисления правой части системы уравнения для гравитационного поезда (без учета трения)""")
    return


@app.function
def grav_train1(t, y, g, R, S, m, ρ_air, k, f):
    x, v = y # распаковка
    xs = v # первое уравнение системы
    vs = -g*x/R 
    return [xs, vs]


@app.cell
def _(mo):
    mo.md(r"""## Решаем систему без учета трения""")
    return


@app.cell
def _(R, S, f, g, k, m, solve_ivp, t_end, t_eval, v0, x0, ρ_air):
    y1 = solve_ivp(grav_train1, [0, t_end], y0=(x0, v0), 
                   method='RK45', t_eval=t_eval,
                   args=(g, R, S, m, ρ_air, k, f)
                  )
    y1.success, y1.message
    return (y1,)


@app.cell
def _(mo):
    mo.md(r"""### Визуализация решения без учета трения""")
    return


@app.cell
def _(plt, y1):
    def visualize_x_v_vs_t(y, figsize=(6, 4), fn=''):
        fig, ax = plt.subplots(nrows=1, ncols=1, 
                               figsize=figsize)
        lns1 = ax.plot(y.t/3600, y.y[0, :]/1000, 'b-', 
                lw=3, label='$x(t)$')
        ax.set_xlabel('$t$, час')
        ax.set_ylabel('$x(t)$, км')    
        ax2 = ax.twinx()
        lns2 = ax2.plot(y.t/3600, y.y[1, :]/1000*3600, 'r-',
                 lw=3, label='$v(t)$')
        ax2.set_ylabel('$v(t)$, км/час') 
        # легенда
        lns = lns1+lns2
        labs = [l.get_label() for l in lns]
        ax.legend(lns, labs, loc=1)
        if fn:
            plt.savefig(fn, dpi=300, facecolor='white')
        return fig 

    visualize_x_v_vs_t(y1)
    return (visualize_x_v_vs_t,)


@app.cell
def _(plt, y1):
    def phase_portrait(y, figsize=(6,6), fn=''):
        fig = plt.figure(figsize=figsize)
        plt.plot(y.y[0,:]/1000, y.y[1, :]/1000*3600, lw=3)
        plt.xlabel('$x(t)$, км')
        plt.ylabel('$v(t)$, км/час')
        if fn:
            plt.savefig(fn, dpi=300, facecolor='white')    
        return fig

    phase_portrait(y1)    
    return (phase_portrait,)


@app.cell
def _(mo):
    mo.md(r"""## Функция для вычисления правой части системы уравнения для гравитационного поезда""")
    return


@app.cell
def _(np):
    def grav_train2(t, y, g, R, S, m, ρ_air, k, f, force):
        x, v = y # распаковка
        xs = v # первое уравнение системы
        # второе уравнение системы 
        vs = -g*x/R \
             -np.sign(v)/m*k*ρ_air*S*v**2/2 \
             -np.sign(v)*f*g*np.sqrt(1 - (x/R)**2) \
             +np.sign(v)*force/m
        return [xs, vs]
    return (grav_train2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Решение системы""")
    return


@app.cell
def _(
    R,
    S,
    f,
    force,
    g,
    grav_train2,
    k,
    m,
    solve_ivp,
    t_end,
    t_eval,
    v0,
    x0,
    ρ_air,
):
    y2 = solve_ivp(grav_train2, [0, t_end], y0=(x0, v0), 
                   method='RK45', t_eval=t_eval,
                   args=(g, R, S, m, ρ_air, k, f, force)
                  )
    y2.success, y2.message
    return (y2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Визуализация решения""")
    return


@app.cell
def _(visualize_x_v_vs_t, y2):
    visualize_x_v_vs_t(y2, fn='05_16.png')
    return


@app.cell
def _(phase_portrait, y2):
    phase_portrait(y2, fn='05_17.png')   
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Выкачаем воздух и тоннеля""")
    return


@app.cell
def _(R, S, f, force, g, grav_train2, k, m, solve_ivp, t_end, t_eval, v0, x0):
    _ρ_air = 0.
    y3 = solve_ivp(grav_train2, [0, t_end], y0=(x0, v0), 
                   method='RK45', t_eval=t_eval,
                   args=(g, R, S, m, _ρ_air, k, f, force)
                  )
    y3.success, y3.message
    return (y3,)


@app.cell
def _(visualize_x_v_vs_t, y3):
    visualize_x_v_vs_t(y3)
    return


@app.cell
def _(phase_portrait, y3):
    phase_portrait(y3, fn='05_18a.png')  
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Добавляем силу тяги""")
    return


@app.cell
def _(R, S, f, g, grav_train2, k, m, solve_ivp, t_end, t_eval, v0, x0):
    _ρ_air, _force = 0., 200.
    y4 = solve_ivp(grav_train2, [0, t_end], y0=(x0, v0), 
                   method='RK45', t_eval=t_eval,
                   args=(g, R, S, m, _ρ_air, k, f, _force)
                  )
    y4.success, y4.message
    return (y4,)


@app.cell
def _(visualize_x_v_vs_t, y4):
    visualize_x_v_vs_t(y4)
    return


@app.cell
def _(phase_portrait, y4):
    phase_portrait(y4, fn='05_18b.png') 
    return


if __name__ == "__main__":
    app.run()
