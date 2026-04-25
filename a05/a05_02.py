import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    mo.md("# Изображение енота")
    return


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.datasets import face

    f = face()
    fig1 = plt.figure(figsize=(4,3))
    plt.imshow(f)
    plt.axis('off')
    print(f"{f.shape=}, {f.dtype=}")
    fig1
    return f, face, np, plt


@app.cell
def _(face):
    # Изображение в градациях серого
    fg = face(gray=True)
    print(f"{fg.shape=}, {fg.dtype=}")
    return (fg,)


@app.cell
def _(fg, plt):
    fig2 = plt.figure(figsize=(4,3))
    plt.imshow(fg, cmap='gray')
    plt.axis('off')
    fig2
    return


@app.cell
def _(plt):
    # изображение ascent
    from scipy.datasets import ascent
    asc = ascent()
    fig3 = plt.figure(figsize=(4,3))
    plt.imshow(asc, cmap='gray')
    plt.axis('off')
    print(f"{asc.shape=}, {asc.dtype=}")
    fig3
    return (asc,)


@app.cell
def _(face, plt):
    # четвертушка енота
    fc = face()
    h, w, c = fc.shape
    fig4 = plt.figure(figsize=(3,2))
    plt.imshow(fc[:h//2, w//2:, :])
    fig4
    return (fc,)


@app.cell
def _(fc, plt):
    # прореживаем изображение четвертушки енота
    fig5 = plt.figure(figsize=(4,3))
    plt.imshow(fc[::10, ::10, :])
    fig5
    return


@app.cell
def _(asc, plt):
    # Переворачиваем изображение
    fig6 = plt.figure(figsize=(3,3))
    plt.imshow(asc[::-2, ::-2], cmap='gray')
    fig6
    return


@app.cell
def _(np):
    # Правила укладки
    a1 = np.zeros((2,3))
    a2 = np.zeros((2,4))
    a3 = np.zeros((2,2))
    a4 = np.array([1,2,3])
    a5 = np.array([4,5,6,7])

    a1[:,:] = a4
    a2[:,:] = a5
    a3[:,:] = 42
    a1, a2, a3
    return


@app.cell
def _(np, plt):
    # Рисуем сетку
    mesh = np.ones((501,601))
    mesh[::20, :] = 0 # горизонтальные линии
    mesh[:, ::20] = 0 # вертикальные линии
    fig7 = plt.figure(figsize=(4,3))
    plt.imshow(mesh, cmap='gray')
    plt.axis('off')
    fig7
    return


@app.cell
def _(fg, plt):
    # Черно-белое изображение
    def to_bw(img, threshold=127, 
              figsize=(4,3), axis=False):
        BLACK, WHITE = 0, 255
        img[img>threshold] = WHITE
        img[img<=threshold] = BLACK
        fig = plt.figure() if figsize is None \
              else plt.figure(figsize=figsize)
        plt.imshow(fg, cmap="gray")
        if not axis: plt.axis("off")
        return fig 

    to_bw(fg)

    return


@app.cell
def _(np, plt):
    # функция Хевисайда
    xf = np.linspace(-5, 5, 10000)
    yf = np.heaviside(xf, 1)
    fig8 = plt.figure(figsize=(3,3))
    plt.plot(xf, yf, 'k-', lw=3)
    plt.xlabel('x', fontsize=14)
    plt.ylabel('y = np.heaviside(x, 1)', fontsize=14)
    fig8
    return


@app.cell
def _(np, plt):
    # Функции NumPy
    def numpy_funcs():
        n = 1000
        x = np.linspace(0, 3*np.pi,n) 
        y = np.sin(x)
        fig = plt.figure(figsize=(6,4))
        plt.plot(x, y, 'k-', label='sin(x)', lw=3) 
        plt.plot(x, np.sign(y),'k--', label='sign(sin(x))', lw=3)
        plt.plot(x, np.heaviside(y,0), 'k:',         
                 label='heaviside(sin(x), 0)', lw=3)
        plt.legend() 
        plt.xlabel('x', fontsize=14)
        plt.ylabel('y(x)', fontsize=14)
        return fig, x, y

    fig9, xh, yh = numpy_funcs()
    fig9
    return (yh,)


@app.cell
def _(np, yh):
    # сортировка массива
    yh_sorted = np.sort(yh)
    (yh[0], yh[-1]), (yh_sorted[0], yh_sorted[-1])
    return


@app.cell
def _(np):
    # функция meshgrig
    nx, ny = 5, 6
    xm, ym = np.linspace(0, 1, nx), np.linspace(0, 1, ny)
    X, Y = np.meshgrid(xm, ym)
    Z = X**2 + Y**2
    xm, ym, X, Y, Z
    return X, Y, Z


@app.cell
def _(X, Y, Z, plt):
    fig10 = plt.figure(figsize=(14,3))
    ax = plt.subplot(111, projection='3d')
    cb = ax.plot_surface(X, Y, Z, cmap='rainbow')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.colorbar(cb)

    fig10
    return


@app.cell
def _(np, plt):
    # Функция np.where
    def imp2(t, T=2.): 
        ts = t % T 
        return np.where(ts<=T/2, 1., 0.)

    tw = np.linspace(-2, 5, 1000)
    yw = imp2(tw)
    fig11 = plt.figure(figsize=(3,3))
    plt.plot(tw, yw, 'k-', lw=3)
    plt.xlabel('t', fontsize=14)
    plt.ylabel('y(t)', fontsize=14)
    fig11
    return


@app.cell
def _(f, np, plt):
    # Используем алгоритм Floyd-Steinberg 
    from PIL import Image

    # создаем изображение PIL из массива NumPy
    im = Image.fromarray(f)
    # преобразуем изображение PIL image в "газетное"
    fp = im.convert(mode='1',dither=Image.FLOYDSTEINBERG) 
    # создаем массив NumPy из  изображения PIL
    fpa = np.array(fp)
    # визуализируем преобразованное "газетное" изображение
    fig12 = plt.figure(figsize=(4, 5))
    plt.imshow(fpa, cmap='gray')
    plt.axis('off')
    print(f"{fpa.shape=}, {fpa.dtype=}")
    fig12
    return (fpa,)


@app.cell
def _(fpa, plt):
    # небольшой фрагмент "газетного" изображения
    ff = fpa[400:500, 550:650]
    fig13 = plt.figure(figsize=(3,3))
    plt.imshow(ff, cmap='gray')
    fig13
    return


if __name__ == "__main__":
    app.run()
