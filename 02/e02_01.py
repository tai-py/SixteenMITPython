import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    mo.md('# Геометрическая интерпрeтация метода Ньютона')
    return mo, np, plt


@app.cell
def _():
    # Пробная функция
    f = lambda x: x**3 - 5*x**2 - 4.5
    # Производная пробной функции
    fs = lambda x: 3*x**2 - 10*x 
    return f, fs


@app.cell
def _(f, fs, np, plt):
    # График пробной функции и ее производной
    xlims = -2.5, 5.5
    x = np.linspace(xlims[0], xlims[1], 1000)
    fx, fsx = f(x), fs(x)

    _fig, _ax = plt.subplots(figsize=(8,5))
    legend1 = _ax.plot(x, fx, 'b-', lw=3, label="$f(x)$")
    _ax.plot([xlims[0], xlims[1]], [0,0], 'b--')
    _ax.set_xlabel('x')
    _ax.set_ylabel('f(x)')
    _ax.set_xlim(*xlims)
    # plt.title("Пробная функция и ее производная")

    # график производной
    _ax2 = _ax.twinx()
    _ax2.plot([xlims[0], xlims[1]], [0,0], 'r--')
    legend2 = _ax2.plot(x, fsx, 'r-', lw=3, label=r"$\frac{df(x)}{dx}$") 
    _ax2.set_ylabel(r"$\frac{df(x)}{dx}$")

    # легенда
    lines1, labels1 = _ax.get_legend_handles_labels()
    lines2, labels2 = _ax2.get_legend_handles_labels()
    lines = lines1 + lines2
    labels = labels1 + labels2
    _ax.legend(lines, labels)
    plt.tight_layout()
    #plt.savefig('02_02.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(f, fs):
    def newton(f, fs, x0, args=(), max_iter=200, tol=1e-10):
        '''
        Реализация метода Ньютона для функций одной переменной
        f - функция вида f(x, *args)
        fs - производная функции f(x) по x: fs(x, *args)    
        x0 -  начальное приближение
        args - дополнительные переменные, передаваемые функциям f, fs
        max_iter - максимальное число итерацийЮ после которого процесс останавливается
        tol - число, используемое для остановки итерационного процесса

        Функция возвращает:
        x1 - значение корня функции 
        iter - число итераций
        f1 - значение функции f(x1, *args)
        success - признак успешного завершения процесса
        history - последовательность приближенных значений корня, функции и производной
                  на каждой итерации 
        '''    
        # значения функции и производной для начального приближения
        f0, df = f(x0, *args), fs(x0, *args)
        # инициализируем историю
        history = [(0, x0, f0, df)] 
        success = False # признак успешного завершения  
        for iter in range(1, max_iter):
             # невозможность продолжения процесса
            if abs(df)<tol:
                raise ValueError(f"Метод Ньютона. Абсолютное значения производной меньше {tol:6.3e}")       
            x1 = x0 - f0/df
            # новые значения функции и производной
            f1, df1 = f(x1, *args),  fs(x1, *args)
            # дополняем историю
            history.append((iter, x1, f1, df1))
            # проверка условий успещного заверщения процесса
            if abs(x1 - x0) <= tol or abs(f1)<tol:
                success = True
                return x1, iter, f(x1, *args), success, history
            x0, f0, df = x1, f1, df1 # подготавливаем следующую итерацию   

        return x1, iter, f(x1, *args), success, history

    _r = newton(f, fs, -2.0)
    print(f"x={_r[0]}, f(x)={_r[2]}, iter={_r[1]}, success={_r[3]}")
    return (newton,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Смотрим, как число итераций зависит от начального приближения
    """)
    return


@app.cell
def _(f, fs, newton):
    _r = newton(f, fs, 5.0)
    print(f"x={_r[0]}, f(x)={_r[2]}, iter={_r[1]}, success={_r[3]}")
    return


@app.cell
def _(f, fs, newton):
    _r = newton(f, fs, 5.16)
    print(f"x={_r[0]}, f(x)={_r[2]}, iter={_r[1]}, success={_r[3]}")
    return


@app.cell
def _(f, fs, newton):
    _r = newton(f, fs, 5.0)
    print(f"x={_r[0]}, f(x)={_r[2]}, iter={_r[1]}, success={_r[3]}")
    return


@app.cell
def _(f, fs, newton):
    _r = newton(f, fs, 5.0, tol=1e-6)
    print(f"x={_r[0]}, f(x)={_r[2]}, iter={_r[1]}, success={_r[3]}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Для визуализации процесса вычисления корня функции методом Ньютона на понадобится преобразовать историю процесса в массивы NumPy
    """)
    return


@app.cell
def _(f, fs, newton, np):
    def history2array(result):
        '''
        Распаковка истории метода Ньютона 
        result - результат, возвращаемый функцией newton
        n - число возвращаемых элементов истории
        Функция возвращает:
        ir - массив номеров итераций
        xr - массив  приближенных значений корня функции 
        fr - массив значений фунции f(x) на массиве xr 
        fsr - массив производных функции    
        '''
        # извлекаю историю, преобразую ее в массив
        history = np.array(result[4]).T

        ir, xr, fr, fsr = history 
        return ir, xr, fr, fsr

    history2array(newton(f, fs, -2))
    return (history2array,)


