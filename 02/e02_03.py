import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.optimize import root
    from scipy.optimize import newton
    mo.md("#Индустриальные методы поиска корней систем алгебраических уравнений")
    return mo, newton, np, plt, root


@app.cell
def _(newton):
    try:
        _r = newton(lambda x: x**2 +1, 1)
        print(f"{_r=}")

    except RuntimeError as _rt:    
        print(f"{_rt}")
    return


@app.cell
def _(newton):
    try:
        _r1 = newton(lambda x: x**2 +1, .1j)
        _r2 = newton(lambda x: x**2 +1, -1.1j)
        print(f"{_r1=}, {_r2=}")

    except RuntimeError as _rt:    
        print(f"{_rt}")
    return


@app.cell
def _(newton):
    f = lambda x : x**3 - 5*x**2 - 4.5

    (newton(f, -2,  tol=1e-10), 
     newton(f, -2j,  tol=1e-10), 
     newton(f, 1j,  tol=1e-10)
    )
    return (f,)


@app.cell
def _(f, newton):
    print(newton(f, -2,  tol=1e-10, full_output=True))
    return


@app.cell
def _(mo):
    mo.md(r"""
    Функция root
    """)
    return


@app.cell
def _(f, root):
    root(f, -2, tol=1e-10, method='hybr'), root(f, 4, tol=1e-10, method='hybr')
    return


@app.cell
def _(f, root):
    root(f, -2, tol=1e-10, method='lm'), root(f, 4, tol=1e-10, method='lm')
    return


@app.cell
def _(f, root):
    root(f, -2, tol=1e-10, method='broyden1'), root(f, 4, tol=1e-10, method='broyden1')
    return


@app.cell
def _(f, root):
    root(f, -2, tol=1e-10, method='broyden2'), root(f, 4, tol=1e-10, method='broyden2')
    return


@app.cell
def _(f, root):
    root(f, -2, tol=1e-10, method='linearmixing'), root(f, 4, tol=1e-10, method='linearmixing')
    return


@app.cell
def _(f, root):
    root(f, -2, tol=1e-10, method='diagbroyden'), root(f, 4, tol=1e-10, method='diagbroyden')
    return


@app.cell
def _(f, root):
    root(f, -2, tol=1e-10, method='krylov'), root(f, 4, tol=1e-10, method='krylov')
    return


@app.cell
def _(f, root):
    root(f, -2, tol=1e-10, method='df-sane'), root(f, 4, tol=1e-10, method='df-sane')
    return


@app.cell
def _(f, np, plt, root):
    _xlim = -20, 20
    _n = 2000
    _x = np.linspace(_xlim[0], _xlim[1], _n)
    _miniters, _maxiters = 10000, -1
    _fig = plt.figure(figsize=(12, 4))
    for _ in range(_n):
        try:
            _r = root(f, _x[_], method='df-sane')
            if _r.success: # успешное завершение
                _iters = _r.nit
                _miniters, _maxiters = min(_miniters, _iters), max(_maxiters, _iters)
                plt.plot(_x[_], _iters, 'bo', ms=2)
        except ValueError:
            ...
    plt.yscale('log')
    plt.grid()
    plt.xlabel('Начальное приближение')
    plt.ylabel('Число итераций')
    print(f"{_miniters=}, {_maxiters=}")
    plt.savefig("newton_05.png", dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ##Овалы Кассини, Толстого, лемниската Бернулли
    """)
    return


@app.cell
def _(np):
    oval_cassini = lambda x, y, a, c : (x**2 + y**2)**2 - 2*c**2*(x**2 - y**2) - (a**4 - c**4)
    oval_tolstoi = lambda x, y : oval_cassini(x, y, np.sqrt(2), 1)
    lemniscata = lambda x, y : oval_cassini(x - .5, y - .5, 2, 2)
    return lemniscata, oval_tolstoi


@app.cell
def _(lemniscata, np, oval_tolstoi, plt, root):
    _n = 500
    _x, _y = np.linspace(-3, 4, _n), np.linspace(-1.5, 2, _n)
    _X, _Y = np.meshgrid (_x, _y)
    _tolstoi = oval_tolstoi(_X, _Y)
    _bernulli = lemniscata(_X, _Y)

    _fig, _ax  = plt.subplots(figsize=(10, 10))
    _ax.contour(_X, _Y, _tolstoi, levels=[0], colors=['blue'] )
    _ax.contour(_X, _Y, _bernulli, levels=[0], colors=['red'] )
    _ax.grid()
    _ax.set_aspect(1)
    _ax.set_xlabel('x')
    _ax.set_xlabel('y')


    def _eq(u):
        return [oval_tolstoi(*u),  lemniscata(*u)]

    def _solution(x0, y0):    
        r = root(_eq, (x0, y0))    
        plt.plot(x0, y0, 'go', ms=10)
        if r.success:
            plt.arrow(x0, y0, r.x[0] - x0, r.x[1] - y0, ls=':', lw=.5)
            plt.plot(*r.x, 'k+', ms=15)
            return r.x
        return None
    _sol = []
    _sol.append(_solution(-2, -1))
    _sol.append(_solution(-2, 1.5))
    _sol.append(_solution(3, 1.5))
    _sol.append(_solution(3, -1))
    _sol.append(_solution(0, -.5))
    _sol.append(_solution(0, 1.5))
    _sol.append(_solution(-2, .5))
    _sol.append(_solution(1, 1.5))
    _sol.append(_solution(-2, .5))
    _sol.append(_solution(2, .5))
    _sol.append(_solution(0, -1.5))
    _sol.append(_solution(-3, 1))
    plt.savefig("newton_10.png", dpi=300, facecolor="white")
    _fig, _sol
    return


@app.cell
def _(lemniscata, newton, np, oval_tolstoi, plt):
    _n = 200
    _x, _y = np.linspace(-3, 4, _n), np.linspace(-1.5, 2, _n)
    _X, _Y = np.meshgrid (_x, _y)
    _tolstoi = oval_tolstoi(_X, _Y)
    _bernulli = lemniscata(_X, _Y)


    _fig, _ax  = plt.subplots(figsize=(10, 10))
    _ax.contour(_X, _Y, _tolstoi, levels=[0], colors=['blue'] )
    _ax.contour(_X, _Y, _bernulli, levels=[0], colors=['red'] )
    _ax.grid()
    _ax.set_aspect(1)
    _ax.set_xlabel('x')
    _ax.set_xlabel('y')


    def _eq(u):
        return [oval_tolstoi(*u),  lemniscata(*u)]

    def _solution(x0, y0):    
        #r = root(_eq, (x0, y0))
        r = newton(_eq, (x0, y0), maxiter=500, disp=False, full_output=True)
        # распаковываю результат
        x = r[1]
        success = np.all(r[1])
        #print(f"{r=}")
        plt.plot(x0, y0, 'go', ms=10)
        if np.all(r[1]):
            plt.arrow(x0, y0, x[0] - x0, x[1] - y0, ls=':', lw=.5)
            plt.plot(*x, 'k+', ms=15)
            return x
        return None
    _sol = []
    _sol.append(_solution(-2, -1))
    _sol.append(_solution(-2, 1.5))
    _sol.append(_solution(3, 1.5))
    _sol.append(_solution(3, -1))
    _sol.append(_solution(0, -.5))
    _sol.append(_solution(0, 1.5))
    _sol.append(_solution(-2, .5))
    _sol.append(_solution(1, 1.5))
    _sol.append(_solution(-2, .5))
    _sol.append(_solution(2, .5))
    _sol.append(_solution(0, -1.5))
    _sol.append(_solution(-3, 1))
    plt.savefig("newton_11.png", dpi=300, facecolor="white")
    _fig, _sol
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Области притяжения корней
    """)
    return


