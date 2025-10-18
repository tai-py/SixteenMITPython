import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    mo.md("# Расчет температуры в стержне")
    return mo, np, plt


@app.cell
def _(np, plt):
    def bar(u0=0., dx =0.01, tmax=0.1, dt=1e-6, alpha=1.,
            C=1., D=10., p=1000.,
            draw=True, xs=0.5, ls='-'): 
        '''
        Расчет температуры в стержне
        u0 - температура окружающей среды
        dx - шаг по пространственной координате
        tmax -  время интегрирования
        dt - шаг по времени
        alpha - теплоотдача с единичы длины
        C - теплоемкость единицы длины стержня
        D - теплопроводность стержня
        p - мощность, выделяющаяся на единице длины стержня
        draw - признак рисования графика зависимости температуры от времени 
        xs - координата для которой рисуется график
        ls - стиль линии
        Функция возвращает масив распределения температур в стержне u,
        t - массив времен, x - массив координат, 
        '''
        nx = int(1./dx + 1) # число разбиений по x
        x = np.linspace(0.,1., nx) 
        nt = int(tmax/dt+1) # число разбиений по t
        t = np.linspace(0., tmax, nt) 
        A = dt/C*D/dx**2 
        B = 2*A + alpha*dt/C - 1
        P = np.ones((nt, nx))*(p + alpha*u0)*dt/C 
        u = np.zeros((nt, nx))+u0 
        for i in range(nt-1): # цикл по времени
            u[i+1, 1:-1] = A*u[i, 2:] - B*u[i, 1:-1] +\
                A*u[i, 0:-2] + P[i, 1:-1] 

        if draw:
            ix = int(u.shape[1]*xs)
            dxdt = dx/dt
            plt.plot(t, u[:, ix], lw=2, ls=ls,
                     label=f'{dx=:7.5e}, dx/dt={dxdt:7.5e} ')
            plt.xlabel('t') 
            plt.ylabel('u(t,x)')        
            plt.legend(fontsize=8)
        return u, t, x 

    _fig = plt.figure(figsize=(8,3))
    plt.subplot(121)
    ub, tb, xb = bar(dx=0.002, dt=2e-7)
    bar()
    bar(dx=0.2, ls='--')
    plt.subplot(122)
    bar(dx=0.002, dt=2e-7, ls='-')
    bar(dx=0.005, ls='-.')
    bar(dx=0.0044716, ls=':')

    plt.tight_layout()
    plt.savefig('03_01.png', dpi=300, facecolor='white') 
    _fig
    return bar, tb, ub, xb


@app.cell
def _(mo):
    mo.md(r"""##Сравниваем полученные решения""")
    return


@app.cell
def _(bar, np, tb, ub, xb):
    from scipy.interpolate import RectBivariateSpline as RBS

    def dists(ub, tb, xb, dxs=(0.2, 0.1, 0.05, 0.02, 0.01, 0.005)):
        dm, ds = [], []
        for dx in dxs:
            u_, t_, x_ = bar(dx=dx)
            ib = RBS(t_, x_, u_)
            ui = ib(tb, xb) 
            dmax = np.max(np.abs(ui - ub))/np.max(ub)
            dstd = np.std(ui - ub)/np.max(ub)
            dm.append(dmax)
            ds.append(dstd)
            print(f"{dx=}, {dmax=}, {dstd=}")
        return dxs, dm, ds

    dxs, dm, ds = dists(ub, tb, xb)
    return dm, ds, dxs


@app.cell
def _(dm, ds, dxs, plt):
    _fig = plt.figure(figsize=(5,3))
    plt.plot(dxs, dm, lw=3, label='максимальное расстояние')
    plt.plot(dxs, ds, lw=3, label='среднее квадратичное отклонение')
    plt.xlabel('dx')
    plt.ylabel('Отклонения')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid()
    plt.legend(fontsize=8)
    plt.savefig('03_02.png', dpi=300, facecolor='white') 
    _fig
    return


if __name__ == "__main__":
    app.run()
