import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")

with app.setup:
    # Initialization code that runs before all other cells
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from e07_05 import draw, above, beside
    from e07_05 import (
        get_blank,
        four,
        get_F,
        get_fish,
        get_fish_outline,
        get_G,
        get_triangle,
    )
    from e07_05 import flip_x, flip_y, nine, rot_45, rot_90
    from e07_05 import scale, translate, union


@app.cell
def _():
    mo.md(r"""
    # Начинаем сборку квадратного предела
    Сначала нарисуем исходные фигуры
    """)
    return


@app.cell
def _():
    _fig = draw(
        get_fish(),
        get_fish_outline(),
        get_triangle(),
        get_G(),
        ncols=4,
        axis=False,
        figsize=(12, 3),
    )
    # plt.savefig('07_15.png', dpi=300, facecolor='white')
    # _fig
    return


@app.cell
def _():
    mo.md(r"""
    ### Унифицируем исходные фигуры
    """)
    return


@app.cell
def _():
    fish = flip_x(get_fish())
    fish_outline = flip_x(get_fish_outline())
    triangle = flip_x(get_triangle())
    G = flip_x(get_G())

    _fig = draw(
        fish, fish_outline, triangle, G, ncols=4, axis=False, figsize=(12, 3)
    )
    # plt.savefig('07_16.png', dpi=300, facecolor='white')
    _fig
    return G, fish, fish_outline, triangle


@app.function
def two_side_by_side(f):
    """
    Отражаем исходную фигуру,
    размещаем ее и повернутую на 180 градусов
    рядом
    """
    fs = flip_x(f)
    return union(fs, rot_90(rot_90(fs)))


@app.cell
def _(fish):
    # тестируем two_side_by_side
    draw(two_side_by_side(fish))
    return


@app.cell
def _():
    mo.md(r"""
    Делаем то же с другими фигурами
    """)
    return


@app.cell
def _(G, fish, fish_outline, triangle):
    _fig = draw(
        two_side_by_side(fish),
        two_side_by_side(fish_outline),
        two_side_by_side(triangle),
        two_side_by_side(G),
        ncols=4,
        axis=False,
        figsize=(12, 3),
    )
    # plt.savefig('07_17.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _():
    mo.md(r"""
    ## Компонуем четыре фигуры из одной, но уменьшенной фигуры
    Функция для уменьшенной и повернутой фигуры
    """)
    return


@app.function
def small_figure(f):
    """
    Уменьшенная повернутая фигура
    """
    return flip_y(rot_45(f))


@app.cell
def _(fish_outline):
    # Тестируем уменьшенную повернутую фигуру
    draw(small_figure(fish_outline))
    return


@app.cell
def _(G, fish, fish_outline, triangle):
    # четыре уменьшенных порождающие фигуры
    _fig = draw(
        small_figure(fish),
        small_figure(fish_outline),
        small_figure(triangle),
        small_figure(G),
        ncols=4,
        axis=False,
        figsize=(12, 3),
    )
    # plt.savefig('07_18.png', dpi=300, facecolor='white')
    _fig
    return


@app.function
def four_small_figures(f):
    """
    Компонуем четыре маленьких фигурки
    """
    sm = small_figure(f)
    return union(
        sm, rot_90(sm), rot_90(rot_90(sm)), rot_90(rot_90(rot_90(sm)))
    )


@app.cell
def _():
    mo.md(r"""
    Делаем четыре маленьких фигурки из всех исходных фигур
    """)
    return


@app.cell
def _(G, fish, fish_outline, triangle):
    _fig = draw(
        four_small_figures(fish),
        four_small_figures(fish_outline),
        four_small_figures(triangle),
        four_small_figures(G),
        ncols=4,
        axis=False,
        figsize=(12, 3),
    )
    # plt.savefig('07_19.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _():
    mo.md(r"""
    ### Компоновка фигуры с двумя маленькими фигурами
    """)
    return


@app.function
def figure_two_small_figures(f):
    # компоновка фигуры с двумя маленькими фигурами
    sm = small_figure(f)
    return union(f, sm, rot_90(rot_90(rot_90(sm))))


@app.cell
def _(G, fish, fish_outline, triangle):
    _fig = draw(
        figure_two_small_figures(fish),
        figure_two_small_figures(fish_outline),
        figure_two_small_figures(triangle),
        figure_two_small_figures(G),
        ncols=4,
        axis=False,
        figsize=(12, 3),
    )
    # plt.savefig('07_20.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _():
    mo.md(r"""
    ### Рисуем основную часть
    """)
    return


@app.function
def side(n, t):
    """
    Рисуем основную часть с помощью рекурсии
    """
    if n == 0:
        return get_blank()
    else:
        return four(side(n - 1, t), side(n - 1, t), rot_90(t), t)


@app.cell
def _(fish):
    draw(side(2, figure_two_small_figures(fish)))
    return


