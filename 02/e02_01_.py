import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    mo.md('# Геометрическая интерпрeтация метода Ньютона на примере $f(x)=x^3-5x^2 -4.5$')
    return np, plt


@app.function
def newton_(f, fs, x0, args=(), eps=1e-10):
    '''
    Реализация метода Ньютона для функций одной переменной
    f - функция вида f(x, *args)
    fs - производная функции f(x) по x: fs(x, *args)
    args - дополнительные переменные, передаваемые функциям f, fs
    x0 -  начальное приближение
    eps - число, используемое для остановки итерационного процесса

    Функция возвращает:
    x1 - значение корня функции 
    f1 - значение функции f(x1, *args)
    history - последовательность приближенных значений корня, функции и производной
              на каждой итерации 
    '''
    f0, fs0 = f(x0, *args), fs(x0, *args)
    history = [(0, x0, f0, fs0)]
    nmax = 100
    for iter in range(1, nmax+1):
        if abs(fs0<eps):
            raise ValueError(f"Метод Ньютона. Абсолютное значения производной меньше {eps:6.3e}")
        dx = -f0/fs0 # приражение x
        x1 = x0 + dx # новое значение x
        f1, fs1 = f(x1, *args), fs(x1, *args)
        history.append((iter, x1,  f1, fs1))   
        #print(f"{iter=}, {dx=} {x1=}, {f1=}, {fs1=}")
        if abs(f1)<eps or abs(x1 - x0)<eps:
            return x1, f1, iter, history
        x0, f0 = x1, f1 # подготавливаем следующую итерацию             
        
    else:
        raise ValueError(f"Процесс уточнения корня методом Ньютона не сошелся на {nmax} итерациях")


@app.cell
def _(np):
    def newton(f, fs, x0, args=(), eps=1e-10, itmax=200):
        '''
        Реализация метода Ньютона для функций одной переменной
        f - функция вида f(x, *args)
        fs - производная функции f(x) по x: fs(x, *args)
        args - дополнительные переменные, передаваемые функциям f, fs
        x0 -  начальное приближение
        eps - число, используемое для остановки итерационного процесса
        itmax - максимальное число итераций

        Функция возвращает:
        x1 - значение корня функции 
        f1 - значение функции на конечной итерации
        iter - число итераций
        success - признак успешности завершения процесса
        history - последовательность приближенных значений корня, функции и производной
                  на каждой итерации 
        '''    
        f0, fs0 = f(x0, *args), fs(x0, *args) # начальные значени функции и призводной
        # история процесса
        history = [(0, x0, f0, fs0)]
        for iter in range(1, itmax+1):
            # проверяем значение производной
            if abs(fs0)<eps:
                raise ValueError(f"Метод Ньютона. Нулевое значение производной на итерации {iter}")
            dx = - f0/fs0
            x1 = x0 + dx # новое значение корня
            # значения функции и производной на следующей итерации
            f1, fs1 = f(x1, *args), fs(x1, *args)
            history.append((iter, x1, f1, fs1)) # сохраняем историю
            # проверяем условие завершения процесса
            if abs(f1)<eps or abs(dx)<eps:
                return x1, f1, iter, True, history
            x0, f0 = x1, f1 # подготавливаем следующую итерацию
        else:
            # процесс завершается неудачно
            return x1, f1, iter, False, history

    def history2array(result, n=-1):
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
        history = np.array(result[4])
        ir, xr, fr, fsr = history if n<0 else history[:, :n]
        return ir, xr, fr, fsr

    
    return (newton,)


@app.cell
def _():
    # пробная функция и ее производная
    f = lambda x: x**3 #lambda x: x**3 - 5*x**2 - 4.5
    fs = lambda x: 3*x**2 #x: 15*x**2 - 10*x
    return f, fs


@app.cell
def _(f, fs, newton):
    _r = newton(f, fs, x0=-2)
    _x, _f, _iter, _success, _history = _r 
    print(f"{_x=}, {_f=}, {_iter=}, {_success=}, {_history[:5]=}")
    f(5.168457595892028)
    return


@app.cell
def _(f):
    f2 = lambda x:x**2
    def newt(f2, x=-2, h=1e-04):
        fs = (f(x+h) - f(x - h))/(2*h)
        return x - f(x)/fs

    newt(-2)
    return f2, newt


@app.cell
def _(f2, newt):
    newt(f2, -1.3333333)
    return


@app.cell
def _(newt):
    newt(-0.888888888888889)
    return


@app.cell
def _(newt):
    newt(-0.5925925925925926)
    return


@app.cell
def _(newt):
    newt(-0.3950617283950617)

    return


@app.cell
def _(f, fs, newton):
    newton(f, fs, x0=5.16845, eps=1e-7)
    return


