import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import sympy as smp
    mo.md("# Пытаемся все параметры  перетащить в sympy")
    return mo, np, plt, smp


@app.cell
def _(smp):
    # объявляем символьные переменные
    x0, y0, alpha, L01, L03, L12, L04 = \
        smp.symbols("x0, y0, alpha, L01, L03, L12, L04")

    def cheb04(alpha, L01=L01, L03=L03, L12=L12, L04=L04, r=15):
        # точка 1
        x1, y1 = -L12, 0.
        # точка 2
        x2, y2 = 0., 0.
        # точка 3
        x3, y3 = r*smp.cos(alpha), r*smp.sin(alpha)
        # уравнения системы 8.1
        eq1 = (x0 - x1)**2 + (y0 - y1)**2 - L01**2
        eq2 = (x0 - x3)**2 + (y0 - y3)**2 - L03**2
        # решение системы
        solution = smp.solve([eq1, eq2], [x0, y0])
        return solution

    sol = cheb04(alpha) 
    return L01, L03, L04, L12, alpha, sol


@app.cell
def _(mo):
    mo.md(r"""
    Решение заняло более минуты
    """)
    return


@app.cell
def _(L01, L03, L04, L12, alpha, smp, sol):
    def get_x0(sol, alpha, L01, L03, L12, L04):
        # аналитическое решение системы
        x01, y01 = sol[0][0], sol[0][1] # первое решение
        x02, y02 = sol[1][0], sol[1][1] # второе решение    
        # решения
        x01p = smp.lambdify((alpha, L01, L03, L12, L04), x01, 'numpy')
        y01p = smp.lambdify((alpha, L01, L03, L12, L04), y01, 'numpy')
        x02p = smp.lambdify((alpha, L01, L03, L12, L04), x02, 'numpy')
        y02p = smp.lambdify((alpha, L01, L03, L12, L04), y02, 'numpy') 
        return x01p, y01p, x02p, y02p

    x01p, y01p, x02p, y02p = get_x0(sol, alpha, L01, L03, L12, L04)
    return x01p, x02p, y01p, y02p


@app.cell
def _(np, x01p, y01p):
    def coords(n, x0, y0, r=15,  L01=25, L03=20, 
               L12=20., L04=20.):
        angles = np.linspace(np.pi, 3*np.pi, n)
        xy = np.zeros((10, n))
        xy[0, :] = x0(angles,  L01, L03, L12, L04) # x0
        xy[1, :] = y0(angles,  L01, L03, L12, L04) # y0
        xy[2, :] = -L12 # x1
        xy[3, :] = 0.   # y1
        xy[4, :] = 0.   # x2
        xy[5, :] = 0.   # y2
        xy[6, :] = r*np.cos(angles)    # x3
        xy[7, :] = r*np.sin(angles)    # y3
        xy[8, :] = (xy[0, :]*(L03 + L04) - L04*xy[6, :])/L03   # x4
        xy[9, :] = (xy[1, :]*(L03 + L04) - L04*xy[7, :])/L03   # y4
        return xy

    coords(5, x01p, y01p) 
    return (coords,)


@app.cell
def _(coords, plt, x02p, y02p):
    def motion_path4(ax, n, x0, y0, r=15,
                     n1 = 0, n2=-1,
                     L01=25, L03=20, L12=20., 
                     L04=20, figsize=(4, 4)):
        xy = coords(n, x0, y0, r,  L01, L03, L12, L04)    
        ax.plot(xy[8, :], xy[9, :], 'k-')
        ax.plot(xy[8, n1:n2], xy[9, n1:n2], 'r-', lw=3)   

    n = 1000
    # создаем рисунки на холсте
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(12, 4))
    motion_path4(ax[0], n, x02p, y02p, n1=150, n2=850, 
                 L01=25, L03=20, L12=20, L04=20)

    motion_path4(ax[1], n, x02p, y02p, n1=150, n2=850, 
                 L01=45, L03=45, L12=40., L04=45)
    motion_path4(ax[2], n, x02p, y02p, n1=150, n2=850, 
                 L01=39.4, L03=39.4, L12=31.23, L04=39.4)
    for _ in range(3):
        ax[_].set_xlabel('x')
        ax[_].set_ylabel('y')
    plt.tight_layout()
    plt.savefig('08_07.png', dpi=400, facecolor='white')
    fig
    return


