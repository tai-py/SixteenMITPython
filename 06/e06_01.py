import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns

    mo.md("# Рост и вес студентов МЭИ")
    return mo, np, pd, plt, sns


@app.cell
def _(np):
    data = np.array([
        [189, 177, 179, 183, 180, 185, 178, 186, 176, 185, 184, 180, 180, 188, 183, 195, 194, 188, 182, 195],
        [ 90,  80,  73,  73,  85,  83,  75,  75,  77,  73,  76,  74,   68,  81,  79,  88,  75,  79,  85,  80],
    ])

    height, weight = data[0, :], data[1, :]

    height, len(height), weight, len(weight)
    return height, weight


@app.cell
def _(mo):
    mo.md(r"""## Характеристики веса и роста студентов""")
    return


@app.cell
def _(height, np, weight):
    len(height), len(weight), np.min(height), np.min(weight), np.max(height), np.max(weight)
    return


@app.cell
def _(height, np, weight):
    (np.mean(height), np.mean(weight), np.median(height), np.median(weight), 
     np.std(height), np.std(weight), np.var(height), np.var(weight), np.corrcoef(height, weight))
    return


@app.cell
def _(mo):
    mo.md(r"""## Зарплаты в фирме""")
    return


@app.cell
def _(np):
    salaries = np.array([1_000_000, 50_000, 50_000, 50_000, 50_000, 
                            50_000, 50_000, 50_000, 50_000, 50_000])
    len(salaries), np.mean(salaries), np.median(salaries)
    return (salaries,)


@app.cell
def _(mo):
    mo.md(r"""## Характеристики разброса""")
    return


@app.cell
def _(np, salaries):
    np.ptp(salaries), np.var(salaries), np.std(salaries)
    return


@app.cell
def _(height, np):
    np.ptp(height), np.var(height), np.std(height)
    return


@app.cell
def _(np, weight):
    np.ptp(weight), np.var(weight), np.std(weight)
    return


@app.cell
def _(height, mo, np, salaries, weight):
    vars = [
        {"Массив":"Зарплаты", 
         "Среднее":f"{np.mean(salaries):6.2e}", "Медиана":f"{np.median(salaries):6.2e}", 
         "Размах": f"{np.ptp(salaries):6.2e}", 
         "Вариация":f"{np.var(salaries):6.2e}", "СКО":f"{np.std(salaries):6.2e}"}, 
        {"Массив":"Рост", 
         "Среднее":f"{np.mean(height):6.2e}", "Медиана":f"{np.median(height):6.2e}", 
         "Размах": f"{np.ptp(height):6.2e}", 
         "Вариация":f"{np.var(height):6.2e}", "СКО":f"{np.std(height):6.2e}"}, 
        {"Массив":"Вес", 
         "Среднее":f"{np.mean(weight):6.2e}", "Медиана":f"{np.median(weight):6.2e}", 
         "Размах": f"{np.ptp(weight):6.2e}", 
         "Вариация":f"{np.var(weight):6.2e}", "СКО":f"{np.std(weight):6.2e}"},     
    ]
    mo.ui.table(data=vars, label="Таблица 6.1. Статистические характеристики для трех массивов"  )
    return


@app.cell
def _(mo):
    mo.md(r"""## Корреляция между ростом и весом""")
    return


@app.cell
def _(height, np, weight):
    np.corrcoef(height, weight)
    return


@app.cell
def _(mo):
    mo.md(r"""## Визуализация с помощью matplotlib""")
    return


@app.cell
def _(height, plt, weight):
    _fig = plt.figure(figsize=(4, 4))
    plt.scatter(height, weight, marker='s', s=20)
    plt.xlabel('Рост, см')
    plt.ylabel('Вес, кг')
    plt.savefig("06_03.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(height, pd, weight):
    height_weight = pd.DataFrame({'рост':height, 'вес':weight})
    height_weight
    return (height_weight,)


@app.cell
def _(height_weight):
    height_weight.describe()
    return


@app.cell
def _(height_weight, plt, sns):

    _lmp = sns.lmplot(data=height_weight,  x="рост", y="вес", height=4)

    plt.savefig("06_07.png", dpi=300, facecolor='white') 
    _lmp
    return


@app.cell
def _(height_weight, plt, sns):
    _jnt = sns.jointplot(data=height_weight,  x="рост", y="вес", height=4)
    plt.savefig("06_08.png", dpi=300, facecolor='white')
    _jnt
    return


@app.cell
def _(mo):
    mo.md(r"""## Строим линию регрессии. Множественность моделей""")
    return


@app.cell
def _(height, np, weight):
    model1 = np.polyfit(height, weight, 1)
    model1
    return (model1,)


@app.cell
def _(height, np, weight):
    model2 = np.polyfit(weight, height, 1)
    model2
    return (model2,)


@app.cell
def _(height, np, weight):
    model3 = np.polyfit(height, weight, 2)
    model3
    return (model3,)


@app.cell
def _(model1, model2, model3, np):
    p1, p2, p3 = np.poly1d(model1), np.poly1d(model2), np.poly1d(model3)
    return p1, p2, p3


@app.cell
def _(np, p1, p2, p3):
    n = 1000
    h = np.linspace(170, 200, n)
    w = np.linspace(60, 100, n)
    w1, h2, w3 = p1(h), p2(w), p3(h)
    return h, h2, w, w1, w3


@app.cell
def _(h, h2, height, plt, w, w1, w3, weight):
    _fig = plt.figure(figsize=(6,6))
    plt.scatter(height, weight, marker='s', s=20, label="Данные опроса")
    plt.plot(h, w1, lw=3, label='model1')
    plt.plot(h, w3, lw=3, label='model3')
    plt.plot(h2,w, lw=3, label='model2')
    plt.xlabel('Рост, см')
    plt.ylabel('Вес, кг')
    plt.legend()
    plt.savefig("06_08.png", dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""## Описание функции polyfit""")
    return


@app.cell
def _(np):
    help(np.polyfit)
    return


@app.cell
def _(mo):
    mo.md(r"""## Система линейных уравнений для метода наименьших квадратов""")
    return


@app.cell
def _(height, np):
    from numpy.linalg import lstsq # метод наименьших квадратов

    m = len(height)
    mat = np.ones((m, 2)) # заготовка матрицы системы
    mat[:, 0] = height # коэффициенты при a
    # Для b ничего не делаем, т.к. коэффициенты равны 1
    return lstsq, mat


@app.cell
def _(lstsq, mat, weight):
    # Решем переопределенную систему линейныъ уравнений
    # методом наименьших квадратов
    (a,b), *rest = lstsq(mat, weight)
    a, b
    return


if __name__ == "__main__":
    app.run()