@app.cell
def _(f, fs, history2array, newton, np, plt):
    ir, xr, fr, fsr = history2array(newton(f, fs, -2))
    _fig, _ax = plt.subplots(figsize=(6,4))
    _ax.plot(ir, np.abs(fr), lw=3, label="$|f(x_i)$|")
    _ax.plot(ir[:-1], np.abs(xr[1:] - xr[:-1]), lw=3, label="$|x_{i+1} - x_i|$")
    plt.yscale('log')
    plt.xlabel('итерация')
    plt.ylabel('погрешности')
    plt.ylim(1e-10, 1e3)
    plt.grid()
    plt.legend()
    #plt.savefig('02_03.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Визуализация процесса вычисления корней функции методом Ньютона
    """)
    return


@app.cell
def _(f, fs, history2array, newton, np, plt):
    def visualize_newton(f, fs, x0, xlim=(-2.5, 5.5), ylim=(-50, 10),
                          inds=[0,1,2,3,4,5], figsize=(6, 4), ms=5, 
                          padx=0.2, pady=2, fn=''):
        x = np.linspace(xlim[0], xlim[1], 1000)
        fx, fsx = f(x), fs(x)    
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(x, fx, 'b-', lw=3, label="$f(x)$")
        ir0, xr0, fr0, fsr0 = history2array(newton(f, fs, x0))
        ir, xr, fr = ir0[inds], xr0[inds], fr0[inds]

        m = len(ir)
        #print(f"{xr.shape=}, {fr.shape=}, {m=} ")
        ax.plot(xr, fr, 'ro', ms=5)
        ax.plot(xr, [0]*m,  'bo', ms=5)
        for i in range(m):
            ax.plot([xr[i], xr[i]], [fr[i], 0.], 'k:', lw=1)
        # касательные
        for i in range(m-1):
            ax.plot([xr[i], xr[i+1]], [fr[i], 0], 'k:')
        plt.text(xr[-1]-padx, pady, f"{int(ir[-1])}")
        for i in range(m-2):
            plt.text(xr[i]-padx, pady, f"{int(ir[i])}") 
            plt.text(xr[i]-padx, fr[i]-pady, f"{int(ir[i])}")

        ax.plot([xlim[0], xlim[1]], [0,0], 'k--')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)') 
        plt.xlim(*xlim)   
        plt.ylim(*ylim)

        ax.grid()
        ax.legend()
        if fn:
            plt.savefig(fn, dpi=300, facecolor="white")

        return fig        

    visualize_newton(f, fs, -2, xlim=(-2.5, 3), ylim=(-40, 10), inds=[0,1,2,3],
                     fn="newton_04a.png")
    return (visualize_newton,)


@app.cell
def _(f, fs, visualize_newton):
    visualize_newton(f, fs, -2, inds=[12,13,14, 15], xlim=(5.1, 5.5), ylim=(-5, 11), padx=0.01, pady=0.5,
                     fn="newton_04b.png")
    return


@app.cell
def _(f, fs, newton, np, plt):
    _xlim = -20, 20
    _n = 2000
    _x = np.linspace(_xlim[0], _xlim[1], _n)
    _miniters, _maxiters = 10000, -1
    _fig = plt.figure(figsize=(12, 4))
    for _ in range(_n):
        try:
            _r = newton(f, fs, _x[_])
            if _r[3]: # успешное завершение
                _iters = _r[1]
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
    ## Метод Ньютона с численным вычислением производной функции
    """)
    return


@app.cell
def _(f):
    def newton2(f, x0, args=(), max_iter=200, tol=1e-10, h=1e-4):
        '''
        Реализация метода Ньютона для функций одной переменной,
        производная вычисляется чисиленно
        f - функция вида f(x, *args)
        fs - производная функции f(x) по x: fs(x, *args)    
        x0 -  начальное приближение
        args - дополнительные переменные, передаваемые функциям f, fs
        max_iter - максимальное число итерацийЮ после которого процесс останавливается
        tol - число, используемое для остановки итерационного процесса
        h - шаг для вычисления проищводной

        Функция возвращает:
        x1 - значение корня функции 
        iter - число итераций
        f1 - значение функции f(x1, *args)
        success - признак успешного завершения процесса
        history - последовательность приближенных значений корня, функции и производной
                  на каждой итерации 
        '''   
        def fs(x, *args, h=h):
            '''Вычисление производной'''
            return (f(x+h, *args) - f(x-h, *args))/(2*h)

        # значения функции и производной для начального приближения
        f0, df = f(x0, *args), fs(x0, *args)
        # инициализируем историю
        history = [(0, x0, f0, df)] 
        success = False # признак успешного завершения  
        for iter in range(1, max_iter):
             # невозможность продолжения процесса
            if abs(df)<tol:
                raise ValueError(f"Метод Ньютона. Абсолютное значения производной меньше {tol:6.3e}")       
            x1 = x0 - f0/df
            # новые значения функции и производной
            f1, df1 = f(x1, *args),  fs(x1, *args)
            # дополняем историю
            history.append((iter, x1, f1, df1))
            # проверка условий успещного заверщения процесса
            if abs(x1 - x0) <= tol or abs(f1)<tol:
                success = True
                return x1, iter, f(x1, *args), success, history
            x0, f0, df = x1, f1, df1 # подготавливаем следующую итерацию   

        return x1, iter, f(x1, *args), success, history

    _r = newton2(f, -2.0)
    print(f"x={_r[0]}, f(x)={_r[2]}, iter={_r[1]}, success={_r[3]}")
    return (newton2,)


