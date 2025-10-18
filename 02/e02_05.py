import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    mo.md("# Возвращаемся к методу Ньютона")
    return mo, np, plt


@app.function
def newton(f, fs, x0, args=(), tol=1e-6, maxiters=100):
    for iters in range(maxiters+1):
        f0 = f(x0,*args)
        x = x0 - f0/fs(x0, *args)
        if abs(x - x0) < tol or abs(f0) < tol:
            break
        x0 = x
    if iters < maxiters:
        return x, iters
    else:
        return None, maxiters


@app.cell
def _(np, plt):
    def iters_distribution(f=lambda z:z**3-1, 
                            fs=lambda z:3*z**2, n= 400, m=5, 
                            args=(), rect=(-1., -1., 1., 1), 
                            iters=200, tol=1e-10, cmap='rainbow', 
                            figsize=(8,6), fn=''):
        xmin, ymin, xmax, ymax = rect
        x = np.linspace(xmin, xmax, n)
        y = np.linspace(ymin, ymax, n)
        X, Y = np.meshgrid(x, y) 
        Z = X +1j*Y
        I = np.zeros((n,n), dtype=np.int32) 
        for i in range(n):
            for j in range(n):
                root, it = newton(f, fs, x0=Z[i,j],                            
                    args=args, maxiters=iters, tol=tol)
                if not (root is None):
                    I[i,j] = it 
        fig = plt.figure(figsize=figsize)
        cb = plt.imshow(I, cmap=cmap) 
        plt.colorbar(cb)
        plt.xticks( np.linspace(0, n, m+1),  
           ['{0:4.3f}'.format(xmin+(xmax-xmin)*i/m) 
           for i in range(m+1)])
        plt.yticks( np.linspace(0, n, m+1), 
           ['{0:4.3f}'.format(ymin+(ymax-ymin)*i/m) 
           for i in range(m+1)])
        plt.xlabel('x')
        plt.ylabel('y')
        if fn:
            plt.savefig(fn, dpi=300, facecolor='white')
        return fig

    iters_distribution(fn="02_17a.png")
    return (iters_distribution,)


@app.cell
def _(iters_distribution):
    iters_distribution(n=400, 
                        rect=(-1, -0.25, -0.6, .25), fn="02_17b.png")
    return


@app.cell
def _(iters_distribution):
    iters_distribution(n=400, cmap="rainbow", tol=1e-10,
                        rect=(-1.01, -0.04, -0.99, 0.04))
    return


@app.cell
def _(iters_distribution):
    iters_distribution(n=400, cmap="rainbow", tol=1e-10,
                        rect=(-0.840, 0.022, -0.830, 0.032), fn="02_17c.png")
    return


@app.cell
def _(iters_distribution):
    iters_distribution(f=lambda z: z**5 + 1, fs=lambda z:5*z**4, 
                        n=400, cmap="rainbow")
    return


@app.cell
def _(iters_distribution):
    iters_distribution(f=lambda z: z**11 + 1, fs=lambda z:11*z**10, 
                        n=400, cmap="rainbow", fn='02_17d.png')
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    iters_distribution(f=lambda z: z**11 - 1, fs=lambda z:11*z**10, 
                        n=600, cmap="rainbow")
    """
    )
    return


@app.cell
def _(iters_distribution):
    iters_distribution(f=lambda z: z**5 + z**3, fs=lambda z:5*z**5-3*z**2, 
                        n=400, cmap="rainbow", rect=(-.5, -1.5, 2.5, 1.5), fn="02_18a.png")
    return


@app.cell
def _(iters_distribution):
    iters_distribution(f=lambda z: z**(5+5j), fs=lambda z: (5+5j)*z**(4+5j), 
                        n=400, cmap="rainbow", rect=(-1, -1, 1, 1), fn="02_18b.png")
    return


@app.cell
def _(iters_distribution):
    iters_distribution(f=lambda z: z**3-z, fs=lambda z: 3*z**2 -1, 
                        n=400, cmap="rainbow", rect=(-1, -1, 1, 1), fn="02_18c.png")
    return


@app.cell
def _(iters_distribution):
    iters_distribution(f=lambda z: z**3-2*z+2, fs=lambda z: 3*z**2 - 2,
                        n=400, cmap="rainbow", rect=(-2, -2, 2, 2), fn="02_18d.png")
    return


@app.cell
def _(mo):
    mo.md(r"""## Используем штатную библиотечную функцию""")
    return


@app.cell
def _(np, plt):
    from scipy.optimize import newton as newton2

    def iters_distribution2(f=lambda z:z**3-1, 
                            fs=lambda z:3*z**2, n= 200, m=5,
                            args=(), rect=(-1., -1., 1.,1), 
                            iters=200, tol=1e-5, cmap='binary', 
                            figsize=(8,6)):
        xmin, ymin, xmax, ymax = rect
        x = np.linspace(xmin, xmax, n)
        y = np.linspace(ymin, ymax, n)
        X, Y = np.meshgrid(x, y) 
        Z = X +1j*Y
        I = np.ones((n,n), dtype=np.int32)*iters 
        for i in range(n):
            for j in range(n):
                r = newton2(f, Z[i,j],  fs,                           
                    args=args, maxiter=iters, tol=tol, full_output=True)
                #print(f"{r=}")
                if r[1].converged:
                    I[i,j] = r[1].iterations
        fig = plt.figure(figsize=figsize)
        cb = plt.imshow(I, cmap=cmap) 
        plt.colorbar(cb)
        plt.xticks( np.linspace(0, n, m+1),  
           ['{0:4.3f}'.format(xmin+(xmax-xmin)*i/m) 
           for i in range(m+1)])
        plt.yticks( np.linspace(0, n, m+1), 
           ['{0:4.3f}'.format(ymin+(ymax-ymin)*i/m) 
           for i in range(m+1)])
        plt.xlabel('x')
        plt.ylabel('y')
        return fig

    iters_distribution2(n=400)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
