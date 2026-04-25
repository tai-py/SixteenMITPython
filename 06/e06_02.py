import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    mo.md("#Строим модели для зашумленных данных")
    return np, plt


@app.cell
def _(np):
    def get_data(n=200, f=np.sin, ab=(0, 2*np.pi), s=0.3):
        x = np.random.uniform(ab[0], ab[1],n)
        y = f(x) + np.random.normal(0, s, n)
        return x, y

    get_data(5)
    return (get_data,)


@app.cell
def _(get_data, np, plt):
    def build_model(x, y, m=1):
        model = np.polyfit(x, y, m)
        return np.poly1d(model)


    _n = 1000
    _x, _y = get_data()
    _xx = np.linspace(np.min(_x), np.max(_x), _n)
    plt.plot(_x, _y, 'b+', ms=5)
    _model = build_model(_x, _y, 3)
    plt.plot(_xx, _model(_xx), 'r-')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig('06_09.png', dpi=300, facecolor="white")
    return (build_model,)


@app.cell
def _(build_model, get_data, np):
    def std_error(x, y, model):
        return np.std(y - model(x))

    _x, _y = get_data()
    _model = build_model(_x, _y, 3)
    std_error(_x, _y, _model)
    return (std_error,)


@app.cell
def _(build_model, get_data, np, plt, std_error):
    def test_models(n=200, f=np.sin, ab=(0, 2*np.pi), s=0.3, part=0.5,
                   ms=(1,3,5,7,9,11,13,15,17,19), figsize=(6, 6)):
        x, y = get_data(n=n, f=f,ab=ab, s=s)
        # формируем обучающую и проверочную последовательности
        ip = int(n*part)
        x_learn, y_learn = x[:ip], y[:ip] 
        x_test, y_test = x[ip:], y[ip:]

        # Погрешности для моделей
        errs_learn = []
        errs_test = []
        for i, m  in enumerate(ms):
            # строим модель степени m
            model = build_model(x_learn, y_learn, m=m)
            err = std_error(x_learn, y_learn, model)
            errs_learn.append(err)
            err = std_error(x_test, y_test, model)
            errs_test.append(err)        
        fig = plt.figure(figsize=figsize)
        plt.plot(ms,errs_learn, 'b-', lw=3, label="обучающие данные")
        plt.plot(ms,errs_test, 'r-', lw=3, label="проверочные данные")
        plt.xlim(0.5, 18.5)
        plt.xlabel('Степень модели')
        plt.ylabel('Погрешности')
        plt.yscale('log')
        plt.legend()
        plt.title(f"СКО:{s}")
        plt.tight_layout()

        return fig

    _fig = test_models(s=0.0)
    plt.savefig('06_10a.png', dpi=300, facecolor='white')
    _fig
    return (test_models,)


@app.cell
def _(test_models):
    test_models(s=0.1)
    return


@app.cell
def _(plt, test_models):
    _fig = test_models(s=0.3)
    plt.savefig('06_10b.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(test_models):
    test_models(s=0.5)
    return


if __name__ == "__main__":
    app.run()
