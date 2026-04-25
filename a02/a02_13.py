import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md("# Раскладки пользовательских интерфейсов")
    return (mo,)


@app.cell
def _(mo):
    mo.md(f"""
    ## Вставка виджетов в Markdown
    Вставляем текушую дату/время: {mo.ui.datetime()}
    """)
    return


@app.cell
def _(mo):
    mo.md('''
    Делаем то же самое с помощью batch: 

    дата/время: {dt} слайдер: {sl}
    ''').batch(dt=mo.ui.datetime(), 
               sl=mo.ui.slider(start=1, stop=10, step=1, value=7))
    return


@app.cell
def _(mo):
    mo.output.append(mo.md("## Размещаем виджеты по вертикали"))
    mo.output.append(mo.vstack(
        items = [
            mo.ui.slider(label="Слайдер:", start=1, stop=10, 
                         step=1, value=8, full_width=True),
            mo.ui.number(label="Ввод числа:", 
                         value=42,full_width=True),
            mo.ui.text_area(label="Текстовая область:",
                           placeholder="Здесь можно ввести текст",
                           rows=6),
        ], 
        heights="equal", gap=1, align="stretch", justify="center" )
    )
    return


@app.cell
def _(mo):
    mo.output.append(mo.md("## Размещаем виджеты по горизонтали"))
    mo.output.append(mo.hstack([
        mo.ui.slider(label="Слайдер:", start=1, stop=10, 
                         step=1, value=8),
        mo.ui.number(label="Ввод числа:", value=42),   
        mo.ui.text_area(label="Текстовая область:",
            placeholder="Здесь можно ввести текст",                     rows=3), 
        mo.ui.checkbox(label="Флажок", value=True),
        mo.ui.switch(label="Переключатель:",value=True)

    ],  wrap=True, justify="space-between"))
    return


@app.cell
def _(mo):
    mo.md("""
    ## Верстаем приложение
    """)
    return


@app.cell
def _():
    # трилистник - трехмерная кривая и поверхность
    import numpy as np
    import matplotlib.pyplot as plt

    def trefoil(u, v, r):
        x = r * np.sin(3 * u) / (2 + np.cos(v))

        y = r * (np.sin(u) + 2 * np.sin(2 * u)) / \
        (2 + np.cos(v + np.pi * 2 / 3))

        z = r / 2 * (np.cos(u) - 2 * np.cos(2 * u)) * \
        (2 + np.cos(v)) * (2 + np.cos(v + np.pi * 2 / 3)) / 4
        return np.array([x, y, z], dtype=np.float64)


    def trefoil_curve_surface(n=300, rmin=-1, rmax=3, wmax=5):

        r = (rmin*np.pi, rmax*np.pi)

        i = np.linspace(r[0], r[1], n)

        # поверхность
        U, V = np.meshgrid(i, i)
        W = trefoil(U, V, wmax)
        S = np.swapaxes(W, 0, 2)
        xs, ys, zs = S[:, :,0], S[:, :,1], S[:, :,2]

        # кривая
        T =  trefoil(i, i, 5) 
        xc, yc, zc = T[0], T[1], T[2]

        return  xc, yc, zc, xs, ys, zs 

    def plot(f=trefoil_curve_surface, argc=(), figsize=(4,3), 
             axis=True, azim=-60,elev=30, roll=0):
        # рисуем трехмерную книвую
        xc, yc, zc, *rest = f(*argc)
        fig = plt.figure(figsize=(5,6))
        ax = plt.axes(projection='3d')
        ax.plot(xc, yc, zc, linewidth=5, color="black")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        if axis:
            ax.axis("on")
        else:
            ax.axis("off")
        # повороты
        az = ax.azim if azim is None else azim
        el = ax.elev if elev is None else elev
        rl = ax.roll if roll is None else roll
        ax.view_init(azim=az, elev=el, roll=rl)
        plt.tight_layout()
        return fig

    return (plot,)


@app.cell
def _(mo):
    # Элементы пользовательского интерфейса
    title = mo.md("# Вращаем трехмерную кривую вокруг осей").center()
    azim = mo.ui.slider(label="Ось Z:", start=-180, stop=180, 
                        debounce=True,
                        step=5, value=-60, full_width=False)
    elev = mo.ui.slider(label="Ось X:", start=-180, stop=180,
                        debounce=True,
                        step=5, value=30, full_width=False)
    roll = mo.ui.slider(label="Ось Y:", start=-180, stop=180, 
                        debounce=True,
                        step=5, value=0, full_width=False)
    axis = mo.ui.switch(label="Оси координат", value=True)
    return axis, azim, elev, roll, title


@app.cell
def _(axis, azim, elev, mo, plot, roll, title):
    # собственно верстка
    mo.vstack([
        title,
        mo.hstack([
            mo.vstack([mo.hstack([azim, mo.md(f'${azim.value}^o$')]), 
                       mo.hstack([roll, mo.md(f'${roll.value}^o$')]), 
                       mo.hstack([elev, mo.md(f'${elev.value}^o$')]), 
                       axis
                      ]), 
            plot(azim=azim.value, elev=elev.value, 
                 roll=roll.value, axis=axis.value, figsize=(4,3) 
            )
        ])
    ])
    return


@app.cell
def _(mo):
    mo.md("""
    ## Гармошка (mo.accordion)
    """)
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    from time import sleep

    def time_consuming_function(dt=5, text=""):
        sleep(dt)
        return mo.md(text)

    accordion = mo.accordion(
        items={
            "Дверь 1": mo.lazy(time_consuming_function(dt=5, text="Нечего")),
            "Дверь 2": mo.lazy(time_consuming_function(dt=5, text="**Приз!!!**")),        
            "Дверь 3": mo.lazy(time_consuming_function(dt=5, text="Ничего")),          
        },
    )
    mo.md(f'''
    ## "Гармошка" (mo.accordion)
    {accordion}
    ''')
    return (time_consuming_function,)


@app.cell
def _(mo, time_consuming_function):
    mo.lazy(time_consuming_function(dt=5, text="123"))
    return


@app.cell
def _(mo):
    mo.md("""
    ## Боковая панель (sidebar)
    """)
    return


@app.cell
def _(mo):
    mo.sidebar(
        [
            mo.md("# marimo"),
            mo.nav_menu(
                {
                    "#/home": f"{mo.icon('lucide:home')} Home",
                    "#/about": f"{mo.icon('lucide:user')} About",
                    "#/contact": f"{mo.icon('lucide:phone')} Contact",
                    "Links": {
                        "https://twitter.com/marimo_io": "Twitter",
                        "https://github.com/marimo-team/marimo": "GitHub",
                    },
                },
                orientation="horizontal",
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(f"""
    ## Иерархия
    {mo.tree(["Элемент", "Элемент со списком", {"key": [0, 1, 2]}], 
             label="Дерево")}
    """)
    return


@app.cell
def _(mo):
    nav_menu = mo.nav_menu(
        {
            "/overview": f"{mo.icon('lucide:home')}Начало",    
            "/users" : f"{mo.icon('lucide:user')}Пользователи",         
            "/login" : f"{mo.icon('lucide:log-in')}Войти", 
        }
    )

    mo.md(f"""
    ## Навигационное меню
    {nav_menu}
    """)
    return


if __name__ == "__main__":
    app.run()