@app.cell
def _(f, np):
    def fn(x, delta=1e-3):
        size = x.shape[0] if isinstance(x, np.ndarray) else 1
        #return f(x)*(1 + np.random.normal(0,delta, size=size))
        return f(x)+ np.random.normal(0,delta, size=size)

    return (fn,)


@app.cell
def _(f, fn, np, plt):
    _n, _delta, _xlim = 500, 1, (-2.5, 5.5)
    _x = np.linspace(*_xlim, _n)
    _fig = plt.figure(figsize=(6,4))
    _y, _yn = f(_x), fn(_x, _delta)
    plt.plot(_x, _y, 'b-', lw=2)
    plt.plot(_x, _yn, 'r-', lw=1)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig('newton_06.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(fn, newton2):
    _r = newton2(fn, -2.0, tol=1e-6, args=(0, ), h=1e-4)
    print(f"x={_r[0]}, f(x)={_r[2]}, iter={_r[1]}, success={_r[3]}")
    return


@app.cell
def _(fn, newton2):
    _r = newton2(fn, -2.0, tol=1e-6, args=(1e-7, ), h=1e-4)
    print(f"x={_r[0]}, f(x)={_r[2]}, iter={_r[1]}, success={_r[3]}")
    return


@app.cell
def _(fn, newton2):
    _r = newton2(fn, -2.0, tol=1e-6, args=(1e-6, ), h=1e-4)
    print(f"x={_r[0]}, f(x)={_r[2]}, iter={_r[1]}, success={_r[3]}")
    return


@app.cell
def _(fn, newton2):
    _r = newton2(fn, -2.0, tol=1e-6, args=(1e-5, ), h=1e-4)
    print(f"x={_r[0]}, f(x)={_r[2]}, iter={_r[1]}, success={_r[3]}")
    return


@app.cell
def _(fn, newton2):
    _r = newton2(fn, -2.0, tol=1e-6, args=(1e-4,), h=1e-4)
    print(f"x={_r[0]}, f(x)={_r[2]}, iter={_r[1]}, success={_r[3]}")
    return


@app.cell
def _(fn, newton2):
    _r = newton2(fn, -2.0, tol=1e-6, args=(5e-4,), h=1e-4)
    print(f"x={_r[0]}, f(x)={_r[2]}, iter={_r[1]}, success={_r[3]}")
    return


@app.cell
def _(fn, newton2):
    _r = newton2(fn, -2.0, tol=1e-6, args=(1e-3,), h=1e-4)
    print(f"x={_r[0]}, f(x)={_r[2]}, iter={_r[1]}, success={_r[3]}")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Статистическое моделирование поиска корня защумленной функции
    """)
    return


@app.cell
def _(fn, newton2, np, plt):
    _n = 1000
    _iters = np.zeros(_n)
    for _ in range(_n):
        _iters[_] = newton2(fn, -2.0, tol=1e-6, args=(1e-3,), h=1e-4, max_iter=500)[1]

    _fig = plt.figure()
    plt.hist(_iters, bins=50, density=True)
    plt.xlabel("Число итераций")
    plt.ylabel("Частота")
    plt.savefig('newton_07a.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(fn, newton2, np, plt):
    _n = 1000
    _iters = np.zeros(_n)
    for _ in range(_n):
        _iters[_] = newton2(fn, -2.0, tol=1e-6, args=(2.5e-3,), h=1e-4, max_iter=500)[1]

    _fig = plt.figure()
    plt.hist(_iters, bins=50, density=True)
    plt.xlabel("Число итераций")
    plt.ylabel("Частота")
    plt.savefig('newton_07b.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(fn, newton2, np, plt):
    _n = 1000
    _iters = np.zeros(_n)
    for _ in range(_n):
        _iters[_] = newton2(fn, -2.0, tol=1e-6, args=(2.5e-3,), h=1e-4, max_iter=500)[1]

    _fig = plt.figure()
    plt.hist(_iters, bins=50, density=True, cumulative=True)
    plt.xlabel("Число итераций")
    plt.ylabel("Частота")
    #plt.savefig('newton_07c.png', dpi=300, facecolor="white")
    _fig
    return


if __name__ == "__main__":
    app.run()
