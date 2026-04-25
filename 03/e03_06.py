import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from Ivl import Ivl

    mo.md("# Рассчитываем температуру в стержне с помощью интервальной арифметики")
    return Ivl, np, plt


@app.cell
def _(Ivl, np):
    def bar_ivl(
        u0=0.0,
        dx=0.05,
        tmax=0.1,
        dt=5e-6,
        alpha=1.0,
        C=1.0,
        D=10.0,
        p=1000.0,
        draw=True,
        xs=0.5,
        ls="-",
        eps=1e-3,
    ):
        """
        Расчет температуры в стержне
        u0 - температура окружающей среды
        dx - шаг по пространственной координате
        tmax -  время интегрирования
        dt - шаг по времени
        alpha - теплоотдача с единичы длины
        C - теплоемкость единицы длины стержня
        D - теплопроводность стержня
        p - мощность, выделяющаяся на единице длины стержня
        draw - признак рисования графика зависимости температуры от времени
        xs - координата для которой рисуется график
        ls - стиль линии
        eps - интервал значений начальной температуры
        Функция возвращает масив распределения температур в стержне u,
        t - массив времен, x - массив координат,
        """
        nx = int(1.0 / dx + 1)  # число разбиений по x
        x = np.linspace(0.0, 1.0, nx)
        nt = int(tmax / dt + 1)  # число разбиений по t
        t = np.linspace(0.0, tmax, nt)
        A = dt / C * D / dx**2
        B = 2 * A + alpha * dt / C - 1
        P = Ivl.ones((nt, nx), eps=0) * (p + alpha * u0) * dt / C
        u = Ivl.zeros((nt, nx), eps=eps) + u0

        for i in range(nt - 1):  # цикл по времени
            u[i + 1, 1:-1] = (
                A * u[i, 2:] - B * u[i, 1:-1] + A * u[i, 0:-2] + P[i, 1:-1]
            )

        return u, t, x

    return (bar_ivl,)


@app.cell
def _(bar_ivl):
    _u, _t, _x = bar_ivl(dx=0.05, tmax=0.1, dt=1.25e-4, eps=0.001)
    _u[-1, _u.shape[1] // 2], _u[-1, _u.shape[1] // 2].delta
    return


@app.cell
def _(bar_ivl):
    _u, _t, _x = bar_ivl(dx=0.05, tmax=0.2, dt=1.25e-4, eps=0.001)
    _u[-1, _u.shape[1] // 2], _u[-1, _u.shape[1] // 2].delta
    return


@app.cell
def _():
    0.05 / 1.25e-4, 0.05 / 1.264e-4
    return


@app.cell
def _(bar_ivl):
    u2, t2, x2 = bar_ivl(dx=0.05, tmax=0.1, dt=1.264e-4)
    u2[-1, u2.shape[1] // 2].delta
    return t2, u2


@app.cell
def _(u2):
    float(u2[-1, u2.shape[1] // 2].delta)
    return


@app.cell
def _(plt, t2, u2):
    _fig = plt.figure(figsize=(4, 3))
    umax2 = u2.b
    umin2 = u2.a
    ax = plt.subplot(111)
    ax.plot(t2, umax2[:, u2.shape[1] // 2], "k-")
    line2 = ax.plot(t2, umin2[:, u2.shape[1] // 2], "k-", label="u")
    ax.set_xlabel("$t$")
    ax.set_ylabel("$u(t,x)$")
    ax.grid()
    ax2 = ax.twinx()
    udelta2 = u2.delta
    line3 = ax2.plot(
        t2, udelta2[:, u2.shape[1] // 2], "r-", lw=3, label=r"$\delta$"
    )
    ax2.set_ylabel(r"$\delta (t)$")

    lines = line2 + line3  # линии
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, loc="best")
    plt.tight_layout()
    plt.savefig("03_05.png", dpi=300, facecolor="white")
    _fig
    return


if __name__ == "__main__":
    app.run()
