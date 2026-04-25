import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import math
    import matplotlib.pyplot as plt

    mo.md("# Решаем систему алгебраических уравнений графическим методом")
    return (plt,)


@app.cell
def _():
    def get_x(xmin=-3, xmax=-3, n=100):
        return [xmin + (xmax - xmin)/n*i for i in range(n+1)]

    get_x(0, 1, 5)

    return (get_x,)


@app.cell
def _():
    def f1(x, y, a):
        return x**2 + y**2 - a**2

    def f2(x, y, b):
        return x**2 - y**2 - b**2

    f1(1,0, 1), f2(1, 1, 1)
    return f1, f2


@app.cell
def _(f1, get_x):
    def fxy(f, min, max, n=100, args=()):
        xx = get_x(min, max, n) 
        return [[f(x, y, *args) for x in xx] for y in xx]

    fxy(f1, -2, 2, n=5, args=(1,))
    return (fxy,)


@app.cell
def _(f1, f2, fxy, get_x, plt):
    def visualize(f1, f2, xmin=-1.5, xmax=1.5, n=100, 
                  figsize=(3,3), args=((1.,), (.5,))):
        xx = get_x(xmin, xmax, n)
        z1 = fxy(f1, xmin, xmax, n, args=args[0])
        z2 = fxy(f2, xmin, xmax, n, args=args[1])

        fig = plt.figure(figsize=(3,3))
        plt.contour(xx, xx, z1, levels=[0], colors=['red'])
        plt.contour(xx, xx, z2, levels=[0], colors=['blue'])
        plt.grid()    
        return fig

    visualize(f1, f2, args=((1.,), (.0,)))
    return (visualize,)


@app.cell
def _(f1, f2, visualize):
    visualize(f1, f2, args=((1.,), (.2,)))
    return


@app.cell
def _(f1, f2, visualize):
    visualize(f1, f2, args=((1.,), (.5,)))
    return


@app.cell
def _(f1, f2, visualize):
    visualize(f1, f2, args=((1.,), (1.,)))
    return


@app.cell
def _(f1, f2, visualize):
    visualize(f1, f2, args=((1.,), (1.1,)))
    return


if __name__ == "__main__":
    app.run()
