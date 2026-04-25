import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import uncertainties as unc
    import uncertainties.umath as um
    from uncertainties import unumpy as unp 
    from uncertainties import correlated_values
    from Ivl  import Ivl

    mo.md("# Работаем с библиотекой uncertainties")
    return Ivl, correlated_values, mo, np, plt, um, unc


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Режим калькулятора
    """)
    return


@app.cell
def _(um, unc):
    x = unc.ufloat(1, 0.1)  # x = 1+/-0,1
    y = unc.ufloat(1, 0.1)
    x, y, um.cos(2 * x)
    return x, y


@app.cell
def _(x, y):
    # простые арифметические операции
    x - y, x - x
    return


@app.cell
def _(unc):
    # инициализация с помощью строкового  представления
    (
        unc.ufloat_fromstr("0.50+/-0.01"),  # каноническое представление
        unc.ufloat_fromstr("(5+/-0.1)e-01"),  # экспоненциальное представление
        unc.ufloat_fromstr("5.00(1)"),  # сокращенное представление
        unc.ufloat_fromstr("0.50±0.01"),  # представление для печати
        # автоматическое задание погрешности +/-1 для последней цифры
        unc.ufloat_fromstr("0.50"),
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Функции на числах с погрешностями
    """)
    return


@app.cell
def _(um, unc):
    (
        um.log10(unc.ufloat(1.00, 0.01) ** 2),
        um.log(unc.ufloat_fromstr("1.00")),
        um.exp(unc.ufloat_fromstr("1.00")),
        um.sin(unc.ufloat(1.57, 0.5)),
        um.cos(unc.ufloat(1.57, 0.5)),
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Извлекаем номинальное значение и СКО
    """)
    return


@app.cell
def _(unc):
    v = unc.ufloat(0.5, 0.01)
    v, v.n, v.nominal_value, v.std_dev, v.s
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Вычисляем $(1-cos(x))/x^2$ с помощью unc
    """)
    return


