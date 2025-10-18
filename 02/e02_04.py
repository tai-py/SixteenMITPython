import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    from scipy.optimize import newton, root
    import sympy as smp
    import matplotlib.pyplot as plt

    mo.md("# Сердце, пронзенное стрелой")
    return mo, np, plt, root, smp


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Кардиоида и прямая линия""")
    return


@app.cell
def _():
    def line(x, y, a, b):
        return y - a * x - b

    def cardioid(x, y):
        return (x**2 + y**2 - 0.5) ** 3 - 3 * x**2 * y**3
    return (cardioid,)


@app.cell
def _(cardioid, np, plt):
    def draw_heart_arrow(n=1000, xlim=(-1.2, 1.2), 
                         a=-1, b=0.2, ylim=(-0.8, 1.2), 
                         figsize=(6, 6)
    ):
        x, y = np.linspace(*xlim, n), np.linspace(*ylim, n)
        X, Y = np.meshgrid(x, y)
        fig, ax = plt.subplots(figsize=figsize)
        # кардиодида
        ax.contour(X, Y, cardioid(X, Y), 
                   levels=[0], colors=["blue"])
        ax.plot(x, a * x + b, "r-")
        ax.grid()
        ax.set_aspect(1)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect(1)
        plt.tight_layout()

        # plt.savefig("newton_13.png", dpi=300, 
        #            facecolor="white")

        return fig


    draw_heart_arrow()
    return


@app.cell
def _(mo):
    mo.md(r"""## Симаолическое вычисление корней""")
    return


@app.cell
def _(np, smp):
    def symbolic_heart_arrow(a=-1, b=0.2):
        x, y, z = smp.symbols("x y z")
        # символические выражения для стрелы и сердца
        arrow = a * x + b
        heart = (x**2 + y**2 - 0.5) ** 3 - 3 * x**2 * y**3
        # подставляем стрелу в сердце
        heart = heart.subs(y, arrow)
        # раскрываем скобки
        heart = smp.expand(heart)
        # решаем полиномиальное уравнение
        # с помощью функции roots
        heart_roots_dict = smp.roots(heart, x)
        x_roots = []
        for r in heart_roots_dict:
            # вычисляем значения корня
            c_root = complex(r.evalf())
            miltiplicity = heart_roots_dict[r]
            for _ in range(miltiplicity):
                x_roots.append(c_root)
        x_roots = np.array(x_roots)
        y_roots = a * x_roots + b
        return np.vstack([x_roots, y_roots])


    croots = symbolic_heart_arrow()
    croots
    return croots, symbolic_heart_arrow


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Конструируем собственную цветовую палитру""")
    return


@app.cell
def _(np, plt):
    from matplotlib.colors import ListedColormap

    # цвета палитры
    colors = ('black', 'lightgray', 'red', 'blue', 
          'yellow', 'lime','white', 'purple',
          'cyan', 'magenta')

    # создаем собственную палитру из последовательности цветов
    custom_cmap = ListedColormap(colors)

    def visialize_areas_of_attractions(
        root_numbers, figsize=(6, 6), cmap=custom_cmap,
        fn='' ):
        fig = plt.figure(figsize=figsize)
        # отображаем номера цветов
        c = plt.imshow(
            root_numbers[::-1, :], 
            vmin=0, vmax=len(cmap.colors), cmap=cmap)
        # соответствие между номером корня и цветом

        # отключение осей координат
        plt.axis("off")
        if fn:
            plt.savefig(fn, dpi=300, facecolor="white")  
        return fig

    root_numbers = np.linspace(0, 15, 16, 
         dtype=np.int16).reshape(4, 4) \
         % len( custom_cmap.colors)

    visialize_areas_of_attractions(root_numbers)
    return (visialize_areas_of_attractions,)


@app.cell
def _(mo):
    mo.md(r"""## Система уравнений для численного решения""")
    return


@app.cell
def _():
    def heart_arrow(p, a=-1, b=0.2):
        xc, yc = p    
        arrow = a * xc + b -yc
        heart = (xc**2 + yc**2 - 0.5) ** 3 - 3 * xc**2 * yc**3
        return arrow, heart

    #тестирование
    _a, _b = -1, .2
    _x, _y = -0.87307269, 1.07307269

    heart_arrow((-0.87307269,1.07307269), _a, _b)
    return (heart_arrow,)


@app.cell
def _(mo):
    mo.md(r"""## Тестируем решение системы уравнений""")
    return


