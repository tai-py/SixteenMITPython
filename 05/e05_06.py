import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.integrate import solve_ivp

    mo.md("# Двойной маятник")
    return mo, np, plt, solve_ivp


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Рисуем двойной маятник""")
    return


@app.cell
def _(plt):
    def draw_double_pendulum(
        x0=0, y0=0, x1=1, y1=-1, x2=1.5, y2=-2, figsize=(6, 5), ms1=5, ms2=15
    ):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
        pad = 0.05
        ax.plot([x0, x1, x2], [y0, y1, y2], "k-", lw=3)
        ax.plot(x0, y0, "bo", ms=ms1)
        ax.plot(x1, y1, "bo", ms=ms2)
        ax.plot(x2, y2, "bo", ms=ms2)
        ax.text(pad, pad, "(0, 0)")
        ax.text(0.5 + pad, -0.5 + pad, r"$l_1$")
        ax.text(1.25 + pad, -1.25 - 3 * pad, r"$l_2$")
        ax.plot([x0, x0], [y0, y2], "k--")
        ax.plot([x1, x1], [y1, y2], "k--")
        ax.text(x0 + pad, y0 - 4 * pad, r"$\alpha_1$")
        ax.text(x1 + pad, y1 - 7 * pad, r"$\alpha_2$")
        ax.text(x1 + 2 * pad, y1 + 2 * pad, r"$m_1, x_1, y_1$")
        ax.text(x2 + 2 * pad, y2 + 2 * pad, r"$m_2, x_2, y_2$")
        ax.set_aspect(1)
        plt.axis("off")
        plt.savefig("05_25.png", dpi=300, facecolor="white")
        return fig


    draw_double_pendulum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r""" """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Реализуем двойной маятник""")
    return


@app.cell
def _(np):
    def coords(a1, a2, l1=1, l2=1):
        """
        Пересчет углов в координаты двойного маятника
        a1, a2 - углы в радианах
        l1, l2 - длины плеч маятника
        Функция возвращает
        x1, y1, x2, y2 - координаты грузов маятника
        """
        x1 = l1 * np.sin(a1)
        y1 = -l1 * np.cos(a1)
        x2 = l1 * np.sin(a1) + l2 * np.sin(a2)
        y2 = -l1 * np.cos(a1) - l2 * np.cos(a2)
        return x1, y1, x2, y2
    return (coords,)


@app.cell
def _(np):
    def rh_dp(t, y, m1=1, mu=1, l=1, g=9.81):
        a1, a2, p1, p2 = y  # распаковка
        a1d = (p1 - p2 * np.cos(a1 - a2)) / (
            m1 * l**2 * (1 + mu * np.sin(a1 - a2) ** 2)
        )
        a2d = (p2 * (1 + mu) - p1 * mu * np.cos(a1 - a2)) / (
            m1 * l**2 * (1 + mu * np.sin(a1 - a2) ** 2)
        )

        A1 = (
            p1
            * p2
            * np.sin(a1 - a2)
            / (m1 * l**2 * (1 + mu * np.sin(a1 - a2) ** 2))
        )
        A2 = (
            (p1**2 * mu - 2 * p1 * p2 * mu * np.cos(a1 - a2) + p2**2 * (1 + mu))
            * np.sin(2 * (a1 - a2))
            / (2 * m1 * l**2 * (1 + mu * np.sin(a1 - a2) ** 2) ** 2)
        )

        p1d = -m1 * (1 + mu) * g * l * np.sin(a1) - A1 + A2
        p2d = -m1 * mu * g * l * np.sin(a2) + A1 - A2

        return a1d, a2d, p1d, p2d


    rh_dp(0, [np.pi / 4, np.pi / 4, 0, 0])
    return (rh_dp,)


@app.cell
def _():
    return


@app.cell
def _(integration_error):
    integration_error(
        eps=1e-7, alpha1=2.6, alpha2=1.5, mu=0.2, tmax=5000, n=200_000
    )
    return