@app.cell
def _(coords, np, x02p, y02p):
    def goal(u):
        n=1000 # число точек траектории
        # распаковываем параметры
        L01, L03, L12, L04 = u
        # вычисляем значение координат
        xy = coords(n, x02p, y02p, r=15,  L01=L01, L03=L03, 
               L12=L12, L04=L04)
        miny = np.min(xy[9]) # нижняя точка траектории
        medy = np.median(xy[9])  # медиана
        return abs(medy - miny) 

    goal((40,40., 20., 40.))
    return (goal,)


@app.cell
def _(goal):
    from scipy.optimize import minimize
    _u0 = 39.4, 39.4, 25, 39.4
    minimize(goal, _u0, method='nelder-mead',  options=dict(xatol=1e-3))
    return (minimize,)


@app.cell
def _(goal, minimize):
    _u0 = 39.4, 39.4, 31.23, 39.4
    minimize(goal, _u0, method='nelder-mead')
    return


@app.cell
def _(goal, minimize):
    _u0 = 39.4, 39.4, 26, 39.4
    minimize(goal, _u0, method='COBYLA')
    return


@app.cell
def _(coords, goal, minimize, plt, x02p, y02p):

    def optimize_(goal=goal, initial_guess=(45, 39.4, 26, 39.4),xatol=0.001,
                 r=15, n=1000, figsize=(4,4), 
                 x0=x02p, y0=y02p, fs=8):

        fig, ax = plt.subplots(figsize=figsize)
        L01, L03, L12, L04 = initial_guess
        xy = coords(n, x0, y0, r,  L01, L03, L12, L04)

        ax.plot(xy[8, :], xy[9, :], 'b-', label="начальное приближение")

        result = minimize(goal, initial_guess, options=dict(xatol=xatol), 
                          method='nelder-mead')
        if result.success:
            xy = coords(n, x0, y0, r, *result.x)
            ax.plot(xy[8, :], xy[9, :], 'r-', 
                    label="результат оптимизации", lw=3)
            fun = result.fun
            x = result.x
        else:
            fun = None
            x = None
        ax.legend(fontsize=fs)
        return fig, fun, x

    fig1, fun1, x1 = optimize_(xatol=1.0e-8)    
    fig1, fun1, x1
    return (x1,)


@app.cell
def _(coords, goal, minimize, plt, x02p, y02p):
    def optimize(ax, goal=goal, initial_guess=(45, 39.4, 26, 39.4),xatol=0.001,
                 r=15, n=1000, figsize=(4,4), 
                 x0=x02p, y0=y02p, fs=8):    
        L01, L03, L12, L04 = initial_guess
        xy = coords(n, x0, y0, r,  L01, L03, L12, L04)

        ax.plot(xy[8, :], xy[9, :], 'b-', label="начальное приближение")
        result = minimize(goal, initial_guess, options=dict(xatol=xatol), 
                          method='nelder-mead')
        if result.success:
            xy = coords(n, x0, y0, r, *result.x)
            ax.plot(xy[8, :], xy[9, :], 'r-', 
                    label="результат оптимизации", lw=3)        
            fun = result.fun
            x = result.x
        else:
            fun = None
            x = None
        ax.legend(fontsize=fs)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(f"L01={L01:5.1f}, L03={L03:5.1f}, L12={L12:5.1f}, L04={L03:5.1f}", 
                     fontsize=fs+2) #f"L01={L01:5.1f}"
        return fun, x

    _fig, _ax = plt.subplots(nrows=2, ncols=2, figsize=(8, 8))
    _fun, _x = optimize(_ax[0,0])
    _fun, _x = optimize(_ax[0,1], initial_guess=(45, 45, 40, 50))
    _fun, _x = optimize(_ax[1,0], initial_guess=(35, 40, 40, 55))
    _fun, _x = optimize(_ax[1,1], initial_guess=(50, 35, 45, 35))
    plt.tight_layout()
    plt.savefig("08_08.png", dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(goal, minimize, x1):
    _r = minimize(goal, x1, method='COBYLA')
    _r.x, _r.fun
    return


if __name__ == "__main__":
    app.run()
