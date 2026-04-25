import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from e07_05 import draw, get_fish, get_fish_outline, get_F, get_G
    from e07_05 import flip_x, flip_y, scale, translate
    from e07_07 import f_square_limit

    mo.md("""
    # Натягиваем сову на глобус, или нечто совсем иное по Монти Пайтон 
    Пытаемся изобразить квадратный предел в в трех измерениях

    Мы не сможем напрямую использовать инструменты трехмерного рисования matplotlib,
    т.к. работаем не с линиями и поверхностями, а с заплатками.
    Поэтому нам придется вернуться к первому курсу ВУЗа и вспомнить о черчении и проекциях
    трехмерных фигур на плоскость.

    Мы не будем использовать инструменты начертательной геометрии, а сразу же применим для работы 
    диметрическую проекцию  и линейную алгебру.

    >Пономарев В.В. Машинная графика. Учебное пособие. Ред. 2. Озерск: ОТИ МИФИ, 2006. — 72 с. [Электронный ресурс]. URL: http://revol.ponocom.ru/-d/ReVoL-KG2-2006.pdf (дата обращения 29.04.2025)

    Начнем с того, что нарисуем три оси координат на плоскости.

    Пусть у нас имеется точка в трехмерном пространстве $u=(x, y, z)$. Мы могли бы рассмотреть ее проекцию на плоскость $x0z$, но тогда будет потеряна вся информация от данных по оси y. 
    Давайте выполним повороты относительно двух осей в трехмерном пространстве так, чтобы изменения масштабов по двум осям из трех было бы одинаковыми при проектировании на плоскость. Такое преобразование называется *диметрическим*.
    Ниже приводится функция dimet, выполняюшая диметрическое преобразование.

    """)
    return (
        draw,
        f_square_limit,
        flip_x,
        get_G,
        get_fish,
        get_fish_outline,
        mo,
        np,
        plt,
    )


@app.cell
def _(np):
    def dimet(u):
        """Диметрическое отображение точки u в трехмерном пространстве"""
        D = np.array(
            [
                [0.935414346693485, 0.0, 0.353553390593274],
                [0.133630620956212, 0.925820099772551, -0.353553390593274],
                [-0.327326835353989, 0.377964473009227, 0.866025403784439],
            ]
        )
        return D @ np.array(u)

    return (dimet,)


@app.cell
def _(mo):
    mo.md(r"""
    Функция dimet позволяет работать с точками, заданными как кортежами и списками, так и массивами NumPy
    """)
    return


@app.cell
def _(dimet, np):
    print(f"""
    Списки
    {dimet([1, 0, 0])=} 
    {dimet([0, 1, 0])=} 
    {dimet([0, 0, 1])=}

    Массивы
    {dimet(np.array([1, 0, 0]))=} 
    {dimet(np.array([0, 1, 0]))=} 
    {dimet(np.array([0, 0, 1]))=}
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    Проекцию на плоскость можно осуществить тремя различными способами, зануляя заначение по одной из координатных осей
    """)
    return


@app.cell
def _(dimet):
    # тестировние dimet
    dimet([1, 1, 1])
    return


@app.cell
def _(dimet, np):
    def proj(u, axis="x"):
        """
        Диметрическая проекция точки u в трехмерном пространстве
        на плоскости y0z, x0z, x0y
        """
        v = dimet(u)

        if axis == "x":
            return np.array([v[1], v[2]]), "Проекция на y0z"
        elif axis == "y":
            return np.array([v[0], v[2]]), "Проекция на x0z"
        else:
            return np.array([v[0], v[1]]), "Проекция на x0y"

    return (proj,)


@app.cell
def _(proj):
    proj([1, 1, 1], "x")
    return


@app.cell
def _(proj):
    # Тестируем proj
    u1, u2, u3 = [1, 0, 0], [0, 1, 0], [0, 0, 1]
    print(f"""
    x
    {proj(u1, 'x')=} 
    {proj(u2, 'x')=}, 
    {proj(u3, 'x')=}

    y
    {proj(u1, 'y')=} 
    {proj(u2, 'y')=}, 
    {proj(u3, 'y')=}

    z
    {proj(u1, 'z')=} 
    {proj(u2, 'z')=}, 
    {proj(u3, 'z')=}
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    Теперь нарисуем диметрические проекции трех осей на плоскость
    """)
    return


