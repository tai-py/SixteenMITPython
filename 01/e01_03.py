import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    from scipy.special import fresnel
    import matplotlib.pyplot as plt
    from scipy.integrate import quad
    from scipy.optimize import root
    import sympy as smp

    mo.md("# Переходной участок в виде **клотоиды**")
    return fresnel, mo, np, plt, quad, root, smp


@app.cell
def _(np):
    def circle(t, R=1, x0=0, y0=0):
        """
        Параметрическое представление окружности
        t - параметр
        R - радиус окружности
        x0, y0 - координаты центра окружности
        Функция возвращает  координты
        точки окружности, соответствующие
        значению параметра t
        """
        return R * np.sin(t) + x0, y0 - R * np.cos(t)
    return (circle,)


@app.cell
def _(circle, np, plt, t):
    _n = 1000
    _t = np.linspace(0, 2*np.pi, _n)
    _x, _y = circle(t, R=1, x0=1, y0=1)
    _fig = plt.figure(figsize=(4,4))
    plt.plot(_x, _y, lw=3)
    plt.axis('equal')
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Интегралы Френеля 
    В соответствие с [Википедией](https://ru.wikipedia.org/wiki/)  [интегралы Френеля](https://ru.wikipedia.org/wiki/Интегралы_Френеля) $S(x)$ и $C(x)$ — это специальные функции, названные в честь Огюстена Жана Френеля,  они определяются как 

    $$ S(x)= \int_0^x sin(t^2)dt, \ C(x)= \int_0^x cos(t^2)dt. \tag{1} $$

    Иногда, в частности в библиотеке scipy ([scipy.special.fresnel](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.fresnel.html)), используется другое определение интегралов Френеля: 

    $$ S_m(x)= \int_0^x sin(\frac{\pi \cdot t^2}{2})dt, \ C_m(x)= \int_0^x cos(\frac{\pi \cdot t^2}{2})dt. \tag{2} $$

    Для приведения результата вызовов функции scipy.special.fresnel к определению (1) напишем функцию clotoid:
    """
    )
    return


@app.cell
def _(fresnel, np):
    def clotoid(t):
        """
        Параметрическое задание клотоиды
        Параметры:
        t - параметр.    
        Функция возвращает значения
        интегралов Френеля, соответствующие
        значению параметра t
        """
        ss, cc = fresnel(t / np.sqrt(np.pi / 2))
        scaled_ss = np.sqrt(np.pi / 2) * ss
        scaled_cc = np.sqrt(np.pi / 2) * cc
        return scaled_cc, scaled_ss
    return (clotoid,)


@app.cell
def _(clotoid, np):
    clotoid(np.inf)
    return


@app.cell
def _(mo):
    mo.md(r"""Нарисуем графики функций $C(t)$ и $S(t)$""")
    return


@app.cell
def _(fresnel, np, plt):
    n, tmax = 1000, 2 * np.pi
    t = np.linspace(0, tmax, n)
    _fig = plt.figure(figsize=(5, 4))
    cs, ss = fresnel(t / np.sqrt(np.pi / 2))
    plt.plot(t, cs, "b-", lw=3, label="$C(t)$")
    plt.plot(t, ss, "r-", lw=3, label="$S(t)$")
    plt.xlabel("$t$")
    plt.ylabel(r"$C(t),\ S(t)$")
    plt.grid()
    plt.legend()
    _fig
    return (t,)


@app.cell
def _(mo):
    mo.md(
        r"""
    Интегралы Френеля можно вычислить непоcредственно с помощью функции [scipy.integrate.
    quad](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.fresnel.html).
    Функции передаются подынтегральная функция и пределы интегрирования, возвращает она 
    значение интеграла и погрешность.
    """
    )
    return


@app.cell
def _(np, quad):
    (quad(lambda t: np.cos(t**2), 0, 5), quad(lambda t: np.sin(t**2), 0, 5))
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Напишем функцию clotoid_q, дублирующую функциональность clotoid,
    но использующую непосредственнок вычисление интегралов Френеля
    """
    )
    return


@app.cell
def _(np, quad):
    def clotoid_q(t, a=1):
        if isinstance(t, (int, float)):
            t = np.array([t], dtype=float)
        cs, ss = (
            np.asarray(t, dtype=float, copy=True),
            np.asarray(t, dtype=float, copy=True),
        )  # преобразуем в массивы
        # quad не работает с массивами
        for _, tt in enumerate(t):
            cs[_] = quad(lambda t: np.cos(t**2), 0, tt)[0]
            ss[_] = quad(lambda t: np.sin(t**2), 0, tt)[0]
        return cs, ss

    clotoid_q(1), clotoid_q([1, 2, 3])
    return (clotoid_q,)


@app.cell
def _(mo):
    mo.md(r"""Вычислим максимальную погрешность вычисления интегралов Френеля:""")
    return


