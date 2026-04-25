import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    from scipy.interpolate import UnivariateSpline as  UVS
    from scipy.interpolate import RectBivariateSpline as RBS
    import matplotlib.pyplot as plt

    mo.md("# Сплайновая интерполяция и экстраполяция")
    return RBS, UVS, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Одномерная  интерполяция
    """)
    return


@app.cell
def _(UVS, np, plt):
    # Исходные данные
    x = np.array([1.0, 2.0, 3.0, 4.5, 5.0, 6.1,  7.0,  8.0,  8.9, 10.0, 11.0, 12.0])
    y = np.array([4.0, 5.0, 7.0, 9.0, 6.0, 7.0, 11.0, 24.0, 34.0, 40.0, 37.0, 47.0])

    # точки, где будет проводиться интерполяция
    _n = 1000
    _x = np.linspace(1, 12, _n)

    _fig = plt.figure(figsize=(6, 4))
    plt.plot(x, y, 'ko', ms=5, label="исходные данные")

    for _k in (1, 3, 5): # _k - степень сплайна
        _spl = UVS(x, y, k=_k, s=0) # интерполяция
        _y = _spl(_x)
        plt.plot(_x, _y, label=f"k={_k}", lw=1)
    plt.xlabel('x')
    plt.ylabel('y(x)')
    plt.legend()
    plt.savefig("06_23a.png", dpi=300, facecolor='white')
    _fig             
    return x, y


@app.cell
def _(UVS, np, plt, x, y):
    # точки где будет проводиться экстраполяция
    _n = 1000
    _x = np.linspace(-2, 13, _n)

    _fig = plt.figure(figsize=(6, 4))
    plt.plot(x, y, 'ko', ms=5, label="исходные данные")

    for _k in (1,3): # k - степень сплайна
        _spl = UVS(x, y, k=_k, s=0) 
        _y = _spl(_x)
        plt.plot(_x, _y, label=f"k={_k}")
    plt.xlabel('x')
    plt.ylabel('y(x)')
    #plt.ylim(0, 50)
    plt.legend()
    plt.savefig("06_23b.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(UVS, np, plt, x, y):
    # аппроксимация и сглаживание
    _n = 1000
    _x = np.linspace(1, 12, _n)

    _fig = plt.figure(figsize=(6, 4))
    plt.plot(x, y, 'ko', ms=5, label="исходные данные")

    for _k in (1,): # k - степень сплайна
        for _s in (0, None, 100, 1000):        
            _spl = UVS(x, y, k=_k, s=_s) 
            _y = _spl(_x)
            plt.plot(_x, _y, label=f"k={_k}, s={_s}", lw=3)
    plt.xlabel('x')
    plt.ylabel('y(x)')
    #plt.ylim(0, 50)
    plt.legend()
    plt.savefig("06_23c.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(UVS, np, plt, x, y):
    # аппроксимация и сглаживание
    _n = 1000
    _x = np.linspace(1, 12, _n)

    _fig = plt.figure(figsize=(6, 4))
    plt.plot(x, y, 'ko', ms=5, label="исходные данные")

    for _k in (3,): # k - степень сплайна
        for _s in (0, None, 100, 1000):        
            _spl = UVS(x, y, k=_k, s=_s) 
            _y = _spl(_x)
            plt.plot(_x, _y, label=f"k={_k}, s={_s}", lw=3)
    plt.xlabel('x')
    plt.ylabel('y(x)')
    #plt.ylim(0, 50)
    plt.legend()
    plt.savefig("06_23d.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(UVS, x, y):
    # коэффициенты полинома
    _spl = UVS(x, y, k=3, s=0) 
    _c = _spl.get_coeffs()
    _d1 = _spl.derivatives(1)
    _d2 = _spl.derivatives(2)
    _f1 =_d1[0] +_d1[1] +_d1[2]/2 + _d1[3]/6
    _f2 =_d2[0] +_d2[1] +_d2[2]/2 + _d2[3]/6
    len(x), len(_c), _c, _d1, _d2, _f1, _f2
    return


@app.cell
def _(UVS, np, plt, x, y):
    def chunks(x, y, figsize=(6,4)):
        spl = UVS(x, y, k=3, s=0) 
        # цвета для вычерчивания участко сплайна
        colors=['b','r','g','c','m', 'k', 'y']
        n = len(x)
        xx = np.linspace(x[0],x[-1], 1000)
        fig = plt.figure(figsize=figsize)
        # кривая, полученная с помощью интерполяции
        plt.plot(xx, spl(xx), 'k-', lw=4)
        nc = len(colors)
        for i in range(n):
            k = i%nc
            c = colors[k]
            d = spl.derivatives(x[i])
            ii = max(i-3, 0)
            jj = min(i+3, n-1)
            xc = np.linspace(x[ii], x[jj], 200)        
            xx = xc - x[i]
            # вычисляем и рисуем сплайн за пределами его участка
            yc = d[0] + d[1]*xx + d[2]/2*xx**2 + d[3]/6*xx**3
            plt.plot(xc, yc, c+'-', lw=2, label=f"{i=}")
        plt.ylim(0, 50)
        plt.xlabel('x')
        plt.ylabel('y(x)')
        plt.legend()   
        plt.savefig("06_24.png", dpi=300, facecolor='white')

        return fig 

    chunks(x, y)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Двумерная интрполяция
    """)
    return