@app.cell
def _(heart_arrow, root):
    _r = root(heart_arrow, (-.9,1), args=(-1, .2), tol=1e-10)
    _r.success, _r.x
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Функция для вычисления номера корня уравнения""")
    return


@app.cell
def _(croots, heart_arrow, np, root):
    def get_heart_arrow_root(croots, f=heart_arrow, x0=-.87, y0=1,
                             args=(-1, 0.2), method=None, eps=1e-4):

        p = (x0, y0) # начальное приближение
        # выбор метода
        if method:
            r = root(f, p, args=args, method=method)
        else:
            r = root(f, p, args=args)
        # корень не найден   
        if not r.success:
            return 0 
        x_root =r.x[0]
        y_root = r.x[1]
        croot = np.array([x_root, y_root], dtype=np.complex128)
        # номер корня
        err = np.max(np.abs(croot - croots.T), axis=1)
        iroot = np.where(err<eps)[0]
        #print(f"{r=}, \n{croots.T=} \n{croot=}, \n{err=} \n{np.abs(croot - croots.T)=}")

        iroot = 0 if iroot.size==0 else iroot[0] + 1
        return iroot

    get_heart_arrow_root(croots, method='df-sane')
    return (get_heart_arrow_root,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Функция для визуализации областей притяжения корней""")
    return


@app.cell
def _(
    get_heart_arrow_root,
    heart_arrow,
    np,
    symbolic_heart_arrow,
    visialize_areas_of_attractions,
):
    def visualize_roots(n=100,f=heart_arrow, a=0.0, b=0.2, 
                        method='hybr', eps=1e-4,
                        area=(-1.5,-1.5,1.5, 1.5),  
                        figsize=(6,5), fn=''):
        xmin, ymin, xmax, ymax = area
        xx = np.linspace(xmin, xmax, n)
        yy = np.linspace(ymin, ymax, n)
        field = np.zeros((n, n), dtype=np.uint8)
        croots = symbolic_heart_arrow(a=a, b=b)
        for iy in range(n):
            for ix in range(n):
                xs, ys = xx[ix], yy[iy]
                iroot = get_heart_arrow_root(croots, f=f, x0=xs, y0=ys,
                             args=(a, b), method=method, eps=eps)
                field[iy, ix] = iroot 

        return  visialize_areas_of_attractions(field, figsize=figsize, fn=fn)


    visualize_roots(n=400, a=-1,b=.2, method='lm', fn="newton_15a.png")
    return (visualize_roots,)


@app.cell
def _(visualize_roots):
    visualize_roots(n=400, a=0,b=0.25, method='lm', fn="newton_15b.png")
    return


@app.cell
def _(visualize_roots):
    visualize_roots(n=400, a=0,b=-.7, method='lm',  fn="newton_15c.png")
    return


@app.cell
def _(visualize_roots):
    visualize_roots(n=400, a=0,b=1, method='lm', fn="newton_15d.png")
    return


@app.cell
def _(mo):
    mo.md(r"""## Строим анимацию""")
    return


@app.cell(hide_code=True)
def _(plt, visualize_roots):
    bs=(-0.7, -.65, -0.6,-.55, -.5,-.45, -.4,-.35, 
        -.25, -.2,-.15,  -0.1, -0.05,
         .01,0.05, 0.1,0.15,0.2, .25,
        0.3, .35, 0.4,.45,.5,.55,.6,.65,.7,.75, .8,.85,
         .9, 0.95, 1., 1.05, 1.1, 1.14)

    def save_images(n=50, bs=bs, method='lm'):
        for i, b in enumerate(bs):
            fig = visualize_roots(n=n, b=b, method=method)
            plt.savefig(f"anim/{i}.png", dpi=300, facecolor="white") 
            print(f"Изображение: {i}, {b=}")

    save_images(n=400)
    return (bs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Собираем и сохраняем анимацию""")
    return


@app.cell
def _(bs, plt):
    import gif
    import matplotlib.image as img

    @gif.frame
    def frame(i):
        im = img.imread(f'anim/{i}.png')
        fig = plt.figure(figsize=(6,6))
        im = im[200:1300, 350:1450]
        plt.imshow(im) 
        plt.title(f"b={bs[i]:6.2f}")
        plt.axis('off')
        return fig
    return frame, gif


@app.cell
def _(frame, gif):
    frames = [frame(i) for i in range(37)] 
    gif.save(frames, 'anim/anim.gif', duration=100)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Отображаем анимацию средствами marimo""")
    return


@app.cell
def _(mo):
    mo.image("./anim/anim.gif")
    return


if __name__ == "__main__":
    app.run()
