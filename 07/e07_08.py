import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from e07_05 import draw, get_F, get_fish, get_fish_outline
    from e07_05 import get_G, get_triangle, flip_x, flip_y
    from e07_07 import f_square_limit

    mo.md(r"""
    # Преобразуем Квадратный предел в Круглый предел
    Для этого на понадобится преобразование из статьи

    Fong С. Analytical Methods for Squaring the Disc. [Электронный ресурс]. URL: 
    https://arxiv.org/ftp/arxiv/papers/1509/1509.06344.pdf (дата обращения 01.05.2025)

    Мы рассмотрим отображение квадрата с центром в точке (0, 0) и длиной стороны равной двум на круг
    единичного радиуса с центром в точке (0, 0).

    Отображение $(x, y)->(u, v)$ описывается формулами:

    $$ u=sign(x) \frac{x^2} {\sqrt{x^2+y^2}},\  для \ x^2 \  \geq y^2, \tag{1} $$

    $$ u=sign(y) \frac{x \cdot y} {\sqrt{x^2+y^2}},\  для \ x^2 \  < y^2, \tag{2} $$

    $$ v=sign(x) \frac{x \cdot y} {\sqrt{x^2+y^2}},\  для \ x^2 \ \geq  y^2, \tag{3} $$

    $$ v=sign(y) \frac{y^2} {\sqrt{x^2+y^2}},\  для \ x^2 \  < y^2, \tag{4} $$
    """)
    return (
        draw,
        f_square_limit,
        flip_x,
        get_G,
        get_fish,
        get_fish_outline,
        get_triangle,
        mo,
        np,
        plt,
    )


@app.cell
def _(np):
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

    return (square_2_circle,)


@app.cell
def _(np, plt, square_2_circle):
    # тестируем преобразование
    n = 50
    x = np.linspace(0, 1, n + 1)
    u, v = square_2_circle(x, x)
    X, Y = np.meshgrid(x, x)
    _fig, axs = plt.subplots(ncols=2, nrows=1, figsize=(12, 6))

    for _ in range(n + 1):
        axs[0].plot(X[_, :], Y[_, :], "k-", lw=0.5)
        axs[0].plot(X[:, _], Y[:, _], "k-", lw=0.5)
    # axs[0].axis('off')
    axs[0].set_xlabel("x")
    axs[0].set_ylabel("y")

    for _ in range(n + 1):
        _U, _V = square_2_circle(X[_, :], Y[_, :])
        _W, _Z = square_2_circle(X[:, _], Y[:, _])
        axs[1].plot(_U, _V, "k-", lw=0.5)
        axs[1].plot(_W, _Z, "k-", lw=0.5)

    # plt.axis('off')
    axs[1].set_xlabel("u")
    axs[1].set_ylabel("v")
    plt.tight_layout()
    # plt.savefig('07_26.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Рассчитывем круглый предел
    """)
    return


@app.cell
def _(f_square_limit, square_2_circle):
    def circle_limit(f, n):
        """
        Отображение квадратного предела,
        порожденного фигурой f
        с уровнем рекурсии n
        на окружность
        """
        s = f_square_limit(f=f, n=n)
        x, y = s.vertices[:, 0], s.vertices[:, 1]
        u, v = square_2_circle(x, y)
        s.vertices[:, 0], s.vertices[:, 1] = u, v
        return s

    return (circle_limit,)


@app.cell
def _(draw, flip_x, get_G, get_fish, get_fish_outline, get_triangle):
    # Порождающие фигуры
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


@app.cell
def _(G, circle_limit, fish, fish_outline, triangle):
    # Преобразуем квадратные пределы в круглые
    # для раздичных порождающих фигур
    сircle_fish = circle_limit(fish, 3)
    сircle_fish_outline = circle_limit(fish_outline, 4)
    circle_triangle = circle_limit(triangle, 5)
    circle_G = circle_limit(G, 5)
    return circle_G, circle_triangle, сircle_fish, сircle_fish_outline


@app.cell
def _(draw, сircle_fish):
    draw(сircle_fish, axis=False, fill=True, box=False, figsize=(6, 6))
    return


@app.cell
def _(draw, сircle_fish_outline):
    draw(сircle_fish_outline, axis=False, fill=True, box=False, figsize=(6, 6))
    return


@app.cell
def _(circle_triangle, draw):
    draw(circle_triangle, axis=False, fill=True, box=False, figsize=(6, 6))
    return


@app.cell
def _(circle_G, draw):
    draw(circle_G, axis=False, fill=True, box=False, figsize=(6, 6))
    # _n = 5
    # _f = flip_x(get_F())
    # _sl = f_square_limit(f=_f, n=_n)
    # _sc = circle_limit(_f, _n)
    # draw(_sl,_sc, axis=False, fill=True, box=False,
    #     ncols=2, figsize=(8, 4))
    return


@app.cell
def _(circle_G, circle_triangle, draw, сircle_fish, сircle_fish_outline):
    # рисуем круглые пределы на одном рисунке
    _fig = draw(
        сircle_fish,
        сircle_fish_outline,
        circle_triangle,
        circle_G,
        axis=False,
        fill=True,
        box=False,
        ncols=2,
        nrows=2,
        figsize=(12, 12),
    )
    # plt.savefig('07_27.png', dpi=300, facecolor="white")
    _fig
    return


if __name__ == "__main__":
    app.run()
