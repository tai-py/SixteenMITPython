
import numpy as np
import matplotlib.pyplot as plt

def draw_contour(
    x, y, fill="b", axis=False, fig=None, figsize=(3, 3), alpha=0.3, box=True
):
    # создаем, если необходимо объект рисунка
    if fig is None:
        figsize = figsize if figsize else (3, 3)
        fig = plt.figure(figsize=figsize)
    plt.plot(x, y, "k-")
    # print(f"{x=}, {y=}, {fig=}")
    # заполнение внутренности контура
    if fill:
        plt.fill(x, y, fill, alpha=alpha)
    # отключаем отображение осей и оцифровки
    if not axis:
        plt.axis("off")
    # задаем одинаковые масштабы по осям координат
    plt.gca().set_aspect("equal")
    if box:
        # рисуем охватывающий прямоугольник
        xmin, xmax = np.min(x), np.max(x)
        ymin, ymax = np.min(y), np.max(y)
        plt.plot([xmin, xmax], [ymin, ymin], "k--", lw=0.5)
        plt.plot([xmin, xmax], [ymax, ymax], "k--", lw=0.5)
        plt.plot([xmin, xmin], [ymin, ymax], "k--", lw=0.5)
        plt.plot([xmax, xmax], [ymin, ymax], "k--", lw=0.5)
    return fig


def affine_transformation(
    x, y, coeffs=np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
):
    # конструируем матрицу преобразования
    a = np.zeros((3, 3))
    a[:2] = coeffs
    a[-1, -1] = 1.0
    # конструирую массив кооржинат
    x_shape = 1 if isinstance(x, int) or isinstance(x, float) else x.shape[0]
    xy = np.ones((3, x_shape))
    xy[0, :] = x
    xy[1, :] = y
    # выполняю преобразование
    r = a @ xy
    return r[:-1]


def composition(*coefs):
    nc = len(coefs)  # число отображений
    c = np.ones((3, 3))  # заготовка резкльтрующего отображения
    c[:-1] = coefs[0]
    c[-1, :-1] = 0.0
    # print(f"начальное \n{c=}")
    for _ in range(1, nc):
        # формирую очередную полную матрицу преобразования
        cx = np.ones((3, 3))
        cx[:-1] = coefs[_]
        cx[-1, :-1] = 0.0
        # print(f"{cx=}")
        # собственно композиция осуществляется умножением матриц
        c = c @ cx
        # print(f"{c[:-1]=}, \n {type(c[:-1])=}")
    return c[:-1]