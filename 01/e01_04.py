import marimo

__generated_with = "0.13.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    return mo, np, plt


@app.cell
def _(mo):
    mo.md(r"""# Эллипсы и овалы Кассини""")
    return


@app.cell
def _():
    def mean(a,b):
        '''Среднее арифметическое a, b'''
        return (a + b) / 2.

    mean(2, 4)
    return (mean,)


@app.cell
def _(np):
    def gmean(a, b):
        '''Среднее геометрическое a, b'''
        return np.sqrt(a * b)

    gmean(2,4)
    return (gmean,)


@app.cell
def _(mean, np):
    def ellipse(x, y, a, c):
        '''Эллипс как геометрическое место точек'''
        return mean(np.sqrt((x - c)**2 + y**2), 
                    np.sqrt((x + c)**2 + y**2)) - a
    return (ellipse,)


@app.cell
def _(gmean, np):
    def cassini(x, y, a, c):
        '''Эллипс как геометрическое место точек'''
        return gmean(np.sqrt((x - c)**2 + y**2), 
                    np.sqrt((x + c)**2 + y**2)) - a
    return (cassini,)


@app.cell
def _(cassini, ellipse, np, plt):
    def draw_ellipse_oval_cassini(n=1000, a=2, c=1,  
                                  xmax=2.5,  figsize=(4,4),
                                  colors=['lime', 'pink'],
                                  fn=""):
        '''
        Рисуем эллипс и овал Касиини.
        Параметры:
        n - число разбиений,
        a, c  - параметры фигуры,
        xmax - размер области,
        figsize - размер рисунка,
        colors - цвета для рисования эллипса и
                 овала Кассини,
        путь к файлу для сохранения рисунка.
        Функция возвращает рисунок с 
        эллипсом и овалом Кассини для
        заданных значение параметров a, c
        '''
        # строим двумерную сетку на плоскости x0y    
        x = np.linspace(-xmax, xmax)
        X, Y = np.meshgrid(x, x)
        # рассчитываем значения функций на двумерной
        # сетке
        Ze = ellipse(X, Y, a, c) # эллипс
        Zc = cassini(X, Y, a,c) # овал Кассини
        # рисуем контурную карту
        _fig = plt.figure(figsize=(4,4))    
        plt.contour(X, Y, Ze, [0], colors=[colors[0]])
        plt.contour(X, Y, Zc, [0], colors=[colors[1]])
        # фокусы
        plt.plot([-c, -c], [0,0], 'b+', ms=10)
        plt.plot([c, c], [0,0], 'b+', ms=10)
        #a, c = float(a), float(c)
        plt.title(f"{a=:5.3f}, {c=:5.3f}")
        #plt.grid()
        plt.axis("equal")
        # сохранение рисунка
        if fn:
            plt.savefig(fn, dpi=300, facecolor="white")
        return _fig

    draw_ellipse_oval_cassini(a=2, c=1, fn='01_11a.png')
    return (draw_ellipse_oval_cassini,)


@app.cell
def _(draw_ellipse_oval_cassini, np):
    draw_ellipse_oval_cassini(a=np.sqrt(2), c=1, fn='01_11b.png')
    return


@app.cell
def _(draw_ellipse_oval_cassini):
    draw_ellipse_oval_cassini(a=1.1, c=1, fn='01_11c.png')
    return


@app.cell
def _(draw_ellipse_oval_cassini):
    draw_ellipse_oval_cassini(a=1.01, c=1,  fn='01_11d.png')
    return


@app.cell
def _(draw_ellipse_oval_cassini):
    draw_ellipse_oval_cassini(a=1.0, c=1,  fn='01_11e.png')
    return


@app.cell
def _(draw_ellipse_oval_cassini):
    draw_ellipse_oval_cassini(a=0.9, c=1, fn='01_11f.png')
    return


@app.cell
def _(draw_ellipse_oval_cassini):
    draw_ellipse_oval_cassini(a=0.7, c=1)
    return


if __name__ == "__main__":
    app.run()
