import marimo

__generated_with = "0.23.2"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import stats as st
    import matplotlib.pyplot as plt

    return mo, np, plt


@app.cell
def _(mo):
    # Элементы интерфейса
    title= mo.md('# **Строим гистограммы**').center()

    vol = mo.ui.slider(label='Объем выборки:', start=50, stop=10_000, value=1500, step=20, 
                       full_width=True, debounce=True, show_value=True)
    bins = mo.ui.slider(label='Число разрядов гистограммы:', start=5, stop=200, step=5, value=50, 
                        full_width=True, debounce=True, show_value=True)
    distrs = mo.ui.radio(label="Распределение:",
           options={'Нормальное':1, 'Равномерное':2, 
                    'Экспоненциальное':3, 'Бимодальное':4}, 
            value='Нормальное')
    width = mo.ui.slider(label='Ширина рисунка:', start=2, stop=12, step=1,  value=3, 
                         full_width=True, debounce=True, show_value=True)
    height = mo.ui.slider(label='Высота рисунка:', start=4, stop=12, step=1,  
                          value=5, full_width=True, debounce=True, show_value=True)   
    return bins, distrs, height, title, vol, width


@app.cell
def _(bins, distrs, height, mo, np, plt, vol, width):
    def get_data(fs=10):
        n = vol.value
        bn = bins.value
        kind = distrs.value
        if kind==1:
            data = np.random.normal(5, 2, n)
        elif kind==2:
            data = np.random.uniform(1, 5, n)
        elif kind==3:
            data = np.random.exponential(1, n)
        else:
            data = np.zeros(n)
            m = n//2
            data[:m]= np.random.normal(5, 2, m) 
            data[m:] = np.random.normal(15, 3, m)

        mean = np.mean(data)
        median = np.median(data)
        std = np.std(data)    

        _fig = plt.figure(figsize=(width.value,height.value))
        plt.subplot(211)
        plt.title('Плотность распределения', fontsize=fs)
        plt.hist(data, bins=bn, density=True, cumulative=False)
        plt.subplot(212)
        plt.title('Кумулятивная функция распределения', fontsize=fs)
        plt.hist(data, bins=bn, density=True, cumulative=True)
        plt.tight_layout()

        meanc = mo.md(f'**Среднее:{mean:6.3f}**') #.callout(kind='info')
        medianc = mo.md(f'**Медиана:{median:6.3f}**') #.callout(kind='info')
        stdc = mo.md(f'**СКО:{std:6.3f}**') #.callout(kind='info')
        stats = mo.vstack([meanc, medianc, stdc ])
        return _fig, stats



    return (get_data,)


@app.cell
def _(bins, distrs, get_data, height, mo, title, vol, width):
    # Собираем пользовательский интерфейс
    def ui():
        _fig, stats = get_data()
        lh = mo.vstack([mo.md('### Данные:'), vol, bins, distrs,
                       mo.md("### Рисунок"), width, height,
                       mo.md('### Характеристики распределения:'), stats])
        middle = mo.hstack([lh, _fig])
        result = mo.vstack([title, middle])

        return result

    ui()
    return


if __name__ == "__main__":
    app.run()
