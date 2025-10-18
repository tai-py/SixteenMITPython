import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    from affine import draw_contour
    from affine import affine_transformation
    from affine import composition

    mo.md("# Рисуем и прeобразуем заглавную букву Г")
    return affine_transformation, composition, draw_contour, mo, np


@app.cell
def _(draw_contour, np):
    # координаты контура Г
    x = np.array([0.0, 0.0, 0.7, 0.7, 0.1, 0.1, 0])
    y = np.array([0.0, 1.0, 1.0, 0.9, 0.9, 0.0, 0])

    # тестируем рисование контура
    draw_contour(x, y, axis=True)
    return x, y


@app.cell
def _(mo):
    mo.md("""## Афинные преобразования""")
    return


@app.cell
def _(affine_transformation, x, y):
    # тестируем аффинные преобразования

    affine_transformation(1.0, 2), affine_transformation(x, y)
    return


@app.cell
def _(affine_transformation, draw_contour, np, x, y):
    # исходная буква Г
    fig = draw_contour(x, y, figsize=(8, 3), fig=None, axis=True)

    # трансляция
    xyt = affine_transformation(x, y, np.array([[1.0, 0.0, 1.5], [0.0, 1.0, 1]]))
    draw_contour(xyt[0], xyt[1], fig=fig, axis=True)

    # изменение масштаба c одновременной трансляцией
    kx, ky = 2.0, 0.5
    xyk = affine_transformation(x, y, np.array([[kx, 0.0, 2.5], [0.0, ky, 0]]))
    draw_contour(xyk[0], xyk[1], fig=fig, axis=True)

    # поворот вокруг оси в точке (0, 0) по часовой стрелке
    angle = 60 * np.pi / 180  # угол поворота в радианах
    cos60, sin60 = np.cos(angle), np.sin(angle)
    xyr = affine_transformation(
        x, y, np.array([[cos60, sin60, 0.0], [-sin60, cos60, 0]])
    )
    draw_contour(xyr[0], xyr[1], fig=fig, axis=True)

    # поворот вокруг оси в точке (0, 0) против часовой стрелке
    xyr2 = affine_transformation(
        x, y, np.array([[cos60, -sin60, 0.0], [sin60, cos60, 0]])
    )
    draw_contour(xyr2[0], xyr2[1], fig=fig, axis=True)

    # зеркальное отражение относительно оси ординат (x=0)
    xyv = affine_transformation(x, y, np.array([[1.0, 0.0, 0.0], [0.0, -1.0, 0]]))
    draw_contour(xyv[0], xyv[1], fig=fig, axis=True)

    # зеркальное отражение относительно оси абсцисс (y=0)
    xyh = affine_transformation(x, y, np.array([[-1.0, 0.0, 0.0], [0.0, 1.0, 0]]))
    draw_contour(xyh[0], xyh[1], fig=fig, axis=True)

    # композиция отображений, одновременное отражение относительно осей абсцисс и ординат
    xyhv = affine_transformation(
        x, y, np.array([[-1.0, 0.0, 0.0], [0.0, -1.0, 0]])
    )
    draw_contour(xyhv[0], xyhv[1], fig=fig, axis=True)

    fig
    return


@app.cell
def _(mo):
    mo.md("""### Композиция отображений""")
    return


@app.cell
def _(affine_transformation, composition, draw_contour, np, x, y):
    # тестируем композицию отображений
    scale_trans = composition(
        np.array([[2.0, 0.0, 0.0], [0.0, 0.5, 0.0]]),
        np.array([[1.0, 0.0, 2.0], [0.0, 1.0, 3.0]]),
    )
    trans_scale = composition(
        np.array([[1.0, 0.0, 2.0], [0.0, 1.0, 3.0]]),
        np.array([[2.0, 0.0, 0.0], [0.0, 0.5, 0.0]]),
    )

    # исходная буква Г
    fig_ts = draw_contour(x, y, figsize=(8, 3), fig=None, axis=True)

    xy_st = affine_transformation(x, y, scale_trans)
    draw_contour(xy_st[0], xy_st[1], fig=fig_ts, axis=True)

    xy_ts = affine_transformation(x, y, trans_scale)
    draw_contour(xy_ts[0], xy_ts[1], fig=fig_ts, axis=True)
    return


@app.cell
def _(mo, np):
    angle30 = 30 * np.pi / 180
    cos30, sin30 = np.cos(angle30), np.sin(angle30)
    rot30 = np.array([[cos30, sin30, 0], [-sin30, cos30, 0]])

    tr = 1.5
    trx = np.array([[1.0, 0, tr], [0.0, 1.0, 0.0]])
    flip_x = np.array([[1.0, 0.0, 0.0], [0.0, -1.0, 0.0]])
    flip_y = np.array([[-1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    mo.md("### Подготавливем преобразования")
    return flip_x, flip_y, rot30, trx


@app.cell
def _(mo):
    mo.md("""### Результат композиции преобразований зависит от их порядка""")
    return


@app.cell
def _(
    affine_transformation,
    composition,
    draw_contour,
    flip_x,
    flip_y,
    rot30,
    trx,
    x,
    y,
):
    fig_c = draw_contour(x, y, figsize=(8, 3), fig=None, axis=True)

    tr1 = composition(trx, rot30)
    xy1 = affine_transformation(x, y, tr1)
    draw_contour(xy1[0], xy1[1], fig=fig_c, axis=True)

    tr2 = composition(trx, trx, rot30, flip_x)
    xy2 = affine_transformation(x, y, tr2)
    draw_contour(xy2[0], xy2[1], fig=fig_c, axis=True)

    tr3 = composition(trx, trx, trx, rot30, rot30, flip_x, flip_y)
    xy3 = affine_transformation(x, y, tr3)
    draw_contour(xy3[0], xy3[1], fig=fig_c, axis=True)

    tr4 = composition(
        trx, trx, trx, trx, rot30, flip_y, flip_x, rot30, rot30, rot30
    )
    xy4 = affine_transformation(x, y, tr4)
    draw_contour(xy4[0], xy4[1], fig=fig_c, axis=True)

    # выполняем преобразование tr4 в обратном порядке
    tr5 = composition(rot30, rot30, rot30, flip_x, flip_y, rot30, trx, trx, trx,trx)
    xy5 = affine_transformation(x, y, tr5)
    draw_contour(xy5[0], xy5[1], fig=fig_c, axis=True)

    fig_c
    return


if __name__ == "__main__":
    app.run()
