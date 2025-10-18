import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import sympy as smp

    mo.md("# Аналитическое решение уравнения 8.1")
    return mo, np, plt, smp


@app.cell
def _(smp):
    # объявляем символьные переменные
    x0, y0, alpha = smp.symbols("x0, y0, alpha")

    def cheb01(alpha, r=15, L12=40, L=35):
        # точка 1
        x1, y1 = -L12, 0.
        # точка 2
        x2, y2 = 0., 0.
        # точка 3
        x3, y3 = r*smp.cos(alpha), r*smp.sin(alpha)
        # уравнения системы 8.1
        eq1 = (x0 - x1)**2 + (y0 - y1)**2 - L**2
        eq2 = (x0 - x3)**2 + (y0 - y3)**2 - L**2
        # решение системы
        solution = smp.solve([eq1, eq2], [x0, y0])
        return solution

    sol = cheb01(alpha) 
    return alpha, sol


@app.cell
def _(sol):
    len(sol)
    return


@app.cell
def _(smp, sol):
    # аналитическое решение системы
    x01, y01 = smp.simplify(sol[0][0]), smp.simplify(sol[0][1]) # первое решение
    x02, y02 = smp.simplify(sol[1][0]), smp.simplify(sol[1][1]) # второе решение
    return x01, x02, y01, y02


@app.cell
def _(x01):
    x01
    return


@app.cell
def _(y01):
    y01
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Перейдем от символьных переменных к обычным переменным Python""")
    return


@app.cell
def _(alpha, smp, x01, x02, y01, y02):
    x01p = smp.lambdify(alpha, x01, 'numpy')
    y01p = smp.lambdify(alpha, y01, 'numpy')
    x02p = smp.lambdify(alpha, x02, 'numpy')
    y02p = smp.lambdify(alpha, y02, 'numpy')
    return x01p, x02p, y01p, y02p


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Мы получили универсальные функции NumPy для вычисления координат точки (x0, y0).

    Теперь напишем функцию для вычисления координат остальных точек
    """
    )
    return


@app.cell
def _(np, plt, x01p, x02p, y01p, y02p):
    def coords(n, x0p, y0p, r=15, L12=40, L=35):
        angles = np.linspace(0, 2*np.pi, n)
        x0, y0 = x0p(angles), y0p(angles)
        x1, y1 = -L12, 0.
        x2, y2 =  0., 0.  
        x3, y3 = r*np.cos(angles), r*np.sin(angles)
        x4, y4 = 2*x0 - x3, 2*y0 - y3
        return x0, y0, x1, y1, x2, y2, x3, y3, x4, y4

    _fig, _ax = plt.subplots(figsize=(6,4))
    _n = 500
    _x0, _y0, _x1, _y1, _x2, _y2, _x3, _y3, _x4, _y4 = coords(_n, x01p, y01p)  
    _ax.plot(_x4, _y4, label="Решение 1", lw=3)
    _x0, _y0, _x1, _y1, _x2, _y2, _x3, _y3, _x4, _y4 = coords(_n, x02p, y02p)  
    _ax.plot(_x4, _y4, label="Решение 2", lw=3)
    #_ax.set_aspect(1)
    plt.legend()
    plt.savefig('08_04.png', dpi=300, facecolor="white")
    _fig
    return (coords,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Рисуем механизм для определенного положения точки x3, y3""")
    return


@app.cell
def _(np, plt, x02p, y02p):
    def mech(ax, n, x0p, y0p, a=0, r=15, L12=40, L=35, ms=5, lw=2, fs=12):
        angles = np.linspace(0, 2*np.pi, n)
        x0, y0 = x0p(angles), y0p(angles)
        x1, y1 = -L12, 0.
        x2, y2 =  0., 0.  
        x3, y3 = r*np.cos(angles), r*np.sin(angles)
        x4, y4 = 2*x0 - x3, 2*y0 - y3  
        fs2 = int(fs/4)
        # вычисляем индекс
        ind = int(a/360*n)    
        # геометрическое место точки 3
        ax.plot(x3, y3, 'k--', lw=lw)
        ax.text(x3[ind]+fs2,y3[ind]-fs2, '3', fontsize=fs)
        # геометрическое место точки 4
        ax.plot(x4, y4, 'k:', lw=lw)  

        # радиус    
        ax.plot(x2, y2, 'ko', ms=ms)
        ax.text(x2+fs2,y2+fs2, '2', fontsize=fs)
        ax.plot(x3[ind], y3[ind], 'ko', ms=ms)
        ax.plot([x2, x3[ind]], [y2, y3[ind]], 'k-', lw=lw)
        # 3-4
        ax.plot(x4[ind], y4[ind], 'ko', ms=ms)
        ax.text(x4[ind]+fs2,y4[ind]-fs2, '4', fontsize=fs)
        ax.plot([x3[ind], x4[ind]], [y3[ind], y4[ind]], 'k-', lw=lw)
        # 0-1
        ax.plot(x0[ind], y0[ind], 'ko', ms=ms)
        ax.text(x0[ind]+fs2,y0[ind]-fs2, '0', fontsize=fs)
        ax.plot(x1, y1, 'ko', ms=ms)
        ax.text(x1+fs2,y1+fs2, '1', fontsize=fs)
        ax.plot([x1, x0[ind]], [y1, y0[ind]], 'k-', lw=lw)
        ax.set_title(rf'$\alpha={a}$')

    _n = 500
    _fig, _ax = plt.subplots(figsize=(6,4))
    mech(_ax, _n, x02p, y02p, a=360-120)
    _ax.set_aspect(1)

    _fig
    return (mech,)


@app.cell
def _(mech, plt, x02p, y02p):
    _nrows, _ncols = 3,4
    _fig, _axs = plt.subplots(_nrows,_ncols,figsize=(12,9))
    _n = _nrows * _ncols
    _beta = 360 / _n
    _alpha = 0
    _n=500
    for _row in range(_nrows):    
        for _col in range(_ncols):
            mech(_axs[_row, _col], _n, x02p, y02p, a = _alpha)
            _alpha += _beta
    plt.tight_layout()   
    plt.savefig('08_05.png', dpi=300, facecolor="white")
    _fig   
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Создаем анимацию""")
    return