@app.cell
def _(fish):
    # тестируем figure_two_small_figures
    draw(
        side(1, figure_two_small_figures(fish)),
        side(2, figure_two_small_figures(fish)),
        side(3, figure_two_small_figures(fish)),
        side(4, figure_two_small_figures(fish)),
        ncols=4,
        axis=False,
        figsize=(12, 3),
    )
    return


@app.cell
def _(fish_outline):
    # тестируем figure_two_small_figures
    draw(
        side(1, figure_two_small_figures(fish_outline)),
        side(2, figure_two_small_figures(fish_outline)),
        side(3, figure_two_small_figures(fish_outline)),
        side(4, figure_two_small_figures(fish_outline)),
        ncols=4,
        axis=False,
        figsize=(12, 3),
    )
    return


@app.cell
def _(triangle):
    # тестируем figure_two_small_figures
    _fig = draw(
        side(1, figure_two_small_figures(triangle)),
        side(2, figure_two_small_figures(triangle)),
        side(3, figure_two_small_figures(triangle)),
        side(4, figure_two_small_figures(triangle)),
        ncols=4,
        axis=False,
        figsize=(12, 3),
    )
    # plt.savefig('07_21.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(G):
    # тестируем figure_two_small_figures
    draw(
        side(1, figure_two_small_figures(G)),
        side(2, figure_two_small_figures(G)),
        side(3, figure_two_small_figures(G)),
        side(4, figure_two_small_figures(G)),
        ncols=4,
        axis=False,
        figsize=(12, 3),
    )
    return


@app.cell
def _():
    mo.md(r"""
    ### Рисуем уголок
    Нам нужно определить две функции
    """)
    return


@app.function
def corner(n, t, u):
    """
    Рекурсивное определение уголка
    """
    if n == 0:
        return get_blank()
    else:
        return four(
            corner(n - 1, u, t), side(n - 1, t), rot_90(side(n - 1, t)), u
        )


@app.function
def f_corner(n, f):
    """
    Рисуем уголок из одной фигуры
    """
    f3 = figure_two_small_figures(f)
    f4 = four_small_figures(f)
    return corner(n, f3, f4)


@app.cell
def _(fish):
    # тестируем уголок
    draw(
        f_corner(1, fish),
        f_corner(2, fish),
        f_corner(3, fish),
        f_corner(4, fish),
        ncols=4,
        axis=False,
        figsize=(12, 3),
    )
    return


@app.cell
def _(fish_outline):
    # тестируем уголок
    draw(
        f_corner(1, fish_outline),
        f_corner(2, fish_outline),
        f_corner(3, fish_outline),
        f_corner(4, fish_outline),
        ncols=4,
        axis=False,
        figsize=(12, 3),
    )
    return


@app.cell
def _(triangle):
    # тестируем уголок
    _fig = draw(
        f_corner(1, triangle),
        f_corner(2, triangle),
        f_corner(3, triangle),
        f_corner(4, triangle),
        ncols=4,
        axis=False,
        figsize=(12, 3),
    )
    # plt.savefig('07_22.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(G):
    # тестируем уголок
    draw(
        f_corner(1, G),
        f_corner(2, G),
        f_corner(3, G),
        f_corner(4, G),
        ncols=4,
        axis=False,
        figsize=(12, 3),
    )
    return


@app.cell
def _():
    mo.md(r"""
    ### Теперь можно сконстрировать квадратный предел из произвольной фигуры
    """)
    return


@app.function
def f_square_limit(n, f):
    """
    Рекурсивно конструируем квадратный предел
    n - уровень рекурсиии
    f - порождающая фигура
    """
    t = figure_two_small_figures(f)
    u = four_small_figures(f)

    return nine(
        corner(n, t, u),
        side(n, t),
        rot_90(rot_90(rot_90(corner(n, t, u)))),
        rot_90(side(n, t)),
        u,
        rot_90(rot_90(rot_90(side(n, t)))),
        rot_90(corner(n, t, u)),
        rot_90(rot_90(side(n, t))),
        rot_90(rot_90(corner(n, t, u))),
    )


@app.cell
def _(fish):
    # тестируем квадратный предел
    _fig = draw(
        f_square_limit(0, fish),
        f_square_limit(1, fish),
        f_square_limit(2, fish),
        f_square_limit(3, fish),
        f_square_limit(4, fish),
        ncols=5,
        axis=False,
        figsize=(15, 3),
    )
    # plt.savefig('fish_0_4.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(fish_outline):
    # тестируем квадратный предел
    _fig = draw(
        f_square_limit(0, fish_outline),
        f_square_limit(1, fish_outline),
        f_square_limit(2, fish_outline),
        f_square_limit(3, fish_outline),
        f_square_limit(4, fish_outline),
        ncols=5,
        axis=False,
        figsize=(15, 3),
    )
    # plt.savefig('fish__outline_0_4.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(triangle):
    # тестируем квадратный предел
    _fig = draw(
        f_square_limit(0, triangle),
        f_square_limit(1, triangle),
        f_square_limit(2, triangle),
        f_square_limit(3, triangle),
        f_square_limit(4, triangle),
        ncols=5,
        axis=False,
        figsize=(15, 3),
    )
    # plt.savefig('07_23.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(G):
    # тестируем квадратный предел
    _fig = draw(
        f_square_limit(0, G),
        f_square_limit(1, G),
        f_square_limit(2, G),
        f_square_limit(3, G),
        f_square_limit(4, G),
        ncols=5,
        axis=False,
        figsize=(15, 3),
    )
    # plt.savefig('07_24.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _():
    mo.md(r"""
    ### Никто не мешает нам изготовить квадратные пределы из других фигур
    """)
    return