@app.cell
def _(np, proj):
    def three_axis(ax, axis="x"):
        vs = np.eye(3)
        for i in range(3):
            v = proj(vs[i, :], axis)
            # print(f"{v=}, {v[0]=}, {v[1]=}")
            ax.plot([0, v[0][0]], [0, v[0][1]], "k-")
            ax.set_title(v[1])
        return ax

    return (three_axis,)


@app.cell
def _(plt, three_axis):
    # тестируем three_axis
    _fig = plt.figure(figsize=(9, 3))
    _ax = plt.subplot(1, 3, 1)
    _ax = three_axis(_ax, axis="x")
    _ax = plt.subplot(1, 3, 2)
    _ax = three_axis(_ax, axis="y")
    _ax = plt.subplot(1, 3, 3)
    _ax = three_axis(_ax, axis="z")
    plt.tight_layout()
    _fig
    return


@app.cell
def _(plt, three_axis):
    def three_dimet_proj(f=three_axis, size=3):
        """
        Рисуем три диметрические проекции
        координатных осей
        size - высота картинки
        """
        axises = ("x", "y", "z")
        fig = plt.figure(figsize=(size * 3, size))
        for i, axis in enumerate(axises):
            ax = plt.subplot(1, 3, i + 1)
            ax = f(ax, axis=axis)
        plt.tight_layout()
        return fig

    return (three_dimet_proj,)


@app.cell
def _(three_dimet_proj):
    _fig = three_dimet_proj()
    # plt.savefig("07_28.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Поверхности в трехмерном пространстве, на которых мы будем рисовать фигуры
    """)
    return


@app.cell
def _(np):
    def mebius(u, v):
        # отображение единичного квадрата на ленту Мебиуса: (u, v)-> x, y, z
        u *= 2 * np.pi
        return np.array(
            [
                (1 + v / 2 * np.cos(u / 2)) * np.cos(u),
                (1 + v / 2 * np.cos(u / 2)) * np.sin(u),
                v / 2 * np.sin(u / 2),
            ]
        )

    return (mebius,)


@app.cell
def _(np):
    def cylinder(x, y, r=0.5):
        # отображение единичного квадрата на цилиндр: (u, v)-> x, y, z
        return [r * np.cos(2 * np.pi * x), r * np.sin(2 * np.pi * x), y]

    return (cylinder,)


@app.cell
def _(np):
    def thor(x, y, r=0.5, R=1):
        # отображение единичного квадрата на тор: (u, v)-> x, y, z
        x = 2 * np.pi * x
        y = 2 * np.pi * (y - 0.5)
        return [
            (R + r * np.cos(y)) * np.cos(x),
            (R + r * np.cos(y)) * np.sin(x),
            r * np.sin(y),
        ]

    return (thor,)


@app.cell
def _(mo):
    mo.md(r"""
    ### Рисуем цидиндр, тор и ленту Мебиуса
    """)
    return


@app.cell
def _(cylinder, mebius, np, plt, thor):
    _n = 50
    _fs = 20
    _x = np.linspace(0, 1, _n)
    _X, _Y = np.meshgrid(_x, _x)

    _fig = plt.figure(figsize=(15, 5))
    _ax1 = plt.subplot(131, projection="3d")
    _U, _V, _W = cylinder(_X, _Y)
    _ax1.plot_wireframe(_U, _V, _W, color="black", linewidth=0.5)
    # _ax1.set_title("Цилиндр", fontsize=_fs)
    _ax1.set_xlabel("X")
    _ax1.set_ylabel("Y")
    _ax1.set_zlabel("Z")

    _ax2 = plt.subplot(132, projection="3d")
    _U, _V, _W = thor(_X, _Y)
    _ax2.plot_wireframe(_U, _V, _W, color="black", linewidth=0.5)
    # _ax2.set_title("Тор", fontsize=_fs)
    _ax2.set_xlabel("X")
    _ax2.set_ylabel("Y")
    _ax2.set_zlabel("Z")

    _ax3 = plt.subplot(133, projection="3d")
    _U, _V, _W = mebius(_X, _Y)
    _ax3.plot_wireframe(_U, _V, _W, color="black", linewidth=0.5)
    # _ax3.set_title("Лента Мебиуса", fontsize=_fs)
    _ax3.set_xlabel("X")
    _ax3.set_ylabel("Y")
    _ax3.set_zlabel("Z")

    plt.tight_layout()
    # plt.savefig("07_29.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Отображение на поверхность
    """)
    return


