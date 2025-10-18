import marimo

__generated_with = "0.12.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    return mo, np, plt


@app.cell
def _(np, plt):
    a0 = 0.5
    astep = 0.05
    xx = np.linspace(0, 5, 600)

    def f1(i):
        fig = plt.figure(figsize=(3, 3))
        yy = np.sinc((a0 + astep * i) * xx)
        plt.plot(xx, yy, lw=3)
        plt.title(f"Кадр:{i + 1}")
        plt.ylim(-0.3, 1.1)
        plt.grid()

    return a0, astep, f1, xx


@app.cell
def _(f1):
    from anim2 import build_gif_animation_py

    build_gif_animation_py(f1, 200)
    return (build_gif_animation_py,)


@app.cell
def _(build_gif_animation_py, np, plt):
    from scipy.signal import convolve  # свертка

    mask = np.array(
        [[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=bool
    )  # окружение ячейки
    nx = 200  # размерность поля
    extended_field = np.zeros((nx + 2, nx + 2))  # расширенное поле
    field = extended_field[1:-1, 1:-1]  # поле игры
    # начальная расстановка
    field[0, :] = field[-1, :] = 1
    field[:, 0] = field[:, -1] = 1


    def step_of_game(i):
        # замыкание на торе
        extended_field[-1, :] = extended_field[1, :]
        extended_field[0, :] = extended_field[-2, :]
        extended_field[:, -1] = extended_field[:, 1]
        extended_field[:, 0] = extended_field[:, -2]
        # число соседей каждой яейки
        c = convolve(extended_field, mask, method="direct", mode="valid")
        # правила рождения и смрти
        birth_confition = (field == 0) & (c == 3)
        dyeing_condition = (field == 1) & ((c < 2) | (c > 3))
        field[birth_confition] = 1
        field[dyeing_condition] = 0

        fig = plt.figure(figsize=(3, 3))
        plt.imshow(extended_field, cmap="binary")
        plt.axis("off")


    build_gif_animation_py(step_of_game, 500, duration=50, 
                        fn="public/life4.gif")
    return convolve, extended_field, field, mask, nx, step_of_game


if __name__ == "__main__":
    app.run()