@app.cell
def _(np):
    # Весовой процент спирта
    ps = np.array([0., 4., 8., 12., 16., 20., 24., 28., 32., 36., 40., 44., 48., 52., 56., 60., 64., 68., 72., 76, 80., 84., 88., 92., 96., 100.])

    # Температура в градусах Цельсия
    ts = np.array([10., 15., 20., 40.])

    # Весовой процент спирта
    pr = np.array([
        [0.99973, 0.99913, 0.99823, 0.99225], #0
        [0.99218, 0.99105, 0.99103, 0.98485], #4
        [0.98660, 0.98584, 0.98478, 0.97808], #8
        [0.98145, 0.98041, 0.97910, 0.97150], #12
        [0.97692, 0.97552, 0.97387, 0.96512], #16
        [0.97252, 0.97068, 0.96864, 0.95856], #20
        [0.96787, 0.96558, 0.96312, 0.95168], #24
        [0.96268, 0.95996, 0.95710, 0.94438], #28
        [0.95655, 0.95357, 0.95038, 0.93662], #32
        [0.94986, 0.94650, 0.94306, 0.92843], #36
        [0.94238, 0.93882, 0.93518, 0.91992], #40
        [0.93433, 0.93062, 0.92685, 0.91108], #44
        [0.92593, 0.92211, 0.91823, 0.90207], #48
        [0.91723, 0.91333, 0.90936, 0.89288], #52
        [0.90831, 0.90433, 0.90031, 0.88335], #56
        [0.89927, 0.89523, 0.89113, 0.87417], #60
        [0.89006, 0.88597, 0.88183, 0.86466], #64
        [0.88074, 0.87660, 0.87241, 0.85507], #68
        [0.87127, 0.86710, 0.86287, 0.84540], #72
        [0.86168, 0.85747, 0.85322, 0.83564], #76
        [0.85197, 0.84772, 0.84344, 0.82588], #80
        [0.84203, 0.83777, 0.83348, 0.81576], #84
        [0.83181, 0.82754, 0.82323, 0.80552], #88
        [0.82114, 0.81688, 0.81257, 0.79491], #92
        [0.80991, 0.80566, 0.80138, 0.78388], #96
        [0.79784, 0.79360, 0.78934, 0.77203], #100
    ])
    return pr, ps, ts


@app.cell
def _(mo):
    mo.md(r"""
    ## Двумерная интерполяция
    ### Конструируем интерполятор
    """)
    return


@app.cell
def _(RBS, pr, ps, ts):
    spl2d = RBS(ps, ts, pr, s=0, kx=3, ky=3)
    return (spl2d,)


@app.cell
def _(mo):
    mo.md(r"""
    Производим интепорполяцию на точках таблицы
    """)
    return


@app.cell
def _(spl2d):
    print(spl2d(0, 10), spl2d(100, 40))
    return


