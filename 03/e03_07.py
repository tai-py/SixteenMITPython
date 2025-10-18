import marimo

__generated_with = "0.16.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from Ivl import Ivl
    import mpmath as mp

    mo.md("# Численное дифференциирование с помощью интервальной арифметики")
    return Ivl, mp, np, plt


@app.cell
def _(Ivl, np):
    def diff(f, fs,  ab=(0,1), h=0.01, epsx=0., epsf=0., n=20):    
        '''
        Численное дифференцирование с помощью интервальной арифметики
        f - дифференцируемая функция f(x)
        fs - производная функции f(x)
        ab - отрезок, на котором задана функция
        h - шаг, используемый при численном дифференцировании
        epsx, epsf - погрешности задания x и f
        n - число разбиений отрезка ab
        Функция возвращает максимальные погрешность вычисления 
        производной и ширину интервала на отрезке ab

        '''
        x = np.linspace(*ab, n+1)
        xi = Ivl(x, eps=epsx) 
        xim, xip = xi - h, xi + h
        yim = xim.apply(f, delta=epsf)
        yip = xip.apply(f, delta=epsf)
        # считаем производную
        d = (yip - yim)/(2*h)
        da = d.a
        dm = d.mid
        db = d.b
        ddelta = d.delta
        dmax = np.max(ddelta)
        # погрешность вычисления производной
        errmax = np.max(np.abs(fs(x) - dm))
        return errmax, dmax

    _f = lambda x:x**3
    _fs = lambda x: 3*x**2
    diff(_f, _fs,  ab=(0,1), h=0.2, epsx=0., epsf=0., n=20)
    return (diff,)


@app.cell
def _(diff, mp, np):
    _f = lambda x: mp.iv.cos(x)
    _fs = lambda x: -np.sin(x)
    diff(_f, _fs,  ab=(0,1), h=0.2, epsx=0., epsf=0., n=20)
    return


@app.cell
def _(diff, mp, np, plt):
    def draw_diff(f, fs, fig,  ab=(0,1), 
                  hs=(0.2, 0.1, 0.01, 0.001, 0.0001),
                  epsx=0., epsf=0., n=10, fsize=8, lw=3): 
        errs, deltas = [], []
        for h in hs:
            err, delta = diff(f, fs,  ab, h, epsx, epsf, n)
            errs.append(err)
            deltas.append(delta)
        plt.subplot(121)
        plt.plot(hs, errs, lw=3,
                 label=rf"$\varepsilon_x$={epsx:5.2e}, $\varepsilon_f$={epsf:5.2e}")
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('h')
        plt.ylabel('Погрешность')
        plt.legend(fontsize=fsize)

        plt.subplot(122)
        plt.plot(hs, deltas, lw=3,
                 label=rf"$\varepsilon_x$={epsx:5.2e}, $\varepsilon_f$={epsf:5.2e}")
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('h')
        plt.ylabel(r'$\delta (h)$') 
        plt.legend(fontsize=fsize)    
        plt.tight_layout()




    _f = lambda x: mp.iv.cos(x)
    _fs = lambda x: -np.sin(x)
    _fig = plt.figure(figsize=(8,3))
    draw_diff(_f, _fs, _fig, epsx=0., epsf=0.)
    draw_diff(_f, _fs, _fig, epsx=0.0001, epsf=0.0001)
    draw_diff(_f, _fs, _fig, epsx=0.001, epsf=0.001)
    draw_diff(_f, _fs, _fig, epsx=0.01, epsf=0.01)
    draw_diff(_f, _fs, _fig, epsx=0.05, epsf=0.05)
    # draw_diff(_f, _fs, _fig, epsx=0.0, epsf=0.1)
    # draw_diff(_f, _fs, _fig, epsx=0.1, epsf=0.0)
    plt.savefig('03_06.png', dpi=300, facecolor='white')
    _fig
    return (draw_diff,)