@app.cell
def _(clotoid, clotoid_q, np, t):
    _cs, _ss = clotoid(t)
    _cs_q, _ss_q = clotoid_q(t)
    error = max(np.max(np.abs(_cs - _cs_q)), np.max(np.abs(_ss - _ss_q)))
    error
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Оба способа дают результаты, отличаюшиеся друг от друга не более чем на $3 \cdot 10^{-15}$, так что 
    можно пользоваться любым способом, но первый быстрее.

    Вычислим, куда придет клотоида на бесконечности с помощью непосредственного интегрирования:
    """
    )
    return


@app.cell
def _(clotoid, np):
    clotoid(np.inf)
    return


@app.cell
def _(clotoid, np, plt, t):
    # Нарисуем теперь клотоиду:
    # import marimo as mo
    # import numpy as np
    # from scipy.special import fresnel
    # import matplotlib.pyplot as plt
    # from scipy.integrate import quad
    # from scipy.optimize import root
    # import sympy as smp

    _n, _tmax = 10000, 20 * np.pi
    _t = np.linspace(0, _tmax, _n)
    _cc, _ss = clotoid(t)
    _cc_inf, _ss_inf = clotoid(np.inf)
    _fig = plt.figure(figsize=(4, 4))
    plt.plot(_cc, _ss)
    plt.plot(_cc_inf, _ss_inf, "r+", ms=15)
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('y')
    #plt.savefig('01_09.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(circle, clotoid):
    def rh1(t, R=1, a=1):
        tc, tr = t
        xc, yc = clotoid(tc, a)
        xr, yr = circle(tr, R)
        return xc - xr, yc - yr
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Нам нужно искать более гладкий переход на поворотный круг. Используем  для этого параметр $a$ функции clotoid, но для этого нужно дополнительное условие. Путь при пересечении клотоиды и окружности кроме равенства координат 
    приравняем друг к другу кривизну клотоиды и окружности.

    Для параметрически заданных кривых  $x(t), y(t)$ кривизна вычисляется следующим образом: 

    $$K(t) = \frac{|x^{''}(t) \cdot y^{'}(t) - y^{''}(t) \cdot x^{'}(t)|}
    {\left (\sqrt{(x^{'}(t))^2 + y^{'}(t))^2} \right)^3}. \tag{3}$$

    В качестве упражнения вычислим кривизну клотоиды и окружности, заданных параметрически.
    """
    )
    return


@app.cell
def _(smp):
    smp.init_printing()

    x_s = smp.Symbol("x_s", positive=True)
    y_s = smp.Symbol("y_s", positive=True)
    a_s = smp.Symbol("a_s", positive=True)
    t_s = smp.Symbol("t_s", positive=True)

    def curvature(x_s, y_s, t_s):
        """
        Символьное вычисление кривизны функции,
        заданной параметрически, через ее производные
        Параметры:
        x_s - производная по t горизонтальной составляющей,
        y_s - производная по t вертикальной составляющей,
        t_s -параметр
        Функция возвращает формулу кривизны кривой, как
        функцию от t_s
        """
        x_2 = x_s.diff(t_s)
        y_2 = y_s.diff(t_s)
        c = smp.Abs(x_2 * y_s - y_2 * x_s) / (smp.sqrt(x_s**2 + y_s**2)) ** 3
        return smp.simplify(c)

    curvature(-a_s * smp.sin(t_s), a_s * smp.cos(t_s), t_s)
    return a_s, curvature, t_s