@app.cell
def _(lemniscata, np, oval_tolstoi, plt, root):
    def root_traction_areas(f,  rect, args=(), n=20,tol=1e-4, 
                            method = 'hybr',
                            nx=8, ny=8, fn=None,
                            figsize=(6,5), cmap="rainbow"):
        xmin, ymin, xmax, ymax = rect
        x, y = np.linspace(xmin, xmax, n), np.linspace(ymin, ymax, n)
        xy = np.zeros((n, n))
        roots = [None] # корни  уранения
        for i in range(n):
            for j in range(n):
                xx, yy = x[j], y[i]
                r = root(f, (xx, yy), args=args, method=method)
                if r.success:
                    s = r.x
                    root_num = 0
                    for k, xr in enumerate(roots):                     
                        if k>0 and np.max(np.abs(s - xr))<tol:
                            root_num = k
                            break
                    if root_num == 0:
                        root_num = len(roots)
                        roots.append(s)
                    xy[i, j] = root_num
        fig= plt.figure(figsize=figsize)            
        cb = plt.imshow(xy, cmap=cmap, origin="lower")

        plt.gca().set_xticks(np.linspace(0, n*(1-1/n), nx))
        plt.gca().set_xticklabels(np.linspace(xmin, xmax, nx))
        plt.gca().set_yticks(np.linspace(0, n*(1-1/n), ny))
        plt.gca().set_yticklabels(np.linspace(ymin, ymax, ny))
        plt.colorbar(cb)
        plt.xlabel('x')
        plt.ylabel('y')
        if fn:
            plt.savefig(fn, dpi=300, facecolor="white")            
        return fig, roots

    def eq(u):
        return [oval_tolstoi(*u),  lemniscata(*u)]

    root_traction_areas(eq,  (-3, -1.5, 4, 2), n=50, fn="newton_11a.png")
    return eq, root_traction_areas


@app.cell
def _(eq, root_traction_areas):
    root_traction_areas(eq,  (-3, -1.5, 4, 2), n=50, method='lm', 
                        fn="newton_11b.png")
    return


@app.cell
def _(eq, root_traction_areas):
    root_traction_areas(eq,  (-3, -1.5, 4, 2), n=50, 
                        method='linearmixing', fn="newton_11c.png")
    return


@app.cell
def _(eq, root_traction_areas):
    root_traction_areas(eq,  (-3, -1.5, 4, 2), n=50, method='broyden2', 
                        fn="newton_11d.png")
    return


if __name__ == "__main__":
    app.run()
