import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    mo.md('# Метод секущих')
    return mo, np, plt


@app.cell
def _():
    cube = lambda x : x**3 - 1
    square = lambda x : x**2 - 1 
    return (square,)


@app.cell
def _(square):
    def secant(f, x0, x1, args=(), max_iter=500, tol=1e-10):
        # значения функции и производной для начального приближения
        f0, f1 = f(x0, *args), f(x1, *args)
        # инициализируем историю
        history = [(0, x0, x1,f0, f1)]     
        # Проверяем, лежит ли 0 на отрезке [x0, x1]
        if f0*f1>0:
            raise ValueError('Функция secant. Некорректный выбор начального приближения')

        success = False # признак успешного завершения  
        for iter in range(1, max_iter):
             # невозможность продолжения процесса
            if abs(f1 - f0) < tol:
                raise ValueError(f"Функция secant. Приращение функции на шаге {iter} меньше {tol:6.3e}")       
            x2 = x1 - f1*(x1 - x0)/(f1 - f0) 
            # новые значения функции и производной
            f2 = f(x2, *args)

            # дополняем историю
            history.append((iter, x1, x2, f1, f2))
            # проверка условий успещного заверщения процесса
            if abs(x2 - x1) <= tol or max(abs(f1), abs(f2))<tol:
                success = True
                return x2, iter, f2, success, history
            # подготавливаем следующую итерацию  
            x0, x1, f0, f1 = x1, x2, f1, f2             

        return x2, iter, f2, success, history

    secant(square, 0, 3)

    return (secant,)


@app.cell
def _(mo):
    mo.md(r"""## Визуализируем метод секущих""")
    return


@app.cell
def _(np, plt, secant, square):
    def visualize_secant_method(ax, f, x0, x1, args=(), iters=(0,2),
                               lw=3, ms=5, padx=0.05, pady=.1, 
                                tol=1e-2, nums=True):
        # ищем корень
        x2, maxiter, f2, success, history = secant(f, x0, x1, args=args, tol=tol)    
        print(f"Корень: {x2=}, {f2=}, {maxiter=}")
        m = iters[1] - iters[0] # число отображаемых итераций

        it, xx1, xx2, ff1, ff2 = [], [], [], [], []
        for _ in range(iters[0], iters[1]+1):
            it.append(history[_][0])
            xx1.append(history[_][1])
            xx2.append(history[_][2])
            ff1.append(history[_][3])
            ff2.append(history[_][4]) 
        print(f"{it=}, {xx1=}, {ff1=}, {xx2}, {ff2}")
        # график функции функции и нулевой уровень
        x0, x1 = xx1[0], xx2[0]
        ax.plot([x0, x1], [0, 0], 'k--') # нулевой уровень
        n =500
        x = np.linspace(x0, x1, n)
        y = f(x, *args)
        ax.plot(x, y, 'b-', lw=lw) 
        ax.plot(x2, f2, 'r+', ms=10)
        # процесс поиска корня
        for _ in range(m): #range(iters[0], iters[1]+1):
            ax.plot(xx1[_], ff1[_], 'ro', ms=ms)
            if nums:
                ax.text(xx1[_] - padx, ff1[_] + pady, str(_ + iters[0])) 
                ax.text(xx2[_] + padx, ff2[_] - 2*pady, str(_ + iters[0]), color='b') 
            ax.plot([xx1[_], xx2[_]], [ff1[_], ff2[_]], 'k:')
            xz = xx1[_] - ff1[_]*(xx2[_] - xx1[_])/(ff2[_] - ff1[_]) 
            ax.plot(xz, 0, 'b+', ms=10)
            fz = f(xz, *args) 
            ax.plot([xz, xz], [0, fz], 'k:')
            if nums:
                ax.text(xz - padx, pady, str(_ + iters[0]), color='red')
            
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')

    _fig, _ax = plt.subplots()
    visualize_secant_method(_ax, square, 0, 2, iters=(0, 5))
    plt.savefig('newton_08.png', dpi=300, facecolor='white')
    _fig
    return (visualize_secant_method,)


@app.cell
def _(plt, square, visualize_secant_method):
    _fig, _ax = plt.subplots()
    visualize_secant_method(_ax, square, 0, 2, iters=(3, 5), padx=0.007, pady=0.01)
    _fig
    return


@app.cell
def _(secant):
    # Пробная функция
    f = lambda x: x**3 - 5*x**2 - 4.5
    x2, iter, f2, success, history = secant(f, -2, 5.5, tol=1e-10)
    print(f"{x2=}, {iter=}, {f2=}, {success=}")

    return (f,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Зависимость числа итераций от насального приближения""")
    return


@app.cell
def _(f, np, plt, secant):
    _xlim = -20, 20
    _n = 4000
    _x = np.linspace(_xlim[0], _xlim[1], _n)
    _miniters, _maxiters = 10000, -1
    _fig = plt.figure(figsize=(12, 4))
    for _ in range(1, _n):
        try:
            _r = secant(f,  _x[_], -2, max_iter=1000)       
            if _r[3]: # успешное завершение
                _iters = _r[1]
                _miniters, _maxiters = min(_miniters, _iters), max(_maxiters, _iters)
                plt.plot(_x[_], _iters, 'bo', ms=2)
        except ValueError:
            ...
    plt.yscale('log')
    plt.grid()
    plt.xlabel(f'Начальное приближение $x_0,(x_1=-2)$')
    plt.ylabel('Число итераций')
    print(f"{_miniters=}, {_maxiters=}")
    plt.savefig("newton_09.png", dpi=300, facecolor="white")
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Аналитическое решение для уравнения пробной функции""")
    return


@app.cell
def _():
    import sympy as smp

    x = smp.symbols('x')
    fa = x**3 - 5*x**2 - 4.5
    smp.solve(fa, x)

    return


if __name__ == "__main__":
    app.run()