@app.cell
def _(draw_diff, plt):
    _f = lambda x: x**3
    _fs = lambda x: 3*x**2
    _fig = plt.figure(figsize=(8,3))
    draw_diff(_f, _fs, _fig, epsx=0., epsf=0.)
    draw_diff(_f, _fs, _fig, epsx=0.0001, epsf=0.0001)
    draw_diff(_f, _fs, _fig, epsx=0.001, epsf=0.001)
    draw_diff(_f, _fs, _fig, epsx=0.01, epsf=0.01)
    draw_diff(_f, _fs, _fig, epsx=0.05, epsf=0.05)
    # draw_diff(_f, _fs, _fig, epsx=0.0, epsf=0.1)
    # draw_diff(_f, _fs, _fig, epsx=0.1, epsf=0.0)
    plt.savefig('eЩ_06a.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(draw_diff, mp, np, plt):
    _f = lambda x: mp.iv.sin(x)
    _fs = lambda x: np.cos(x)
    _fig = plt.figure(figsize=(8,3))
    draw_diff(_f, _fs, _fig, epsx=0., epsf=0.)
    draw_diff(_f, _fs, _fig, epsx=0.0001, epsf=0.0001)
    draw_diff(_f, _fs, _fig, epsx=0.001, epsf=0.001)
    draw_diff(_f, _fs, _fig, epsx=0.01, epsf=0.01)
    draw_diff(_f, _fs, _fig, epsx=0.05, epsf=0.05)
    # draw_diff(_f, _fs, _fig, epsx=0.0, epsf=0.1)
    # draw_diff(_f, _fs, _fig, epsx=0.1, epsf=0.0)
    plt.savefig('eЩ_06b.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(draw_diff, plt):
    _f = lambda x: x**6
    _fs = lambda x: 6*x**5
    _fig = plt.figure(figsize=(8,3))
    draw_diff(_f, _fs, _fig, epsx=0., epsf=0.)
    draw_diff(_f, _fs, _fig, epsx=0.0001, epsf=0.0001)
    draw_diff(_f, _fs, _fig, epsx=0.001, epsf=0.001)
    draw_diff(_f, _fs, _fig, epsx=0.01, epsf=0.01)
    draw_diff(_f, _fs, _fig, epsx=0.05, epsf=0.05)
    # draw_diff(_f, _fs, _fig, epsx=0.0, epsf=0.1)
    # draw_diff(_f, _fs, _fig, epsx=0.1, epsf=0.0)
    plt.savefig('eЩ_06c.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(draw_diff, mp, np, plt):
    _f = lambda x: mp.iv.exp(x)
    _fs = lambda x: np.exp(x)
    _fig = plt.figure(figsize=(8,3))
    draw_diff(_f, _fs, _fig, epsx=0., epsf=0., ab=(0,3))
    draw_diff(_f, _fs, _fig, epsx=0.0001, epsf=0.0001, ab=(0,3))
    draw_diff(_f, _fs, _fig, epsx=0.001, epsf=0.001, ab=(0,3))
    draw_diff(_f, _fs, _fig, epsx=0.01, epsf=0.01, ab=(0,3))
    draw_diff(_f, _fs, _fig, epsx=0.05, epsf=0.05, ab=(0,3))

    plt.savefig('03_07.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(draw_diff, mp, np, plt):
    _f = lambda x: mp.iv.exp(x)
    _fs = lambda x: np.exp(x)
    _fig = plt.figure(figsize=(8,3))
    draw_diff(_f, _fs, _fig, epsx=0., epsf=0., ab=(0,3))
    draw_diff(_f, _fs, _fig, epsx=0.0, epsf=0.0001, ab=(0,3))
    draw_diff(_f, _fs, _fig, epsx=0.0, epsf=0.001, ab=(0,3))
    draw_diff(_f, _fs, _fig, epsx=0.0, epsf=0.01, ab=(0,3))
    draw_diff(_f, _fs, _fig, epsx=0.0, epsf=0.05, ab=(0,3))
    plt.savefig('03_06.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
