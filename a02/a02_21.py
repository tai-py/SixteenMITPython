import marimo

__generated_with = "0.10.15"
app = marimo.App(
    width="full",
    layout_file="layouts/three_d_example.slides.json",
)


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from trefoil import trefoil_curve_surface
    from mebius import mebius_curve_surface
    from thor import thor_curve_surface
    from visualize3d import visualize3d_curve, visualize3d_surface

    # данные для рисования кривых и поверхностей
    xct, yct, zct, xst, yst, zst = trefoil_curve_surface()  # трилистник
    # данные для рисования кривых и поверхностей
    xcm, ycm, zcm, xsm, ysm, zsm = mebius_curve_surface()  # лента Мёбиуса
    # данные для рисования кривых и поверхностей
    xcr, ycr, zcr, xsr, ysr, zsr = thor_curve_surface()  # тор


    def figure_selection(figure):
        title = mo.md("# " + figure)
        if figure == "Трилистник":
            return xct, yct, zct, xst, yst, zst, title
        elif figure == "Мёбиус":
            return xcm, ycm, zcm, xsm, ysm, zsm, title
        else:
            return xcr, ycr, zcr, xsr, ysr, zsr, title


    mo.md("# Рисуем кривые и поверхности в `3d`").center()
    return (
        figure_selection,
        mebius_curve_surface,
        mo,
        np,
        plt,
        thor_curve_surface,
        trefoil_curve_surface,
        visualize3d_curve,
        visualize3d_surface,
        xcm,
        xcr,
        xct,
        xsm,
        xsr,
        xst,
        ycm,
        ycr,
        yct,
        ysm,
        ysr,
        yst,
        zcm,
        zcr,
        zct,
        zsm,
        zsr,
        zst,
    )


@app.cell
def _(mo):
    # элементы пользовательского интерфейса
    label_figure = mo.md("**Выбор фигуры**")
    fig_form = mo.ui.dropdown(
        options=("Трилистник", "Мёбиус", "Тор"), value="Трилистник"
    )
    # повороты рисунка вокруг координатных осей
    label_axis = mo.md("**Поворот вокруг оси**")

    azim = mo.ui.slider(
        start=-180,
        stop=180,
        step=10,
        value=-60,
        debounce=True,
        full_width=False,
        label="z",
    )
    elev = mo.ui.slider(
        start=-180,
        stop=180,
        step=10,
        value=30,
        debounce=True,
        full_width=False,
        label="y",
    )
    roll = mo.ui.slider(
        start=-180,
        stop=180,
        step=10,
        value=0,
        debounce=True,
        full_width=False,
        label="x",
    )
    label_parameters = mo.md("**Цвета, оцифровка, сетка**")
    cmap = mo.ui.dropdown(
        options=[
            "rainbow",
            "jet",
            "Spectral",
            "BuPu",
            "summer",
            "autumn",
            "winter",
            "Paired",
            "binary",
        ],
        value="rainbow",
        label="палитра:",
        allow_select_none=True,
    )
    axis2 = mo.ui.checkbox(value=True, label="оцифровка")
    axis = mo.ui.switch(value=True, label="оцифровка")
    stride = mo.ui.slider(
        steps=(0, 20, 25, 40, 50, 100), value=25, label="шаг сетки"
    )
    # label_axis, azim, elev, roll, cmap, axis, stride
    return (
        axis,
        axis2,
        azim,
        cmap,
        elev,
        fig_form,
        label_axis,
        label_figure,
        label_parameters,
        roll,
        stride,
    )


@app.cell
def _(
    axis,
    azim,
    cmap,
    elev,
    fig_form,
    figure_selection,
    roll,
    stride,
    visualize3d_curve,
    visualize3d_surface,
):
    figsize = (8, 7)
    xc, yc, zc, xs, ys, zs, title = figure_selection(fig_form.value)
    figc = visualize3d_curve(
        xc,
        yc,
        zc,
        axis=axis.value,
        azim=azim.value,
        elev=elev.value,
        roll=roll.value,
        figsize=figsize,
    )
    figs = visualize3d_surface(
        xs,
        ys,
        zs,
        cmap=cmap.value,
        axis=axis.value,
        azim=azim.value,
        elev=elev.value,
        roll=roll.value,
        stride=stride.value,
        figsize=figsize,
    )
    return figc, figs, figsize, title, xc, xs, yc, ys, zc, zs


@app.cell
def _(
    axis,
    azim,
    cmap,
    elev,
    fig_form,
    figc,
    figs,
    label_axis,
    label_figure,
    label_parameters,
    mo,
    roll,
    stride,
    title,
):
    mo.vstack(
        [
            title.center(),
            mo.hstack(
                [
                    mo.vstack(
                        [
                            label_figure,
                            fig_form,
                            label_axis,
                            azim,
                            elev,
                            roll,
                            label_parameters,
                            cmap,
                            axis,
                            stride,
                        ]
                    ),
                    figc,
                    figs,
                ]
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