@app.cell
def _(proj):
    def apply_func(f, func, axis="x"):
        """
        Отображение (натягивание) фигуры, заданной matplotlib Path
        на поверхность, заданной функцией отображения
        f - фигура
        func - функция отображения
        axis - задание проекции
        """
        v = f.vertices
        # print(f"{v=}")
        n, m = v.shape
        for i in range(n):
            # print(f"apply_func {i=}, {v[i,0]=}, {v[i,1]=}, {type(v[i,0])=}, {type(v[i,1])=}")
            xy = func(v[i, 0], v[i, 1])
            v[i, :] = proj(xy, axis)[0]
        f.vertices = v
        return f

    return (apply_func,)


@app.cell
def _(apply_func, cylinder, get_G):
    apply_func(get_G(), cylinder, axis="x")
    return


@app.cell
def _(apply_func, cylinder, get_G):
    apply_func(get_G(), cylinder, axis="y")
    return


@app.cell
def _(apply_func, cylinder, get_G):
    apply_func(get_G(), cylinder, axis="z")
    return


@app.cell
def _(apply_func, cylinder, draw, f_square_limit, get_fish_outline):
    def fig_on_surface(
        fig=get_fish_outline(),
        map=f_square_limit,
        surface=cylinder,
        n=0,
        axis=False,
        fill=False,
        prj="x",
        figsize=(3, 3),
    ):
        """
        Отображение фигуры на плоскость в трехмерном пространстве
        fig - порождающая фигура,
        map - преобразование порождающей фигуры,
        surface - поверхность, на которую отображается фигура
        n - уровень рекурсии при преобразовании породающей фигуры,
        axis - признак отображения координатных осей и оцифровки,
        fill - признак закраски фигуры при рисовании,
        prj - вид проекции,
        figsize - размер рисунка
        Функция возвращает  изображение
        """
        # создаем сложную фигуру из порождающей
        cf = map(n, fig)
        f = apply_func(cf, surface, axis=prj)

        return draw(
            f, fill=fill, axis=axis, box=False, figsize=figsize, ncols=1, nrows=1
        )

    return (fig_on_surface,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Символ Г на цилиндре
    """)
    return


@app.cell
def _(fig_on_surface, get_G):
    fig_on_surface(get_G(), map=lambda n, f: f, prj="x")
    return


@app.cell
def _(fig_on_surface, get_G):
    fig_on_surface(get_G(), map=lambda n, f: f, prj="y")
    return


@app.cell
def _():
    return


@app.cell
def _(fig_on_surface, get_G):
    fig_on_surface(get_G(), map=lambda n, f: f, prj="z")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Квадратный предел из символов Г на цилиндре
    """)
    return


@app.cell
def _(fig_on_surface, flip_x, get_G):
    G = flip_x(get_G())
    _fig = fig_on_surface(G, n=4, prj="x", fill=True)
    # plt.savefig("07_30a.png", dpi=300, facecolor='white')
    _fig
    return (G,)


@app.cell
def _(G, fig_on_surface):
    _fig = fig_on_surface(G, n=4, prj="y", fill=True)
    # plt.savefig("07_30b.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(G, fig_on_surface):
    _fig = fig_on_surface(G, n=4, prj="z", fill=True)
    # plt.savefig("07_30c.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Рыбка на цилиндре
    """)
    return


@app.cell
def _(fig_on_surface, flip_x, get_fish):
    _fish = flip_x(get_fish())
    _fig = fig_on_surface(_fish, n=1, prj="x", fill=True)
    # plt.savefig("07_31a.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(fig_on_surface, flip_x, get_fish):
    _fish = flip_x(get_fish())
    _fig = fig_on_surface(_fish, n=1, prj="y", fill=True)
    # plt.savefig("07_31b.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(fig_on_surface, flip_x, get_fish):
    _fish = flip_x(get_fish())
    _fig = fig_on_surface(_fish, n=1, prj="z", fill=True)
    # plt.savefig("07_31c.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(fig_on_surface, flip_x, get_fish_outline):
    _fish_outline = flip_x(get_fish_outline())
    _fig = fig_on_surface(_fish_outline, n=3, prj="x", fill=True)
    # plt.savefig("07_32a.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(fig_on_surface, flip_x, get_fish_outline):
    _fish_outline = flip_x(get_fish_outline())
    _fig = fig_on_surface(_fish_outline, n=3, prj="y", fill=True)
    # plt.savefig("07_32b.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(fig_on_surface, flip_x, get_fish_outline):
    _fish_outline = flip_x(get_fish_outline())
    _fig = fig_on_surface(_fish_outline, n=3, prj="z", fill=True)
    # plt.savefig("07_32c.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Рыбка на торе
    """)
    return


