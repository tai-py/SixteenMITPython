import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium", layout_file="layouts/a02_14.grid.json")


@app.cell
def _():
    import marimo as mo

    mo.md("# Запускаем приложение по нажатию кнопки").center()
    return (mo,)


@app.cell
def _():
    # трилистник - трехмерная кривая и поверхность
    import numpy as np
    import matplotlib.pyplot as plt

    def trefoil(u, v, r):
        x = r * np.sin(3 * u) / (2 + np.cos(v))

        y = r * (np.sin(u) + 2 * np.sin(2 * u)) / \
        (2 + np.cos(v + np.pi * 2 / 3))

        z = r / 2 * (np.cos(u) - 2 * np.cos(2 * u)) * \
        (2 + np.cos(v)) * (2 + np.cos(v + np.pi * 2 / 3)) / 4
        return np.array([x, y, z], dtype=np.float64)


    def trefoil_curve_surface(n=300, rmin=-1, rmax=3, wmax=5):

        r = (rmin*np.pi, rmax*np.pi)

        i = np.linspace(r[0], r[1], n)

        # поверхность
        U, V = np.meshgrid(i, i)
        W = trefoil(U, V, wmax)
        S = np.swapaxes(W, 0, 2)
        xs, ys, zs = S[:, :,0], S[:, :,1], S[:, :,2]

        # кривая
        T =  trefoil(i, i, 5) 
        xc, yc, zc = T[0], T[1], T[2]

        return  xc, yc, zc, xs, ys, zs 

    def plot(f=trefoil_curve_surface, argc=(), figsize=(4,3), 
             axis=True, azim=-60,elev=30, roll=0):
        # рисуем трехмерную книвую
        xc, yc, zc, *rest = f(*argc)
        fig = plt.figure(figsize=(5,6))
        ax = plt.axes(projection='3d')
        ax.plot(xc, yc, zc, linewidth=5, color="black")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_xlim(np.min(xc), np.max(xc))
        ax.set_ylim(np.min(yc), np.max(yc))
        ax.set_zlim(np.min(zc), np.max(zc))
        if axis:
            ax.axis("on")
        else:
            ax.axis("off")
        # повороты
        az = ax.azim if azim is None else azim
        el = ax.elev if elev is None else elev
        rl = ax.roll if roll is None else roll
        ax.view_init(azim=az, elev=el, roll=rl)
        plt.tight_layout()
        return fig

    # mo.md("## Подготавливаем функции для вращения трехмерной кривой трилистника")
    return (plot,)


@app.cell
def _(mo):
    # Создаем элементы пользовательского интерфейса
    azim0, elev0, roll0 = -60, 30, 0 
    title = mo.md("# Вращаем трилистник по нажатию кнопки").center()
    azim = mo.ui.slider(label="Ось Z:", start=-180, stop=180, 
                        debounce=True,
                        step=5, value=azim0, full_width=False)
    elev = mo.ui.slider(label="Ось X:", start=-180, stop=180,
                        debounce=True,
                        step=5, value=elev0, full_width=False)
    roll = mo.ui.slider(label="Ось Y:", start=-180, stop=180, 
                        debounce=True,
                        step=5, value=roll0, full_width=False)
    axis = mo.ui.switch(label="Оси координат", value=True)

    title
    return axis, azim, azim0, elev, elev0, roll, roll0


@app.cell
def _(azim0, elev0, mo, plot, roll0):
    # состояние для рисунка
    fig_get, fig_set = mo.state(plot(azim=azim0,elev=elev0, roll=roll0))
    return fig_get, fig_set


@app.cell
def _(axis, azim, elev, mo, roll):
    # верстка слайдеров и переключателя
    sliders_switch =   mo.vstack([mo.hstack([azim, mo.md(f'${azim.value}^o$')],
                                 justify="start"), 
                       mo.hstack([roll, mo.md(f'${roll.value}^o$')],
                                justify="start"), 
                       mo.hstack([elev, mo.md(f'${elev.value}^o$')],
                                justify="start"), 
                       axis
    ]) 
    sliders_switch
    return


@app.cell
def _(mo):
    # кнопка запуска
    run_button = mo.ui.run_button(label="Запустить")
    run_button.center()
    return (run_button,)


@app.cell
def _(axis, azim, elev, fig_get, fig_set, mo, plot, roll, run_button):
    # реагируем на нажатие кнопки
    mo.stop(not run_button.value, fig_get()) # кнопка не нажата
    # кнопка нажата, одновляем и отображаем картинку
    fig = plot(axis=axis.value, azim=azim.value,
               elev=elev.value, roll=roll.value)
    fig_set(fig)
    fig
    return


if __name__ == "__main__":
    app.run()