@app.cell
def _():
    # def history2array(result, n=-1):
    #     '''
    #     Преобразую историю итераций 
    #     метода Ньютона в массив NumPy
    #     для визуализации
    #     '''
    #     if result:
    #         a = np.array(result[3]) # извлекаю history
    #         if n>0:
    #             a = a.T
    #             print(f"{a.shape=}")
    #             ir, xr, fr, fsr = a[:, :n]
    #         else:
    #             ir, xr, fr, fsr = a.T
    #         #ir, xr, fr, fsr = a.T
    #         return ir, xr, fr, fsr

    # _result = newton(f, fs, -2)
    # history2array(_result, n=3)
    return


@app.cell
def _(axs, f, fig, fr, fs, fsr, ir, newton, np, plt, x, xr, y):
    def visualize_newton(f, fs, x0, #iters=(0,3,5,7, 15, 18, 20, 31), 
                         iters=(0,1,2,3, 4, 5, 6, 7), 
                         figsize=(12, 9), xlim=[-2.5,6]):
        result = newton(f, fs, x0)
        if result: 
            iend = result[2]

     
            for row in range(3):
                for col in range(3):
                    i = 3*row + col
                    if i<=7:
                        ax = axs[row, col]
                        ax.plot(x, y)
                        it = iters[i]
                        ax.set_title(f"Итeрация: {it}")
                        ax.plot(xr[it], fr[it], 'ro', ms=7)
                        ax.plot([xr[it], xr[it]], [0, fr[it]], 'k--')
                        ax.plot(xr[it], 0, 'ro', ms=7)
                        if it < iend:
                            ax.plot(xr[it+1], 0, 'bs', ms=5)
                            ax.plot([xr[it+1], xr[it+1]], [0, fr[it+1]],'b--')
                            ax.plot(xr[it+1], fr[it+1], 'bs', ms=5)
                        ax.plot([xlim[0], xlim[1]], [0, 0], 'k--', lw=0.5)
                        ax.set_xlim(*xlim)
                        ylim = y[0], y[-1]
                        ax.set_ylim(*ylim)
                        ax.set_xlabel('x')
                        ax.set_ylabel('f(x)')          
                    
                        # строим касательную
                        x1, x2 = xlim
                        x0, y0 = xr[it], fr[it]
                        y1, y2 = y0 + fsr[it]*(x1 - x0),  y0 + fsr[it]*(x2 - x0)
                        ax.plot([x1,x2], [y1,y2])
         
                        
                        
                    
        
            # зависимость погрешностей от номера итерации
            ax = axs[-1,-1]
            ax.plot(ir, np.abs(fr), lw=3, label="$|f(x_i)|$")
            dx = np.abs(xr[1:] - xr[:-1])
            ax.plot(ir[1:], dx, lw=3, label="$|x_{i}-x_{i-1}|$")
            ax.set_yscale('log')
            ax.set_xlabel('номер итерации')
            ax.set_ylabel('погрешности')
            ax.grid()
            ax.legend()
            ax.set_title("Погрешности от номера итерации")
        
            plt.tight_layout()
            return fig

    visualize_newton(f, fs, -2)
    return


@app.cell
def _(f, fs, newton):
    print(newton(f, fs, 5.3))
    return


app._unparsable_cell(
    r"""
    def visualize_newton2(f, fs, x0=-2, n=6,
                         figsize=(8, 6), xlim=[-2.5,6], ms=3):
        result = newton(f, fs, x0)
        if result:         
            x = np.linspace(xlim[0], xlim[1], 1000)
            y = f(x)
            ylim = np.min(y), np.max(y)
            ir, xr, fr, fsr = history2array(result, n)        
            fig, ax = plt.subplots(figsize=figsize)
            ax.plot(x, y)
            ax.plot([xlim[0], xlim[1]], [0, 0], 'k--', lw=0.5)
            iters = len(ir)
            for i in range(iters):
                ax.plot(xr[i], fr[i], 'ro', ms=ms)
                ax.plot(xr[i], 0, 'ro', ms=ms)
                ax.plot([xr[i], xr[i]], [0, fr[i]], 'r--', lw=0.5)
            for i in range(0, iters, 1):
                # касательные
                x1, x2 = 
                y1 = fr[i]  + fsr[i]*(x1 - xr[i])
                y2 = fr[i]  + fsr[i]*(x2 - xr[i])
                ax.plot([x1, x2], [y1, y2], 'k--', lw=0.5)

            ax.set_xlim(*xlim)
            ax.set_ylim(*ylim)
            return fig

    visualize_newton2(f, fs, -2)
    """,
    name="_"
)


@app.cell
def _():
    def newtons_method(f, df, x0, e):
        delta = df(x0)
        i = 0
        while delta > e:
            x0 = x0 - f(x0)/df(x0)
            delta = df(x0)
            i+=1
        print('Root is at: ', x0)
        print('iter:', i)
        print('f(x) at root is: ', f(x0))

    f3 = lambda x: x**2
    f3s = lambda x: 2*x
    newtons_method(f3, f3s, 15, 1e-5)
    return


if __name__ == "__main__":
    app.run()