@app.cell
def _(fig_on_surface, flip_x, get_fish, thor):
    _fish = flip_x(get_fish())
    _fig = fig_on_surface(_fish, n=1, prj="x", fill=True, surface=thor)
    # plt.savefig("07_32a.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(fig_on_surface, flip_x, get_fish, thor):
    _fish = flip_x(get_fish())
    _fig = fig_on_surface(_fish, n=1, prj="y", fill=True, surface=thor)
    # plt.savefig("07_32b.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(fig_on_surface, flip_x, get_fish, thor):
    _fish = flip_x(get_fish())
    _fig = fig_on_surface(_fish, n=1, prj="z", fill=True, surface=thor)
    # plt.savefig("07_32c.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Рыбка на ленте Мебиуса
    """)
    return


@app.cell
def _(G, fig_on_surface, mebius):
    _fig = fig_on_surface(G, n=4, prj="x", fill=True, surface=mebius)
    # plt.savefig("07_33a.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(G, fig_on_surface, mebius):
    _fig = fig_on_surface(G, n=4, prj="y", fill=True, surface=mebius)
    # plt.savefig("07_33b.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(G, fig_on_surface, mebius):
    _fig = fig_on_surface(G, n=4, prj="z", fill=True, surface=mebius)
    # plt.savefig("07_33c.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Упражняемся с символом Ж
    Соберем его не из отрезков прямых, а кривых Безье
    """)
    return


@app.cell
def _():
    from svgpath2mpl import parse_path
    from matplotlib.path import Path
    import matplotlib.patches as patches
    from matplotlib.patches import PathPatch, Rectangle


    def get_J():
        """
        Символ Ж на кривых Безье
        """
        J = """
    M 0.0, 0.0
    C  0.083,  0.150,  0.167,  0.300,  0.250,  0.450, 
    C  0.250,  0.483,  0.250,  0.517,  0.250,  0.550, 
    C  0.167,  0.700,  0.083,  0.850,  0.000,  1.000, 
    C  0.033,  1.000,  0.067,  1.000,  0.100,  1.000, 
    C  0.183,  0.850,  0.267,  0.700,  0.350,  0.550, 
    C  0.383,  0.550,  0.417,  0.550,  0.450,  0.550, 
    C  0.450,  0.700,  0.450,  0.850,  0.450,  1.000, 
    C  0.483,  1.000,  0.517,  1.000,  0.550,  1.000, 
    C  0.550,  0.850,  0.550,  0.700,  0.550,  0.550, 
    C  0.583,  0.550,  0.617,  0.550,  0.650,  0.550, 
    C  0.733,  0.700,  0.817,  0.850,  0.900,  1.000, 
    C  0.933,  1.000,  0.967,  1.000,  1.000,  1.000, 
    C  0.917,  0.850,  0.833,  0.700,  0.750,  0.550, 
    C  0.750,  0.517,  0.750,  0.483,  0.750,  0.450, 
    C  0.833,  0.300,  0.917,  0.150,  1.000,  0.000, 
    C  0.967,  0.000,  0.933,  0.000,  0.900,  0.000, 
    C  0.817,  0.150,  0.733,  0.300,  0.650,  0.450, 
    C  0.617,  0.450,  0.583,  0.450,  0.550,  0.450, 
    C  0.550,  0.300,  0.550,  0.150,  0.550,  0.000, 
    C  0.517,  0.000,  0.483,  0.000,  0.450,  0.000, 
    C  0.450,  0.150,  0.450,  0.300,  0.450,  0.450, 
    C  0.417,  0.450,  0.383,  0.450,  0.350,  0.450, 
    C  0.267,  0.300,  0.183,  0.150,  0.100,  0.000, 
    C  0.067,  0.000,  0.033,  0.000,  0.000,  0.000
        """
        return parse_path(J)

    return (get_J,)