@app.cell
def _(plt, um, unc):

    def cos_1(eps):
        u = unc.ufloat(eps,eps)
        v = (1 - um.cos(u)) / u**2
        return v, v.n, v.s, abs(0.5-v.n)


    nom = []
    std = []
    epss = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1.5e-8, 1.2e-8, 1.1e-8, 1e-8, 1e-9]
    for _eps in epss:
        _v, _n, _s, _err = cos_1(_eps)
        nom.append(_err)
        std.append(_s)

    _fig, _ax = plt.subplots(figsize=(6,4))
    _lns1 =_ax.plot(epss, nom, 'b-', lw=3, label='номинальное значение')
    _ax.set_xscale('log')
    _ax.set_yscale('log')
    _ax.set_xlabel(r'$\varepsilon$')
    _ax.set_ylabel('$|(1-cos(x))/x^2 -0.5|$')
    _ax.grid()
    _ax2 = _ax.twinx()
    _lns2 =_ax2.plot(epss, std, 'r:', lw=5, label='СКО')
    _ax2.set_ylabel('СКО')
    _ax2.set_yscale('log')
    # легенда
    _lns = _lns1 + _lns2
    _labs = [_l.get_label() for _l in _lns]
    _ax.legend(_lns, _labs, loc=0)
    plt.tight_layout()
    plt.savefig('03_09.png', dpi=300, facecolor='white')

    _fig #, epss, nom, std
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Логистическое отображение
    """)
    return


@app.cell
def _(np, plt):
    def logistic(x=0.5, r=3.1, n=5):
        t = np.linspace(0, n, n+1)
        y = np.ones(n+1)*x
        for i in range(1, n+1):
            y[i] = r *y[i-1]*(1 - y[i-1])
        return t, y

    _fig = plt.figure(figsize=(5, 4))
    _t, _y = logistic(n=25, r=3.1, x=0.5)
    plt.plot(_t, _y, 'b-', ms=2), _t, _y 
    plt.xlabel("$i$")
    plt.ylabel("$x_i$")
    plt.savefig('03_10.png', dpi=300, facecolor='white')
    _fig, _y 
    return


@app.cell
def _(unc):
    def logistic1(x=.5, r=3.1):   
        return r * x * (1 - x) 

    _n = 25
    _x = unc.ufloat(0.5, 1e-30)
    for _i in range(1, _n+1):
        _x = logistic1(_x)
        print(f"{_i=}, {_x=}") 
    return (logistic1,)


@app.cell
def _(unc):
    def logistic2(x=unc.ufloat(0.5, 1e-6), r=3.1):
        nom, std = x.n, x.s
        return r * unc.ufloat(nom, std) * (1 - unc.ufloat(nom, std)) 

    _n = 25
    iters, delta1 = [], []
    _x = unc.ufloat(0.5, 1e-7)
    for _i in range(1, _n+1):
        _x = logistic2(_x)
        iters.append(_i)
        delta1.append(_x.s)
        print(f"{_i=}, {_x=}")
    return (iters,)


@app.cell
def _(Ivl, logistic1):
    # Интервальная арифметика

    _n = 25
    delta2 = []
    _x = Ivl(0.5, 1e-7)
    for _i in range(1, _n+1):
        _x = logistic1(_x)
        #ii.append(_i)
        delta2.append(_x.delta)
        print(f"{_i=}, {_x=}")
    return (delta2,)


@app.cell
def _(correlated_values, np):
    def logistic3(nom=0.5, std=1e-7, r=3.1, corr=0.9):
        '''
        Вычисляем логистическое отображение для
        коррелированных величин.
        Параметры:
        nom - номинальное значение
        std - СКО
        r - коэффициент логистического отображения
        corr - коэффициент корреляции
        corr = 0  - независимые переменные
        corr = 1 - одна и та же перемнная 
        Функция возвращает значение
        r * u * (1 - v),
        где u,v - коррелированне переменные 
        '''
        # Шаг 1. Подготовка данных
        # создаем массив номинальных значений
        noms = np.array([nom, nom])
        # корреляционная матрица
        R = np.array([[1, corr], [corr, 1]])
        # создаем массив СКО
        stds = np.array([std, std])

        # Шаг 2. Расчет ковариационной матрицы
        # элемент i,j коварианной матрицы равен Rij*stdi*stdj 
        # вычислить ковариационную матрицу удобно
        # через внешнее произведение

        cov_matrix = R * np.outer(stds, stds)

        # Шаг 3. Создание коррелированных переменных
        # средствами библиотеки uncertainties
        u, v = correlated_values(noms, cov_matrix)

        # Шаг 4. Возвращаем  результат логистического отображения
        result = r * u * (1 - v)
        #print(f"{corr=}, {R=}, {cov_matrix=}, {u=}, {v=}, {result=}")

        return result

    logistic3(corr=0), logistic3(corr=1), logistic3()   

    return (logistic3,)


@app.cell
def _(delta2, iters, logistic3, np, plt):
    def logistic3_visualize(nom=0.5, std=1e-6, r=3.1, n =25, figsize=(5, 4),
                            corrs=(0.0,0.5, 0.7, 0.9, 0.95, 0.99)):
        iters = np.linspace(0, n, n+1)
        stds = np.ones((len(corrs), n+1))
        fig = plt.figure(figsize=figsize)
        for i, corr in enumerate(corrs):
            stds[i, :] = std
            nom_value = nom

            for j in range(1, n+1):
                result = logistic3(nom=nom_value, std=stds[i, j-1], r=r, corr=corrs[i])
                nom_value, stds[i, j] = result.n, result.s  
            plt.plot(iters, stds[i, :], lw=3, label=f'corr={corrs[i]}')
        plt.yscale('log')
        plt.xlabel('i')
        plt.ylabel('СКО')
        #plt.legend()
        return fig

    _fig = logistic3_visualize(n=50)
    _n = 19
    plt.plot(iters[:_n], delta2[:_n], lw=3, label="интервалы")
    plt.legend()
    plt.savefig('03_11.png', dpi=300, facecolor='white')
    _fig
    return


if __name__ == "__main__":
    app.run()