@app.cell
def _(mech, plt, x02p, y02p):
    import gif

    nframes = 180
    figsize = (6, 6)
    beta = 360//nframes

    @gif.frame
    def play(i):
        ''' i-ый кадр анимации'''
        fig, ax = plt.subplots(figsize=figsize)
        alpha = beta * i
        mech(ax, 500, x02p, y02p, a=alpha)
        return fig

    # формирую последовательность кадров
    frames = [play(i) for i in range(nframes)]

    # сохраняю анимацию
    gif.save(frames, "08_anim1.gif", duration=50)
    return beta, figsize, gif, nframes


@app.cell
def _(mo):
    mo.md(r"""## Вставляем анимацию""")
    return


@app.cell
def _(mo):
    mo.image("08_anim1.gif")
    return


@app.cell
def _(beta, figsize, gif, mech, nframes, plt, x01p, y01p):
    @gif.frame
    def play1(i):
        ''' i-ый кадр анимации'''
        fig, ax = plt.subplots(figsize=figsize)
        alpha = beta * i
        mech(ax, 500, x01p, y01p, a=alpha)
        return fig

    # формирую последовательность кадров
    frames1 = [play1(i) for i in range(nframes)]

    # сохраняю анимацию
    gif.save(frames1, "08_anim2.gif", duration=50)
    return


@app.cell
def _(mo):
    mo.image("08_anim2.gif")
    return


@app.cell
def _(mo):
    mo.md(r"""## Исследуем критические точки""")
    return


@app.cell
def _(coords, np, x02p, y02p):
    _n = 1000
    _x0, _y0, _x1, _y1, _x2, _y2, _x3, _y3, _x4, _y4 = coords(_n, x02p, y02p) 
    _dxp = _x4[2:] - _x4[1:-1]
    _dxm = _x4[1:-1] - _x4[:-2]
    _ind2 = np.where((_dxp>0) & (_dxm<0)) 
    _ind1 = np.where((_dxp<0) & (_dxm>0))
    _x4[_ind1], _y4[_ind1], _x4[_ind2], _y4[_ind2], np.min(_y4), np.max(_y4)
    return


@app.cell
def _(coords, np, plt, x02p, y02p):
    def f(n=1000, figsize=(6, 4)):
        x0, y0, x1, y1, x2, y2, x3, y3, x4, y4 = coords(n, x02p, y02p) 
        dxp = x4[2:] - x4[1:-1]
        dxm = x4[1:-1] - x4[:-2] 
        ind1 = np.where((dxp<0) & (dxm>0))
        ind2 = np.where((dxp>0) & (dxm<0)) 
        xmin = np.min(x4)
        xmax = np.max(x4)
        ymin = np.min(y4)
        ymax = np.max(y4)  
        ylevel = (y4[ind1] + y4[ind2])/2
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(x4, y4, 'k-')
        ax.plot([xmin, xmax], [ylevel, ylevel], 'k-', lw=0.5)
        ax.plot([xmin, xmax], [ymin, ymin], 'k-', lw=0.5)        
        return fig, ylevel - ymin

    f()

    return


if __name__ == "__main__":
    app.run()
