import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.integrate import solve_ivp # решение системы дифференциальных уравнений

    #mo.md('# Хищник-жертва')
    return mo, np, plt, solve_ivp


@app.function
def predator_prey(t, z, α, β, λ1, λ2, γ, δ):
    '''
    Правая часть системы уравнений Лотки-Вольтерры ("хищник жертва")
    Параметры:
    t - время 
    z - кортеж (x, y)
    x - величина, характеризующвя численность жертвы, например, число зайцев
        на квадратный километр
    y - величина, характеризующая численность хищника
    α - коэффициент прироста численности жертв (без учета уничтожения ее хищником)
    β - величина, характеризующая  смертность хищников
    λ1, λ2 - величины, характеризующие скорость 
             уничтожения жертв хищниками 
             и обусловленную этим скорость изменения
             численности хищников             
    γ - величина, учитывающая внутривидовую конкуренцию  в популяции жертв
    δ - величина, учитывающая внутривидовое сотрудничество  в популяции хищников
    Функция возвращает правую часть системы уравнений Лотки-Вольтерры 

    '''
    x, y = z
    return [α*x - λ1*x*y - γ*x**2, λ2*x*y - β*y+ δ*y**2]


@app.cell
def _(np, solve_ivp):
    # значения параметров 
    α, β, λ1, λ2, γ, δ =0.5, 0.2, 0.05, 0.02, 0.0005, 0.0001
    # начальные условия
    x0, y0 = 50, 5
    t_end = 250

    n = 10_000 # число разбиений интервала времени
    t_eval = np.linspace(0, t_end, n) # массив времен

    z = solve_ivp(predator_prey, [0, t_end], (x0, y0), 
                       method='RK45', t_eval=t_eval,
                       args=(α, β, λ1, λ2, γ, δ))
    return


@app.cell
def _(mo):
    # Элементы пользовательского интерфейса
    title_label = mo.md('#Хищник-жертва (система уравнений Лотки-Вольтерры)').center()
    tmax_label = mo.md('Время интегрирования:')
    tmax_slider = mo.ui.slider(label='', start=0, stop=500, 
                               step=5, value=50, debounce=True, show_value=True)
    x0_label = mo.md('Начальная численность жертв:')
    x0_slider = mo.ui.slider(label='', start=0, stop=200, 
                               step=1, value=50, debounce=True, show_value=True)
    y0_label = mo.md('Начальная численность хищников:')
    y0_slider = mo.ui.slider(label='', start=0, stop=200, 
                               step=1, value=5, debounce=True, show_value=True)
    α_label = mo.md('Прирост численности жертвы:')
    α_slider = mo.ui.slider(label='', start=0, stop=1, 
                               step=.01, value=.5, debounce=True, show_value=True)
    β_label = mo.md('Прирост численности хищников:')
    β_slider = mo.ui.slider(label='', start=0, stop=1, 
                               step=.01, value=.2, debounce=True, show_value=True)
    λ1_label = mo.md('Скорость уничтожения жертв хищниками:')
    λ1_slider = mo.ui.slider(label='', start=0, stop=0.2, 
                               step=.01, value=.05, debounce=True, show_value=True)
    λ2_label = mo.md('Скорость изменения численности хищников:')
    λ2_slider = mo.ui.slider(label='', start=0, stop=0.2, 
                               step=.01, value=.02, debounce=True, show_value=True)
    γ_label = mo.md('Внутривидовая конкуренция  у жертв:')
    γ_slider = mo.ui.slider(label='', start=0, stop=0.005, 
                               step=.0001, value=.0, debounce=True, show_value=True)
    δ_label = mo.md('Внутривидовое сотрудничество у хищников:')
    δ_slider = mo.ui.slider(label='', start=0, stop=0.005, 
                               step=.0001, value=.0, debounce=True, show_value=True)
    w_label = mo.md('Ширина рисунка, дюймы')
    w_slider = mo.ui.slider(label='', start=1, stop=15, 
                               step=.5, value=6, debounce=True, show_value=True)
    h_label = mo.md('Высота рисунка, дюймы')
    h_slider = mo.ui.slider(label='', start=1, stop=15, 
                               step=.5, value=6, debounce=True, show_value=True)
    lw_label = mo.md('Толщина линии')
    lw_slider = mo.ui.slider(label='', start=0.5, stop=5, 
                               step=.5, value=1, debounce=True, show_value=True)
    return (
        h_label,
        h_slider,
        lw_label,
        lw_slider,
        title_label,
        tmax_label,
        tmax_slider,
        w_label,
        w_slider,
        x0_label,
        x0_slider,
        y0_label,
        y0_slider,
        α_label,
        α_slider,
        β_label,
        β_slider,
        γ_label,
        γ_slider,
        λ1_label,
        λ1_slider,
        λ2_label,
        λ2_slider,
    )