@app.cell
def _(integration_error):
    integration_error(
        eps=1e-7,
        method="RK45",
        alpha1=2.6,
        alpha2=1.5,
        mu=0.2,
        tmax=5000,
        n=200_000,
    )
    return


@app.cell
def _(integration_error):
    integration_error(
        eps=1e-7,
        method="Radau",
        alpha1=2.6,
        alpha2=1.5,
        mu=0.2,
        tmax=5000,
        n=200_000,
    )
    return


@app.cell
def _(integration_error):
    integration_error(
        eps=1e-7,
        method="DOP853",
        alpha1=2.6,
        alpha2=1.5,
        mu=0.2,
        tmax=5000,
        n=200_000,
    )
    return


@app.cell
def _():
    return


@app.cell
def _(integration_error):
    integration_error(
        eps=1e-7,
        method="Radau",
        alpha1=2.6,
        alpha2=1.5,
        mu=0.2,
        tmax=10000,
        n=200_000,
    )
    return


@app.cell
def _(integration_error):
    integration_error(
        eps=1e-9,
        method="BDF",
        alpha1=2.6,
        alpha2=1.5,
        mu=0.2,
        tmax=5000,
        n=200_000,
    )
    return


@app.cell
def _(integration_error):
    integration_error(
        eps=1e-10,
        method="BDF",
        alpha1=2.6,
        alpha2=1.5,
        mu=0.2,
        tmax=5000,
        n=200_000,
    )
    return


@app.cell
def _(integration_error):
    integration_error(
        eps=1e-6,
        method="BDF",
        alpha1=2.6,
        alpha2=1.5,
        mu=0.2,
        tmax=5000,
        n=200_000,
    )
    return


@app.cell
def _(integration_error):
    integration_error(
        eps=1e-2,
        method="BDF",
        alpha1=2.6,
        alpha2=1.5,
        mu=0.2,
        tmax=5000,
        n=200_000,
    )
    return


@app.cell
def _(coords, np, plt, rh_dp, solve_ivp):
    def visualize_double_pendulum(
        m1=1.0, # масса первого маятника
        mu=1.3, # m2/m1 - отношение масс
        alpha1=np.pi / 2, # начальное отклонение 1ого маятника
        alpha2=np.pi / 2, # начальное отклонение 1ого маятника
        tmax=10, # время интегрирования
        n=10000, # число разбиений отрезка [0, tmax]
        l=1.0, # длины плеч маятника
        g=9.81, # ускорение земного притяжения
        method="BDF", # метод интегрирования
        figsize=(4, 4), # размер изображения
        lw=1, # толщина линии
        lw2=0.5,  # толщина линии
        fn="",  # путь к файлу для сохранения картинки
        aspect=True, # признак равных масштабов по осям координат
        axis=True, # признак отключения отображения осей координат
        mode=1, # тип визуализации
    ):
        # начальные условия
        y0 = [alpha1, alpha2, 0.0, 0.0]
        # массив времен
        t = np.linspace(0, tmax, n)
        # дополнительные параметры
        #      m1, mu, g, l
        args = m1, mu, g, l
        # решение системы дифференциальных уравнений
        y = solve_ivp(
            rh_dp,  # правые части системы уравнений
            [0, tmax],  # временной интервал
            y0,  # начальные условия
            t_eval=t,  # массив времен
            method=method,  # метод решения
            dense_output=True,
            args=args,  # дополнительные параметры
        )
        # пересчет в координаты
        a1, a2 = y.y[0, :], y.y[1, :]  # углы
        x1, y1, x2, y2 = coords(a1, a2, l1=l, l2=l)

        # визуализация
        if mode == 1:  # зависимости y1 vs x1, y2 vs x1
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
            ax.plot(x1, y1, lw=lw, label="$(x_1, y_1)$")
            ax.plot(x2, y2, lw=lw2, label="$(x_2, y_2)$")
            if aspect:
                ax.set_aspect(1)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            plt.legend()
            if axis:
                plt.axis("off")
        else:  # трехмерная зависимость колебаний от времени
            fig = plt.figure(figsize=figsize)
            ax = plt.subplot(121, projection="3d")
            ax.plot(t, x1, y1, color="b", lw=lw, label="$x_1, y_1=f_1(t)$")
            ax.set_xlabel("t")
            ax.set_ylabel("x")
            ax.set_zlabel("y")
            plt.legend()
            ax = plt.subplot(122, projection="3d")
            ax.plot(t, x2, y2, color="r", lw=lw, label="$x_2, y_2=f_2(t)$")
            ax.set_xlabel("t")
            ax.set_ylabel("x")
            ax.set_zlabel("y")
            plt.legend()
            if axis:
                plt.axis("off")
        plt.tight_layout()
        if fn:
            plt.savefig(fn, dpi=300, facecolor="white")
        return x1, y1, x2, y2, fig


    visualize_double_pendulum()
    return (visualize_double_pendulum,)


