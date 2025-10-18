import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.integrate import solve_ivp

    import schemdraw
    import schemdraw.elements as elm

    mo.md("# Рисуем и рассчитывем схему генератора на туннельном диоде")
    return elm, mo, np, plt, schemdraw, solve_ivp


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Рисуем схему""")
    return


@app.cell
def _(elm, schemdraw):
    # Рисуем схему генератора
    with schemdraw.Drawing() as d:  # инициализируем рисунок
        # Европейский стиль (МЭК) отображения электронных схем
        elm.style(elm.STYLE_IEC)
        # Источник ЭДС (направление вверх)
        d += elm.SourceI().label("E").up()
        # Резистор с надписью рисуем горизонтально
        d += elm.Resistor().label("R").right()
        # Индуктивность
        d += elm.Inductor2().label("L").dot()
        # Здесь у нас разветвление
        d.push()  # запоминаем состояние
        # Рисуем туннельный диод, направление вниз, рисуем точку
        d += elm.DiodeTunnel().label("D").down().dot()
        # Возвращаемся назад вверх
        d.pop()
        # Русуем укороченную горизонтальную линию
        d += elm.Line(l=2)
        # Рисуем конденсатор, направление вниз
        d += elm.Capacitor().label("C").down()
        # Рисуем линии и точку для замыкания схемы
        d += elm.Line(l=2).left()
        d += elm.Line()
        d += elm.Line().dot()
        # Заземляем схему
        d += elm.Vss()
        d.save("05_22.png", dpi=300, transparent=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Вольт-амперная характеристика туннельного диода (ВАХ)""")
    return


@app.cell
def _(np, plt):
    from numpy import polynomial as poly

    ud_ = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2])
    id_ = np.array([0.0000, 0.0100, 0.0040, 0.0010, 0.0009, 0.0030, 0.0100])
    vah = poly.Polynomial.fit(ud_, id_, 6)  # аппроксимация полиномом 6 степени
    _n = 1000
    _uu = np.linspace(ud_[0], ud_[-1], _n)
    plt.plot(ud_, id_, "ks", label="исходные данные")
    plt.plot(_uu, vah(_uu), "k-", label="аппроксимация ВАХ")
    plt.xlabel("$u_D$")
    plt.ylabel("$i_D(u_D)$")
    plt.legend()
    plt.savefig("05_23.png", dpi=300, facecolor="white")
    return (vah,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Функция для вычисления правых частей системы уравнений (5.10), (5.11)""")
    return


@app.function
def rh_td(t, y, E, R, L, vah, C):
    i, ud = y
    return [(E - i * R - ud) / L, (i - vah(ud)) / C]


@app.cell
def _(np, plt, solve_ivp, vah):
    def tdiod(E=0.35, R=10., L=5.e-8, C=5.e-11, umax=1.2,
              vah=vah, method='RK45',
              tmax=5.e-8, n = 1000, figsize=(8, 8), fn=''):
        t = np.linspace(0., tmax, n)
        # решение системы уравнений
        y = solve_ivp(rh_td, [0, tmax], (0., 0.), 
                      method=method, t_eval=t,
                      args=(E, R, L, vah, C))
        if y.success:
            i, ud = y.y[0, :], y.y[1, :] # распаковка
            # Визуализация
            fig = plt.figure(figsize=figsize) 

            # рисуем ток от времени
            plt.subplot(2,2,1) 
            plt.plot(t, i, lw=3, color='black')
            plt.xlabel('$t$')
            plt.ylabel('$i(t)$')
            plt.grid(ls='solid', lw=0.2)
            plt.title("Ток от времени", fontsize=14)

            # рисуем напряжение на диоде от времени
            plt.subplot(2,2,2) 
            plt.plot(t, ud, lw=3, color='black')
            plt.xlabel('$t$')
            plt.ylabel('$u_D(t)$')
            plt.grid(ls='solid', lw=0.2)
            plt.title("Напряжение на диоде от времени", fontsize=14)

            # Зависимость напряжения от тока
            plt.subplot(2,2,3) 
            plt.plot(ud, i, lw=3, color='black')
            plt.xlabel('$u_D(t)$')
            plt.ylabel('$i(t)$')
            plt.grid(ls='solid', lw=0.2)     
            plt.title("Зависимость тока напряжения ", fontsize=14)    

            # ВАХ
            plt.subplot(2,2,4) 
            ud_ = np.linspace(0, umax, n)
            id_ = vah(ud_) 
            plt.plot(ud_, vah(ud_), lw=3, color='black')
            plt.xlabel('$u_D$')
            plt.ylabel('$i$')
            plt.grid(ls='solid', lw=0.2)
            plt.title("ВАХ и линия нагрузки", fontsize=14)
            plt.ylim(0, np.max(id_))
            # линия нагрузки
            ur = np.linspace(0.,E, n) 
            ir = (E - ur)/R
            plt.plot(ur, ir, lw=3, ls='--', color='red')

            plt.tight_layout()
            if fn:
                plt.savefig(fn, dpi=300, facecolor='white')
            return fig
        else:
            return f'Интегрирование закончилось неудачно. \nСообщение:{y.message}'

    tdiod(fn='05_24.png')    
    return (tdiod,)


@app.cell
def _(tdiod):
    tdiod(R=18, fn='05_25.png') 
    return


if __name__ == "__main__":
    app.run()
