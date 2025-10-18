import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.path import Path
    from matplotlib.patches import PathPatch, Rectangle
    from svgpath2mpl import parse_path
    from matplotlib.transforms import Affine2D as T

    mo.md('# Рисуем фигуры, состоящие из отрезков  прямых и кривых Безье средствами matplotlib')
    return PathPatch, parse_path, plt


@app.cell
def _():
    # ячейка 1
    curve='''
    M 1.,1.
    C 0.78,0.95 0.78,0.95 0.58,0.97
    C 0.38,0.80 0.38,0.80 0.25,0.73
    L 0.,1.
    '''
    return (curve,)


@app.cell
def _(curve, parse_path):
    # ячейка 2
    curve_path = parse_path(curve)
    curve_path
    return (curve_path,)


@app.cell
def _(curve_path):
    # ячейка 3
    print(f"{curve_path.vertices=}\n{curve_path.codes=}")
    return


@app.cell
def _(PathPatch, curve_path, plt):
    # ячейка 4
    _fig, _ax = plt.subplots(figsize=(3,3))
    _patch = PathPatch(curve_path, fill=True, 
             color="purple", alpha=0.4)
    _ax.add_patch(_patch)
    _ax

    return


if __name__ == "__main__":
    app.run()
