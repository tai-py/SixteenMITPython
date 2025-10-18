import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium", layout_file="layouts/e07_04.grid.json")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.path import Path
    from matplotlib.patches import PathPatch, Rectangle
    from matplotlib.transforms import Affine2D as A
    from svgpath2mpl import parse_path
    return PathPatch, mo, parse_path, plt


@app.cell
def _(mo):
    mo.md('''
    # Интерактивный редактор фигур
    ''').center()
    return


@app.cell
def _(mo):
    cmds = mo.ui.text_area(
        "M  0., 0.",
        rows=10,
        debounce=True,
        full_width=True,
        label="Введите последовательность команд: ",
    )
    fsize = mo.ui.number(
        label="Размер: ",
        full_width=True,
        debounce=True,
        value=4,
        start=2,
        stop=12,
        step=0.5,
    )
    axis = mo.ui.checkbox(
        label="Оси     ",
        value=True,    
    )
    fill = mo.ui.checkbox(
        label="Закраска",
        value=False,
    )
    lw = mo.ui.number(
        label="Толщина:", debounce=True, value=1, 
        full_width=True,
        start=0.5, stop=10, step=0.5
    )
    mo.vstack([cmds, axis, fill, fsize, lw])
    return axis, cmds, fill, fsize, lw


@app.cell
def _(mo):
    rbtn = mo.ui.run_button(kind='warn', label="Запустить")
    rbtn
    return (rbtn,)


@app.cell
def _(PathPatch, axis, cmds, fill, fsize, lw, mo, parse_path, plt, rbtn):
    resultb = mo.md("Нажмите кнопку **Запустить**") 
    message = f'{resultb}'
    if rbtn.value:  
        resultb = ''
        ax = None
        try:
            mes =""
            w = fsize.value
            txt = cmds.value        
            path = parse_path(txt)  
            fige, ax = plt.subplots(figsize=(w, w))
            ax = ax.add_patch(PathPatch(path, fill = fill.value, 
                                       linewidth=lw.value)) 
            if not axis.value:
                plt.axis('off')
            resultb = ax
        except Exception as ex:
            mes = f"Ошибка при вводе команд: **{ex}**"
            resultb = mo.md(f"{mes}")        
    resultb
    return


if __name__ == "__main__":
    app.run()