@app.cell
def _(fish_outline):
    _fig = draw(
        f_square_limit(0, fish_outline),
        f_square_limit(1, fish_outline),
        f_square_limit(2, fish_outline),
        f_square_limit(3, fish_outline),
        f_square_limit(4, fish_outline),
        ncols=5,
        axis=False,
        figsize=(15, 3),
    )
    # plt.savefig('fish_outline_0_4.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(triangle):
    draw(
        f_square_limit(1, triangle),
        f_square_limit(2, triangle),
        f_square_limit(3, triangle),
        f_square_limit(4, triangle),
        f_square_limit(5, triangle),
        ncols=5,
        axis=False,
        figsize=(15, 3),
    )
    return


@app.cell
def _(G):
    draw(
        f_square_limit(1, G),
        f_square_limit(2, G),
        f_square_limit(3, G),
        f_square_limit(4, G),
        f_square_limit(5, G),
        ncols=5,
        axis=False,
        figsize=(15, 3),
    )
    return


@app.cell
def _():
    F = get_F()
    _fig = draw(
        f_square_limit(0, F),
        f_square_limit(1, F),
        f_square_limit(2, F),
        f_square_limit(3, F),
        f_square_limit(4, F),
        ncols=5,
        axis=False,
        figsize=(15, 3),
    )
    # plt.savefig('F_0_4.png', dpi=300, facecolor="white")
    _fig
    return (F,)


@app.cell
def _():
    mo.md(r"""
    ## Изготовим теперь большие рисунки квадратных пределов
    """)
    return


@app.cell
def _(fish):
    _fig = draw(
        f_square_limit(4, fish), ncols=1, box=False, axis=False, figsize=(12, 12)
    )
    # plt.savefig('fish__filled.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(fish):
    _fig = draw(
        f_square_limit(4, fish),
        ncols=1,
        box=False,
        axis=False,
        figsize=(12, 12),
        fill=True,
    )
    # plt.savefig('fish_filled.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(fish_outline):
    _fig = draw(
        f_square_limit(5, fish_outline),
        ncols=1,
        box=False,
        axis=False,
        figsize=(12, 12),
        fill=False,
    )
    # plt.savefig('fish_outline.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(fish_outline):
    _fig = draw(
        f_square_limit(5, fish_outline),
        ncols=1,
        box=False,
        axis=False,
        figsize=(12, 12),
        fill=True,
    )
    # plt.savefig('fish_outline_filled.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(F):
    draw(
        f_square_limit(5, F),
        ncols=1,
        box=False,
        axis=False,
        figsize=(12, 12),
        fill=False,
    )
    return


@app.cell
def _(F):
    _fig = draw(
        f_square_limit(6, F),
        ncols=1,
        box=False,
        axis=False,
        figsize=(12, 12),
        fill=True,
    )
    # plt.savefig('F_5.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _():
    _F = flip_y(flip_x(get_F()))
    _fig = draw(
        f_square_limit(6, _F),
        ncols=1,
        box=False,
        axis=False,
        figsize=(12, 12),
        fill=True,
    )
    # plt.savefig('F_5_y_x.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _():
    mo.md(r"""
    ## Изготовим теперь набор Квадратных пределов из всех порождающих фигур
    """)
    return


@app.cell
def _(G, fish, fish_outline, triangle):
    _F = flip_y(flip_x(get_F()))
    square_limits = (
        f_square_limit(4, fish),
        f_square_limit(4, fish_outline),
        f_square_limit(5, triangle),
        f_square_limit(5, G),
        # f_square_limit(5, _F)
    )
    return (square_limits,)


@app.cell
def _(square_limits):
    _fig = draw(
        *square_limits,
        ncols=2,
        nrows=2,
        box=False,
        axis=False,
        figsize=(12, 12),
        fill=False,
    )
    # plt.savefig('07_24.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(square_limits):
    # рисуем с закраской
    _fig = draw(
        *square_limits,
        ncols=2,
        nrows=2,
        box=False,
        axis=False,
        figsize=(12, 12),
        fill=True,
    )
    # plt.savefig('07_25.png', dpi=300, facecolor="white")
    _fig
    return


if __name__ == "__main__":
    app.run()
