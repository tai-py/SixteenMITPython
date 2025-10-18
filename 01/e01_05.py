import marimo

__generated_with = "0.13.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import sympy as smp
    return mo, np, plt, smp


@app.cell
def _(mo):
    mo.md(r"""# Овал Толстого и лемниската Бернулли""")
    return


@app.cell
def _(smp):
    # инициализируем "красивый" вывод формул
    smp.init_printing()

    # объявляем символьные переменные
    x, y, a, c = smp.symbols('x, y, a, c')

    def cassini(x, y, a, c):
        ''' Овал Кассини'''
        f = smp.sqrt(smp.sqrt((x-c)**2 + y**2)*\
                       smp.sqrt((x+c)**2 + y**2)) - a
        eq = smp.Eq(f, 0)
        return  smp.solve(eq, y)
    cassini(x, y, a, c)
    return cassini, x, y


@app.cell
def _(cassini, smp, x, y):
    lemniscata = cassini(x, y, 1, 1) 
    tolstoi = cassini(x, y, smp.sqrt(2), 1)
    return lemniscata, tolstoi


@app.cell
def _(lemniscata):
    lemniscata
    return


@app.cell
def _(tolstoi):
    tolstoi
    return


@app.cell
def _(lemniscata, smp, x):
    def curvature(curve):
        l = len(curve)
        result = []
        for c in curve:
            ys = c.diff(x,1)
            ys2 = c.diff(x, 2)  
            result.append(smp.Abs(ys2)/smp.sqrt(1 + ys**2)**3)
        return result

    lemniscata_curvature = curvature(lemniscata)
    lemniscata_curvature
    return curvature, lemniscata_curvature


@app.cell
def _(smp, tolstoi, tolstoi_curvature, x):
    def curve_plot(curve=tolstoi, 
                   curvature=tolstoi_curvature,
                   fn=''):
        p1 =smp.plot(curve[2], (x, -5, 5), line_color='b',    
                 show=False,aspect_ratio=(1,1))
        p2 =smp.plot(curve[3], (x, -5, 5), line_color='b', 
                 show=False,aspect_ratio=(1,1))
        p3 = smp.plot(curvature[2], (x, -1.5, 1.5), line_color='r', 
                  show=False,aspect_ratio=(1,1))
        p1.extend(p2)
        p1.extend(p3)   
        p1.show()

    curve_plot()

    return (curve_plot,)


@app.cell
def _(curve_plot, lemniscata, lemniscata_curvature):
    curve_plot(curve=lemniscata, 
              curvature=lemniscata_curvature)
    return


@app.cell
def _(curvature, tolstoi):
    tolstoi_curvature = curvature(tolstoi)
    tolstoi_curvature
    return (tolstoi_curvature,)


@app.cell
def _(np, plt):
    xmax, n  = 3, 10000
    xx = np.linspace(-xmax, xmax, n, dtype=complex)
    y2 = np.sqrt(4*xx**2 +1)

    yy = np.sqrt(np.sqrt(4*xx**2+1) -1 -xx**2)
    _fig = plt.figure(figsize=(5, 4))
    yy = np.where(np.abs(yy.imag)>1e-2, np.nan, yy)
    plt.plot(xx, yy.real, 'b-')
    plt.plot(xx, -yy.real, 'b-')
    plt.axis('equal')
    _fig
    return


@app.cell
def _(np):
    def tolstoi_numpy(x, h=1):
        '''
        Четвертушка овала Толстого
        Параметры:
        x - значение горизонтальной координаты
        h - полуширина овала
        Функция возвращает вертикальную координату овала
        '''    
        return h*np.sqrt(-x**2 + 2*np.sqrt(x**2+1) - 1)

    return (tolstoi_numpy,)


@app.cell
def _(np, tolstoi_numpy, y):
    def stadium(x, l=1, h=1):
        '''
        Верхняя половина стадиума, составленного из
        прямолинейных участков длиной 2*l и
        полуовалов Кассини высотой 2*h.
        Параметры
        x - горизонтальная координата,
        l - длина половины прямолинейного участка,
        h - полувысота стадиума.
        Функция возвращает вертикальную координату стадиума. 
        '''
        xx = np.abs(x)    
        return  np.where(np.abs(xx)<l, h, tolstoi_numpy(xx-l, h=h))
        return y 
    return (stadium,)


@app.cell
def _(np, plt, stadium):
    def draw_stadium(l=1, h=1, lw=1, color='b', n=10000, xmax=5):
        '''
        Рисуем стадиум
        l, h - полудлина и полуширина стадиума,
        lw - толщина линии,
        color - цвет линии,
        n - число разбиений стадиума на участки для рисования,
        xmax - отрезок, на котором осуществляется рисование
        '''
        x = np.linspace(-xmax, xmax, n)
        y = stadium(x, l=l, h=h)
        plt.plot(x, y,ls='-', lw=lw, color=color,
                label=f"{l=}, {h=}")
        plt.plot(x, -y,ls='-', lw=lw, color=color)

    _fig = plt.figure(figsize=(4,3))
    draw_stadium(lw=3) 
    draw_stadium(l=0.,lw=3, color='red') 
    draw_stadium(l=0., h=0.5, lw=3, color='lime') 
    plt.legend()
    plt.savefig('01.17.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(np):
    from decimal import Decimal, getcontext
    getcontext().prec = 1000
    _z = np.zeros(5, dtype=Decimal)
    _z +1
    return


@app.cell
def _(np):
    import mpmath as mp
    from mpmath import iv
    _z = np.zeros(7, dtype=object)
    _z[0] = iv.mpf([2,3])
    _z -= iv.mpf([-1,1])
    _z
    return


@app.cell
def _(np):
    class Ivl(np.ndarray):
        ...
        def __init__(self): 
            super().__init__(self)
        
    Ivl()
    return


@app.cell
def _(np):
    class C(np.ndarray):
        def __new__(cls, *args, **kwargs):
            print('In __new__ with class %s' % cls)
            return super().__new__(cls, *args, **kwargs)

        def __init__(self, *args, **kwargs):
            # in practice you probably will not need or want an __init__
            # method for your subclass
            print('In __init__ with class %s' % self.__class__)

        def __array_finalize__(self, obj):
            print('In array_finalize:')
            print('   self type is %s' % type(self))
            print('   obj type is %s' % type(obj))

    C((10,), dtype=object)

    return


if __name__ == "__main__":
    app.run()
