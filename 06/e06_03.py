import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo 
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit

    mo.md("# Нелинейная аппроксимация")
    return curve_fit, np, plt


@app.cell
def _(np):

    def gaussian(x, a, x0, sigma):
        '''Единичный колокол'''
        return a * np.exp(-(x-x0)**2/(2*sigma**2))

    def err(f, x, y, c):
        ''' Вычисление погрешности аппроксимации'''
        return np.max(np.abs(y-f(x, *c)))

    return err, gaussian


@app.cell
def _(curve_fit, err, gaussian, np, plt):
    def test_approximation(f, p, n=1000, xminmax=(0., 10), 
                           s=0., p0=None, 
                           figsize=(6, 4), lw=3, fn=None):
        # генерируем данные
        x = np.linspace(*xminmax, n)
        y = f(x, *p) + np.random.normal(0, s, n)
        # ищем коэффициенты аппроксимирующей функции
        if p0:
            с = curve_fit(f, x, y, p0=p0)
        else:
            с = curve_fit(f, x, y)

        # аппроксимация
        ya = f(x, *с[0])
        error = err(f, x, y, с[0])

        # визуализация
        fig = plt.figure(figsize=figsize)
        plt.plot(x, y, 'b-', lw=lw, label='Исходные данные')
        plt.plot(x, ya, 'r-', lw=lw, label='Аппроксимация')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        if fn:
            plt.savefig(fn, dpi=300, facecolor='white')

        return с[0], error, fig

    test_approximation(gaussian, p=(1, 5, 2), fn='06_11a.png')
    return (test_approximation,)


@app.cell
def _(gaussian, test_approximation):
    test_approximation(gaussian, p=(1, 5, 2), s=.3, fn='06_11b.png')
    return


@app.cell
def _(np, test_approximation):
    def gaussian2(x, a1, x01, sigma1, a2, x02, sigma2):
        '''Сумма двух колоколов'''
        return a1 * np.exp(-((x-x01)/sigma1)**2) +\
               a2 * np.exp(-((x-x02)/sigma2)**2) 


    test_approximation(gaussian2, p=(1, 3, 2, 1.2, 8, 1), fn='06_12a.png')
    return (gaussian2,)


@app.cell
def _(gaussian2, test_approximation):
    test_approximation(gaussian2, p=(1, 3, 2, 1.2, 8, 1), 
                                  p0=(1.2, 2.5, 1, 1.1, 7,1), fn='06_12b.png')
    return


@app.cell
def _(gaussian2, test_approximation):

    test_approximation(gaussian2, p=(1, 5, 2, 1.2, 7, 1), 
                       p0=(1, 5, 1, 0.8, 8, 1), fn='06_13a.png')
    return


@app.cell
def _(gaussian2, test_approximation):

    test_approximation(gaussian2, p=(1, 5, 2, 1.2, 7, 1), 
                       p0=(1, 5, 1, 0.8, 8, 1), s=.1, fn='06_13b.png')
    return


@app.cell
def _(gaussian2, np, test_approximation):
    _p = np.array([1, 5, 2, 1.2, 7, 1])
    _c, _error, _fig, = test_approximation(gaussian2, p=_p, 
                        p0=(1, 5, 1, 0.8, 8, 1), s=.3, fn='06_13b.png')
    err_p = np.max(np.abs(_p - _c)/_p)
    _fig, err_p
    return


if __name__ == "__main__":
    app.run()