@app.cell
def _(np, visualize_double_pendulum):
    visualize_double_pendulum(
        alpha1=0,
        alpha2=np.pi / 12,
        mode=2,
        tmax=500,
        n=2_000,
        lw=1,
        axis=False,
        mu=0.2,
        figsize=(12, 4), fn='05_26.png',
    )
    return


@app.cell
def _(visualize_double_pendulum):
    visualize_double_pendulum(
        mode=2, tmax=500, n=2_000, lw=1, axis=False, mu=0.2, figsize=(12, 4)
    )
    return


@app.cell
def _(visualize_double_pendulum):
    visualize_double_pendulum(
        mode=2, tmax=500, n=5_000, lw=1, axis=False, mu=1, figsize=(12, 4)
    )
    return


@app.cell
def _(np, visualize_double_pendulum):
    visualize_double_pendulum(
        alpha1= 0, alpha2 = 2*np.pi/3,
        mode=2, tmax=500, n=2_000, lw=1, axis=False, mu=.2, figsize=(12, 4), fn='05_27.png'
    )
    return


@app.cell
def _(visualize_double_pendulum):
    visualize_double_pendulum(
        mode=2, tmax=500, n=5_000, lw=1, axis=False, mu=1, figsize=(12, 4)
    )
    return


@app.cell
def _(visualize_double_pendulum):
    visualize_double_pendulum(
        alpha1=2.6,
        alpha2=1.5,
        mode=2,
        tmax=500,
        n=2_000,
        lw=1,
        axis=False,
        mu=1,
        figsize=(12, 4), fn='05_27.png' 
    )
    return


@app.cell
def _(visualize_double_pendulum):
    visualize_double_pendulum(
        alpha1=2.6, alpha2=1.5, mu=0.2, tmax=5000, n=200_000, lw=2, lw2=0.5, fn='05_28b',
    )
    return


@app.cell
def _(visualize_double_pendulum):
    visualize_double_pendulum(
        alpha1=2.6, alpha2=1.5, mu=2, tmax=5000, n=200_000, lw=2, lw2=0.5, fn='05_28a',
    )
    return


@app.cell
def _(np, visualize_double_pendulum):
    visualize_double_pendulum(
        alpha1=0,
        alpha2=np.pi / 6,
        l=0.2,
        mu=2,
        tmax=5000,
        n=200_000,
        lw=2,
        lw2=0.5,
    )
    return


@app.cell
def _(np, visualize_double_pendulum):
    visualize_double_pendulum(
        alpha1=-np.pi - 0.3,
        alpha2=np.pi + 0.2,
        l=0.2,
        mu=0.2,
        tmax=5000,
        n=200_000,
        lw=2,
        lw2=0.5,
    )
    return


@app.cell
def _(np, visualize_double_pendulum):
    visualize_double_pendulum(
        alpha1=0,
        alpha2=np.pi + 0.2,
        l=0.2,
        mu=0.2,
        tmax=5000,
        n=200_000,
        lw=2,
        lw2=0.5,
    )
    return