@app.cell
def _(mo, np, plt, solve_ivp):
    def calculate_visualize(t_end=250, x0=50, y0=5, α=0.5, β=0.2,
                            λ1=0.05, λ2=0.02, γ=0, δ=0,
                            figsize=(4, 6), lw=1):

        n = 10_000 # число разбиений интервала времени
        t_eval = np.linspace(0, t_end, n) # массив времен

        z = solve_ivp(predator_prey, [0, t_end], (x0, y0), 
                           method='RK45', t_eval=t_eval,
                           args=(α, β, λ1, λ2, γ, δ))
        if z.success: # успешное интегрирование
            fig, axs = plt.subplots(nrows=2, ncols=1, figsize=figsize)
            axs[0].plot(z.t, z.y[0,:], 'b-', lw=lw, label='Численность жертв' )
            axs[0].plot(z.t, z.y[1,:], 'r-', lw=lw, label='Численность хищников' )
            axs[0].set_xlabel('Время')
            axs[0].set_ylabel('Численность жертв и хищников')
            # легенда
            axs[0].legend()        

            axs[1].plot(z.y[0,:], z.y[1,:],'b-', lw=lw)
            axs[1].set_xlabel('Численность жертв')
            axs[1].set_ylabel('Численность хищников')

            plt.tight_layout()
            return fig
        else:
            return mo.md(f"**Интегрирование завершилось неудачей. Сообщение: {z.message}**")

    return (calculate_visualize,)


@app.cell
def _(
    calculate_visualize,
    h_slider,
    lw_slider,
    tmax_slider,
    w_slider,
    x0_slider,
    y0_slider,
    α_slider,
    β_slider,
    γ_slider,
    λ1_slider,
    λ2_slider,
):
    def c_and_v():    
        return calculate_visualize(t_end=tmax_slider.value, 
                        x0=x0_slider.value, y0=y0_slider.value,
                        α=α_slider.value, β=β_slider.value,
                        λ1=λ1_slider.value, λ2=λ2_slider.value,
                        #γ=γ_slider.value, δ=δ_slider.value,
                        γ=γ_slider.value, δ=0,           
                        figsize=(w_slider.value, h_slider.value), 
                        lw=lw_slider.value)

    return (c_and_v,)


@app.cell
def _(
    c_and_v,
    h_label,
    h_slider,
    lw_label,
    lw_slider,
    mo,
    title_label,
    tmax_label,
    tmax_slider,
    w_label,
    w_slider,
    x0_label,
    x0_slider,
    y0_label,
    y0_slider,
    α_label,
    α_slider,
    β_label,
    β_slider,
    γ_label,
    γ_slider,
    λ1_label,
    λ1_slider,
    λ2_label,
    λ2_slider,
):
    lhs = mo.vstack([
     tmax_label, tmax_slider, 
     x0_label, x0_slider,
     y0_label, y0_slider,
     α_label, α_slider, 
     β_label, β_slider, 
     λ1_label, λ1_slider, 
     λ2_label, λ2_slider, 
     γ_label, γ_slider, 
     # δ_label, δ_slider,
     w_label, w_slider,  
     h_label, h_slider,
     lw_label, lw_slider,
    ])

    gui = mo.vstack([
        title_label,
        mo.hstack([lhs,c_and_v()])   
    ])

    gui
    return


if __name__ == "__main__":
    app.run()