@app.cell
def _(a_s, curvature, smp, t_s):
    curvature(a_s * smp.cos(t_s**2), a_s * smp.sin(t_s**2), t_s)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Оставим клотоиду в начале координат, будем менять координаты
    центра и радиус повортного круга.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Нам нужно подобрать $x_0,y_0,R$ так, чтобы в точке пересечения у нас совпадали: 

    - координаты;
    - вертикальные и горизонтальные скорости (производные),
    - кривизна клотоиды и окружности.

    Реализуем это функцией rh:
    """
    )
    return


@app.cell
def _(clotoid, np):
    def rh(t, R=0.5):
        '''
        Функция, передаваемая библиотечной функции
        root для решения системы алгебраических
        уравнений
        t - кортеж параметров, включающий в себя:
        tc - значение параметра клотоиды в точке пересечения,
        tr - значение параметра окружности в точке пересечения,
        x0, y0 - координаты центра круга
        '''
        tc, tr, x0, y0 = t # распаковываем параметры
        # координаты кривых
        xc, yc = clotoid(tc) # клотоида
        xr, yr = x0 + R*np.sin(tr), y0 - R*np.cos(tr) # окружность
        # производные
        xcs, ycs = np.cos(tc**2), np.sin(tc**2)
        xrs, yrs = R*np.cos(tr), R*np.sin(tr)
        dyc_dxc = ycs/xcs
        dyr_dxr = yrs/xrs
        # кривизна
        kc = 2*tc
        kr = 1/R
        # уравнения
        return [
            xc - xr, # горизонтальная координата
            yc - yr, # вертикальная координата       
            dyc_dxc - dyr_dxr, # производные
            kc - kr # кривизна
        ]

    return (rh,)


@app.cell
def _(rh, root):
    # тестируем решение алгебраических уравнений
    root(rh, (2.5, 1, 0.5, 0.5), args=(.05,)) 
    return


@app.cell
def _():
    return


@app.cell
def _(clotoid, np):
    clotoid(0.5), -4.720e-01 +np.sin(1.321e+00), 2.889e-01 - np.cos(1.321e+00)
    return


@app.cell
def _(rh, root):
    root(rh, (0.1, 0.1, 0.1, 0.1), args=(.3,))
    return


@app.cell
def _(circle, clotoid, np, plt, rh, root):
    def draw_clotoid_circle(R=1.,
                            t0 = (0.1, 0.1, 0., 0.),
                            c_color='b', r_color='r', 
                            tmax= 2*np.pi, ms=10,
                            figsize = (4,4), n=1000, 
                            axis=True,
                            lims=(-0.5, 1.5)
                            ):
        '''
        Вычисление и визуализация  переходного участка
        с клотоиды на круг
        Параметры:
        t0 - кортеж начальных значений параметров, включающий
        в себя:
        tc - значение параметра клотоиды в точке пересечения,
        tr - значение параметра окружности в точке пересечения,
        x0, y0 - координаты центра круга,
        c_color - цвет для отображения клотоиды,
        r_color - цвет для отображения откружности,
        tmax - максимальное значение параметра t,
        ms - размер маркеров,
        figsize - размер картинки,
        n - число разбиений кривых на участки,
        axis - признак отображения осей координат и оцифровки
        Функция возвращает объект картинки
        '''
        slv = root(rh, t0, args=(R,))
        x0, y0 = 0., 0.
        tc, tr, x0, y0 = slv.x
        t = np.linspace(0, tmax, n)
        xc, yc = clotoid(t) 
        xr, yr = circle(t, R=R, x0=x0, y0=y0)

        # рисуем
        fig = plt.figure(figsize=figsize) 
        # круг и центр
        plt.plot(xr, yr, r_color+'-')
        plt.plot(x0, y0, r_color+'+', ms=ms)

        if slv.success:   
            # клотоида
            plt.plot(xc, yc, c_color+'-')
            xi, yi = clotoid(np.inf) 
            plt.plot(xi, yi, c_color+'+', ms=ms) 
            # точка пересечения
            xrc, yrc = circle(tr, R=R, x0=x0, y0=y0) 
            plt.plot(xrc, yrc, r_color+'+', ms=ms)
        else:
            # рисуем только клотоиду
            plt.plot(xc, yc, c_color+'-')
            xi, yi = clotoid(np.inf) 
            plt.plot(xi, yi, c_color+'+', ms=ms) 

        if lims: # задаем границы по осям координат
            plt.xlim(*lims)
            plt.ylim(*lims) 

        if not axis:
            plt.axis('off')
        else:        
            plt.grid()
        plt.title(f'R={R:5.3f}') # заголовок

        return fig 


    draw_clotoid_circle(R=.5)   
    return (draw_clotoid_circle,)


@app.cell
def _(draw_clotoid_circle):
    draw_clotoid_circle(R=0.05, t0=(1.000e+01,  1.204e+01,  6.264e-01,  6.268e-0)) 
    return


@app.cell
def _(draw_clotoid_circle):
    draw_clotoid_circle(R=.1)
    return


@app.cell
def _(draw_clotoid_circle, plt):
    _fig = draw_clotoid_circle(R=.2)
    plt.savefig('01.10a.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(draw_clotoid_circle, plt):
    _fig = draw_clotoid_circle(R=.3)
    plt.savefig('01.10b.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(draw_clotoid_circle):
    draw_clotoid_circle(R=.35)
    return


@app.cell
def _(draw_clotoid_circle):
    draw_clotoid_circle(R=.4)
    return


@app.cell
def _(draw_clotoid_circle, plt):
    _fig = draw_clotoid_circle(R=.5)
    plt.savefig('01.10c.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(draw_clotoid_circle):
    draw_clotoid_circle(R=0.7)
    return


@app.cell
def _(draw_clotoid_circle, plt):
    _fig = draw_clotoid_circle(R=1)
    plt.savefig('01.10d.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""Анимация окружности и переходного участка  при изменении радиуса поворотного круга""")
    return


@app.cell
def _(draw_clotoid_circle):
    import gif

    @gif.frame
    def frame(i):
        rmin, rmax,  step = 0.05, 1., 0.01    
        rr = rmax - rmin
        n = rr // step +1
        R = rmin + i * rr/n
        return draw_clotoid_circle(R=R)

    frame(6)
    return frame, gif


@app.cell
def _(mo):
    mo.md(r"""Собираем кадры и сохраняем анимацию в файловой системе""")
    return


@app.cell
def _(frame, gif):
    frames = [frame(i) for i in range(145)]
    gif.save(frames, 'clotoid.gif', duration=200)
    return


@app.cell
def _(mo):
    mo.md(r"""Анимация переходного участка и поворотного круга при изменении его радиуса""")
    return


@app.cell
def _(mo):
    mo.image('clotoid.gif', width='80%').center() 
    return


if __name__ == "__main__":
    app.run()