@app.cell
def _(draw, get_J):
    J = get_J()
    _fig = draw(J, fill=True)
    # plt.savefig("07_34a.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Отображаем Ж на круг
    """)
    return


@app.cell
def _(get_J, np):
    from e07_05 import rot_90, rot_45, rotate_deg_around


    def square_2_circle(x, y):
        """
        Преобразование квадрата на круг"""
        xx = 2 * x - 1
        yy = 2 * y - 1
        x2 = xx**2
        y2 = yy**2
        r = np.sqrt(x2 + y2)
        r = np.where(r <= 1e-6, np.inf, r)
        u = np.where(x2 >= y2, np.sign(xx) * x2 / r, np.sign(yy) * xx * yy / r)
        v = np.where(x2 >= y2, np.sign(xx) * xx * yy / r, np.sign(yy) * y2 / r)
        return u, v


    def to_circle(J):
        x, y = J.vertices[:, 0], J.vertices[:, 1]
        u, v = square_2_circle(x, y)
        J.vertices[:, 0], J.vertices[:, 1] = u, v
        return J


    JC = to_circle(get_J())
    return JC, rot_90, to_circle


@app.cell
def _(JC, draw):
    _fig = draw(JC, axis=False, figsize=(3, 3), box=False, fill=True)
    # plt.savefig("07_34b.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(draw, get_J, rot_90):
    _fig = draw(rot_90(get_J()), axis=False, figsize=(3, 3), box=False, fill=True)
    _fig
    return


@app.cell
def _(draw, get_J, rot_90, to_circle):
    _fig = draw(
        to_circle(rot_90(get_J())),
        axis=False,
        figsize=(3, 3),
        box=False,
        fill=True,
    )
    _fig
    return


@app.cell
def _(draw, f_square_limit, get_J):
    _fj = f_square_limit(f=get_J(), n=0)
    _fig = draw(_fj, axis=False, figsize=(3, 3), box=False, fill=True)
    # plt.savefig("97_35a.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(draw, f_square_limit, get_J, to_circle):
    _fj = f_square_limit(f=get_J(), n=0)
    _fig = draw(to_circle(_fj), axis=False, figsize=(3, 3), box=False, fill=True)
    # plt.savefig("07_35b.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(draw, f_square_limit, get_J, to_circle):
    _fj = f_square_limit(f=to_circle(get_J()), n=0)
    _fig = draw(_fj, axis=False, figsize=(3, 3), box=False, fill=True)
    # plt.savefig("07_35c.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(draw, f_square_limit, get_J, to_circle):
    _fj = f_square_limit(f=to_circle(get_J()), n=1)
    _fig = draw(_fj, axis=False, figsize=(3, 3), box=False, fill=True)
    # plt.savefig("07_35d.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(draw, f_square_limit, get_J, to_circle):
    _fj = f_square_limit(f=to_circle(get_J()), n=1)
    _fig = draw(_fj, axis=False, figsize=(3, 3), box=False, fill=False)
    _fig
    return


@app.cell
def _(draw, f_square_limit, get_J, to_circle):
    _fj = f_square_limit(f=to_circle(get_J()), n=3)
    _fig = draw(_fj, axis=False, figsize=(3, 3), box=False, fill=False)
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Круглый предел из символа Ж на цилиндре
    """)
    return


@app.cell
def _(cylinder, fig_on_surface, get_J, to_circle):
    _fj = to_circle(get_J())
    _fig = fig_on_surface(_fj, n=0, prj="x", fill=True, surface=cylinder)
    # plt.savefig("07_36a.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(cylinder, fig_on_surface, get_J, to_circle):
    _fj = to_circle(get_J())
    _fig = fig_on_surface(_fj, n=1, prj="x", fill=True, surface=cylinder)
    # plt.savefig("07_36b.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(cylinder, fig_on_surface, get_J, to_circle):
    _fj = to_circle(get_J())
    _fig = fig_on_surface(_fj, n=1, prj="y", fill=True, surface=cylinder)
    # plt.savefig("Э_35c.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(cylinder, fig_on_surface, get_J, to_circle):
    _fj = to_circle(get_J())
    _fig = fig_on_surface(_fj, n=1, prj="z", fill=True, surface=cylinder)
    # plt.savefig("Э_35c.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Круглый предел из символе  Ж на торе
    """)
    return


@app.cell
def _(fig_on_surface, get_J, thor, to_circle):
    _fj = to_circle(get_J())
    _fig = fig_on_surface(_fj, n=1, prj="x", fill=True, surface=thor)
    # plt.savefig("07_36c.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Круглый предел из символе  Ж на ленте мебиуса
    """)
    return


@app.cell
def _(fig_on_surface, get_J, mebius, to_circle):
    _fj = to_circle(get_J())
    _fig = fig_on_surface(_fj, n=2, prj="x", fill=True, surface=mebius)
    # plt.savefig("07_36d.png", dpi=300, facecolor='white')
    _fig
    return


if __name__ == "__main__":
    app.run()