@app.cell
def _(np, visualize_double_pendulum):
    visualize_double_pendulum(
        alpha1=171.0 / 180 * np.pi,
        alpha2=171 / 180 * np.pi,
        l=0.2,
        mu=2.75,
        tmax=5000,
        n=200_000,
        lw=2,
        lw2=0.5,
    )
    return


@app.cell
def _(np, visualize_double_pendulum):
    x11, y11, x12, y12, _fig = visualize_double_pendulum(
        alpha1=-np.pi / 2,
        alpha2=np.pi / 2,
        l=0.2,
        mu=0.2,
        tmax=5000,
        n=200_000,
        lw=2,
        lw2=0.5,
    )
    _fig
    return


@app.cell
def _(np, visualize_double_pendulum):
    eps = 1e-8
    x01, y01, x02, y02, _fig = visualize_double_pendulum(
        alpha1=-np.pi / 2 + eps,
        alpha2=np.pi / 2 + eps,
        l=0.2,
        mu=0.2,
        tmax=5000,
        n=200_000,
        lw=2,
        lw2=0.5,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""## Погрешности интегрирования""")
    return


@app.cell
def _(coords, np, plt, rh_dp, solve_ivp):
    def integration_error(
        eps=1e-7,
        m1=1.0,
        mu=1.3,
        alpha1=np.pi / 2,
        alpha2=np.pi / 2,
        tmax=10,
        n=10000,
        l=1.0,
        g=9.81,
        method="BDF",
        figsize=(6, 4),
        fn="",
    ):
        # начальные условия
        y01 = [alpha1, alpha2, 0.0, 0.0]  # исходные начальные условия
        y02 = [
            alpha1 + eps,
            alpha2 + eps,
            0.0,
            0.0,
        ]  # возмущенные начальные услович
        # массив времен
        t = np.linspace(0, tmax, n)
        # дополнительные параметры
        #      m1, mu, g, l
        args = m1, mu, g, l
        # решения системы дифференциальных уравнений
        y1 = solve_ivp(
            rh_dp,  # правые части системы уравнений
            [0, tmax],  # временной интервал
            y01,  # начальные условия
            t_eval=t,  # массив времен
            method=method,  # метод решения
            dense_output=True,
            args=args,  # дополнительные параметры
        )
        y2 = solve_ivp(
            rh_dp,  # правые части системы уравнений
            [0, tmax],  # временной интервал
            y02,  # начальные условия
            t_eval=t,  # массив времен
            method=method,  # метод решения
            dense_output=True,
            args=args,  # дополнительные параметры
        )
        if y1.success and y2.success:
            # пересчет в координаты
            a1, a2 = y1.y[0, :], y1.y[1, :]  # углы
            x11, y11, x21, y21 = coords(a1, a2, l1=l, l2=l)
            a1, a2 = y2.y[0, :], y2.y[1, :]  # углы
            x12, y12, x22, y22 = coords(a1, a2, l1=l, l2=l)
            errs = np.zeros((4, n))  # массив погрешностей
            errs[0, :] = np.abs(x11 - x12)
            errs[1, :] = np.abs(y11 - y12)
            errs[2, :] = np.abs(x21 - x22)
            errs[3, :] = np.abs(y21 - y22)
            err = np.max(errs, axis=0)
            max_err = np.max(err)
            fig = plt.figure(figsize=figsize)
            plt.plot(t, err)
            plt.xscale("log")
            plt.yscale("log")
            plt.xlabel("t")
            plt.ylabel("погрешность")
            plt.grid()
            if fn:
                plt.savefig(fn, dpi=300, facecolor="white")
            return fig, max_err, errs[:, -1]

        else:
            return "Процесс интегрирования не завершен"


    return (integration_error,)


@app.cell
def _(integration_error):
    integration_error(eps=1e-9, m1=1,  mu=0.2,
        alpha1=2.6, alpha2=1.5, tmax=5000,
        n=10000, l=1.0, g=9.81,     method="BDF", figsize=(6, 4),
        fn="05_29.png",
    )
    return


@app.cell
def _(integration_error):
    integration_error(eps=1e-8, m1=1,  mu=0.2,
        alpha1=2.6, alpha2=1.5, tmax=5000,
        n=10000, l=1.0, g=9.81,     method="BDF", figsize=(6, 4),
        fn="",
    )
    return


@app.cell
def _(integration_error):
    integration_error(eps=1e-7, m1=1,  mu=0.2,
        alpha1=2.6, alpha2=1.5, tmax=5000,
        n=10000, l=1.0, g=9.81,     method="BDF", figsize=(6, 4),
        fn="",
    )
    return


@app.cell
def _(integration_error):
    integration_error(eps=1e-6, m1=1,  mu=0.2,
        alpha1=2.6, alpha2=1.5, tmax=5000,
        n=10000, l=1.0, g=9.81,     method="BDF", figsize=(6, 4),
        fn="",
    )
    return


@app.cell
def _(integration_error):
    integration_error(eps=1e-5, m1=1,  mu=0.2,
        alpha1=2.6, alpha2=1.5, tmax=5000,
        n=10000, l=1.0, g=9.81,     method="BDF", figsize=(6, 4),
        fn="",
    )
    return


@app.cell
def _(integration_error):
    integration_error(eps=1e-4, m1=1,  mu=0.2,
        alpha1=2.6, alpha2=1.5, tmax=5000,
        n=10000, l=1.0, g=9.81,     method="BDF", figsize=(6, 4),
        fn="",
    )
    return


@app.cell
def _(integration_error):
    integration_error(eps=1e-3, m1=1,  mu=0.2,
        alpha1=2.6, alpha2=1.5, tmax=5000,
        n=10000, l=1.0, g=9.81,     method="BDF", figsize=(6, 4),
        fn="",
    )
    return


@app.cell
def _(integration_error):
    integration_error(eps=1e-2, m1=1,  mu=0.2,
        alpha1=2.6, alpha2=1.5, tmax=5000,
        n=10000, l=1.0, g=9.81,     method="BDF", figsize=(6, 4),
        fn="",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Погрешность интегрирования от погрешности в начальных условиях""")
    return


@app.cell
def _(np, plt):
    err0 = [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2]
    labels = ['$x_1$', '$y_1$', '$x_2$', '$y_2$']
    data = np.array([
        [0.39973172, 0.07746028, 1.57320371, 0.63245232], #1e-9
        [0.91535981, 1.37006719, 0.26697025, 0.68879458], #1e-8
        [0.40060426, 0.08972722, 0.401793, 0.62099276,],  #1e-7
        [0.12907093, 0.00659558, 0.10218185, 0.41285707], #1e-6
        [0.75651674, 1.66930044, 1.5613313, 0.94975753],  #1e-5
        [0.94820285, 1.35562218, 1.86309448, 0.62459309], #1e-4
        [0.93004841, 0.66898138, 0.04684002, 0.06313876], #1e-3
        [0.92280851, 0.64901772, 0.36315338, 0.00197016],#1e-2
    ])

    _fig = plt.figure(figsize=(6, 4))
    for _, _l in enumerate(labels):
        plt.plot(err0, data[:, _], label=labels[_])
    plt.plot(err0, np.sqrt(data[:, 0]**2 + data[:, 1]**2), label="$r_1$", lw=3)
    plt.plot(err0, np.sqrt(data[:, 2]**2 + data[:, 3]**2), label="$r_2$", lw=3)
    plt.xscale('log')
    plt.xlabel(r'$\varepsilon$[0]')
    plt.ylabel(r'$\varepsilon$[-1]')
    plt.legend()
    _fig
    return


if __name__ == "__main__":
    app.run()
