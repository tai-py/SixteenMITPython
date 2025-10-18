import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from e07_05 import draw, union, translate, rot_90, rotate_deg_around
    from e07_05 import flip_x, flip_y, rot_45
    from e07_05 import get_blank, get_F, get_fish, get_fish_outline
    from e07_05 import get_G, get_triangle

    mo.md("# Складываем простые мозаики")
    return (
        draw,
        flip_x,
        flip_y,
        get_F,
        get_fish,
        get_fish_outline,
        get_triangle,
        plt,
        translate,
        union,
    )


@app.cell
def _(translate, union):
    def tiles(f, transform=lambda f, i, j: f,
              nrows=4, ncols=4):
        '''
        Складываем простую мозаику
        f - функция для получения элемента мозаики с шириной и высотой 1
        transform - преобразование, применяемое к 
                    элементу мозаики
        nrows, ncols - число рядов и столбцов мозаики
        '''
        result = None
        for i in range(nrows):
            for j in range(ncols):
                if i==0 and j==0: # инициализация мозаики
                    el = f()
                    result = el
                else: 
                    _f =transform(f, i, j)
                    el = translate(_f, i, j)
                    result = union(result, el) # сборка            
        return result
    return (tiles,)


@app.cell
def _(draw, flip_x, flip_y, get_fish, tiles):
    def _t(f, i, j):
        _f = f() 
        if i%2:
            _f = flip_x(_f) 
        if j%2:
            _f = flip_y(_f)
        return _f

    draw(tiles(get_fish, transform=_t, ncols=8, nrows=8),
        axis=False, equal=True, box=False, fill=True,
        figsize=(6, 6) 
        )
    return


@app.cell
def _(flip_x, flip_y, get_fish, tiles):
    def _t(f, i, j):
        _f = f() 
        #_f = flip_x(_f)
        if i%2:
            _f = flip_x(_f) 
        if j%2==0:
            _f = flip_y(_f)
        return _f

    t1 = tiles(get_fish, transform=_t, ncols=8, nrows=8)
    return (t1,)


@app.cell
def _(flip_x, flip_y, get_fish, tiles):
    def _t(f, i, j):
        _f = f() 
        if i%2:
            _f = flip_y(_f) 
        if j%2:
            _f = flip_x(_f)
        return _f

    t2=tiles(get_fish, transform=_t, ncols=8, nrows=8)
    return (t2,)


@app.cell
def _(flip_x, flip_y, get_fish_outline, tiles):
    def _t(f, i, j):
        _f = f() 
        if i%2:
            _f = flip_x(_f) 
        if j%2:
            _f = flip_y(_f)
        return _f

    t3= tiles(get_fish_outline, transform=_t, ncols=8, nrows=8)
    return (t3,)


@app.cell
def _(flip_x, flip_y, get_fish_outline, tiles):
    def _t(f, i, j):
        _f = f() 
        if i%2:
            _f = flip_y(_f) 
        if j%2:
            _f = flip_x(_f)
        return _f

    t4=tiles(get_fish_outline, transform=_t, ncols=8, nrows=8)
    return (t4,)


@app.cell
def _(flip_x, flip_y, get_F, tiles):
    def _t(f, i, j):
        _f = f()   
        if i%2:
            _f = flip_y(_f) 
        if j%2:
            _f = flip_x(_f)
        return _f

    t5 = tiles(get_F, transform=_t, ncols=8, nrows=8)
    return (t5,)


@app.cell
def _(flip_x, flip_y, get_triangle, tiles):
    def _t(f, i, j):
        _f = f()
        #_f = flip_y(_f)
        if i%2:
            _f = flip_y(_f) 
        if j%2:
            _f = flip_x(_f)
        return _f

    t6 = tiles(get_triangle, transform=_t, ncols=8, nrows=8)
    return (t6,)


@app.cell
def _(draw, plt, t1, t2, t3, t4, t5, t6):
    _fig = draw(t1, t2, t3, t4,t5, t6,     
         axis=False, equal=True, box=False,
         figsize=(15,12), ncols=3, nrows=2, fill=True
        )
    plt.savefig('Э_15.png', dpi=300, facecolor="white")
    _fig
    return


if __name__ == "__main__":
    app.run()