@app.cell
def _(spl2d):
    type(spl2d(100, 40)), spl2d(100, 40).shape
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Вычисляем плотности раствора  спирта на сетке 100 на 100
    """)
    return


@app.cell
def _(np, spl2d):
    tts = np.linspace(10., 40., 101)
    pps = np.linspace(0., 100., 101)
    # Вычисляем значения весового процента и температуры на сетке
    Pr = spl2d(pps, tts, grid=True) # собственно интерполяция
    pps.shape, tts.shape, Pr.shape, pps, tts
    return Pr, pps, tts


@app.cell(hide_code=True)
def _(Pr, np, plt, pps, tts):
    def visualize3d(x, y, Z,  
                    azim=-60, elev=30, roll=0,
                    shrink=0.5, alpha=1, cmap='rainbow',
                    figsize=(10,7), fn=None):
        '''
        Визуализация трехмерной таблицы
        Параметры:
        x, y - данные по осям координат
        z - двумерный визулизируеиый масиив данных    
        azim. elev, roll - углы поворота 
        shrink - параметр, масштабирующий colorbar -
                 соответствие между цветами и значениями
                 по оси z
        alpha - непрозрачность поверхности
        cmap - палитра matplotlib
        figsize - размер рисунка
        fn -путь к файлу в котором сохраняется рисунок

        Функция возвращает:
        fig - объект рисунка
        '''
        fig = plt.figure(figsize=figsize) 
        ax = plt.subplot(111, projection='3d')    
        X, Y = np.meshgrid(x, y)
        cb = ax.plot_surface(X, Y, Z, cmap=cmap, alpha=alpha)
        fig.colorbar(cb, shrink=shrink)

        # вращение рисунка
        ax.view_init(azim=azim, elev=elev, roll=roll)
        ax.set_xlabel(r'$Температура,\ ^oС$')
        ax.set_ylabel(r'$Весовой\ процент\ спирта$')
        ax.set_zlabel(r'$Плотность,\ г/см^3$')
        plt.tight_layout()
        if fn:
            plt.savefig(fn, dpi=300, facecolor="white")
        return fig

    visualize3d(tts, pps, Pr, azim=120, shrink=.75, fn='06_28a.png')
    return (visualize3d,)


@app.cell
def _(Pr, pps, tts, visualize3d):
    visualize3d(tts, pps, Pr, azim=-180, shrink=.75, fn='06_28b.png')
    return


@app.cell
def _(mo):
    azim = mo.ui.slider(label='azim', start=-180, stop=180, value=-60,
                        step=10, debounce=True,show_value=True)
    elev = mo.ui.slider(label='elev', start=0, stop=360, value=30, 
                        step=10, debounce=True,show_value=True)
    roll = mo.ui.slider(label='roll ', start=0, stop=180, value=0, 
                        step=10, debounce=True,show_value=True)

    #visualize3d(azim=azim.value, elev=elev.value, roll=roll.value)
    return azim, elev, roll


@app.cell
def _(azim, elev, mo, roll):
    mo.hstack([azim, elev, roll])
    return


@app.cell
def _(Pr, azim, elev, pps, roll, tts, visualize3d):
    visualize3d(tts, pps, Pr, azim=azim.value, elev=elev.value, roll=roll.value)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Зависимости плотности от температуры
    """)
    return


@app.cell
def _(np, plt, spl2d):
    _t = np.linspace(-10, 60, 100)
    _fig = plt.figure(figsize=(6, 4))
    _p = spl2d(50, _t).flatten()
    plt.plot(_t, _p, lw=3, label=r"$50.0\ ^oC$")
    _p = spl2d(36.6, _t).flatten()
    plt.plot(_t, _p, lw=3, label=r"$36.6\ ^oC$")
    plt.xlabel(r'$Температура,\ ^oС$')
    #plt.ylabel(r'$Весовой\ процент\ спирта$')
    plt.ylabel(r'$Плотность,\ г/см^3$')
    plt.grid()
    plt.legend()
    plt.savefig('06_29a.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(np, plt, spl2d):
    _p = np.linspace(0, 100, 101)
    _fig = plt.figure(figsize=(6, 4))
    _z = spl2d(_p, 36.6).flatten()
    plt.plot(_p, _z, lw=3, label=r"$50.0\ ^oC$")
    # _z = spl2d(_p, 16.0).flatten()
    # plt.plot(_p, _z)
    # _z = spl2d(_p, 40.0).flatten()
    # plt.plot(_p, _z)
    _z = spl2d(_p, 10.0).flatten()
    plt.plot(_p, _z, lw=3, label=r"$10.0\ ^oC$")
    #plt.xlabel(r'$Температура,\ ^oС$')
    plt.xlabel(r'$Весовой\ процент\ спирта,\ \%$')
    plt.ylabel(r'$Плотность,\ г/см^3$')
    plt.grid()
    plt.legend()
    plt.savefig('06_29b.png', dpi=300, facecolor="white")
    _fig
    return


if __name__ == "__main__":
    app.run()
