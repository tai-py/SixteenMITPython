import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium", layout_file="layouts/e07_02.grid.json")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    # Вспомогательный модуль аффинных преобразований
    from affine import draw_contour
    from affine import affine_transformation
    from affine import composition

    mo.md("# Знакомимся с кривыми Безье")
    return affine_transformation, mo, np, plt


@app.cell
def _(np):
    def besier(x, y, nt=100):   
        # делим кривую на сегменты
        n_p = len(x) # число точек кривой
        # print(f"{n_p=}")
        segments = []
        while n_p > 0:        
            if n_p>4:
                segments.append((x[:4], y[:4]))
                x = x[3:]
                y = y[3:]
                n_p -= 3
            else:
                segments.append((x, y))
                n_p = 0
                break

        n_s = len(segments) # число сегментов кривой
        t = np.linspace(0., 1, nt) # массив значений параметра
        xr, yr = np.zeros(n_s*nt), np.zeros(n_s*nt) # массивы координат кривой Безье
        for i in range(n_s): # строим кривую по сегментам
            p_s = segments[i] # опорные точки сегмента кривой
            x_s = p_s[0]
            y_s = p_s[1]
            ls = len(x_s)
            if ls==1: # реализуем формулу (3)
                xr[i*nt:(i+1)*nt] = x_s[0]
                yr[i*nt:(i+1)*nt] = x_s[0]
            elif ls==2:
                xr[i*nt:(i+1)*nt] = x_s[0]*(1-t) + x_s[1]*t
                yr[i*nt:(i+1)*nt] = y_s[0]*(1-t) + y_s[1]*t            
            elif ls==3:
                xr[i*nt:(i+1)*nt] = x_s[0]*(1-t)**2 + x_s[1]*2*t*(1-t) + x_s[2]*t**2
                yr[i*nt:(i+1)*nt] = y_s[0]*(1-t)**2 + y_s[1]*2*t*(1-t) + y_s[2]*t**2
            else:
                xr[i*nt:(i+1)*nt] = x_s[0]*(1-t)**3 + x_s[1]*3*t*(1-t)**2 + x_s[2]*3*t**2*(1-t) + x_s[3]*t**3
                yr[i*nt:(i+1)*nt] = y_s[0]*(1-t)**3 + y_s[1]*3*t*(1-t)**2 + y_s[2]*3*t**2*(1-t) + y_s[3]*t**3

        return xr, yr, segments    
    return (besier,)


@app.cell
def _(besier, plt):
    def draw_besier(x, y, nt=100, fig=None, figsize=(3,3), ms=10, lw=3):
        xr, yr, segments = besier(x, y, nt=100)
        if fig is None:
            fig = plt.figure(figsize=figsize) if figsize else plt.figure()
        plt.plot(xr, yr, 'k-', lw=3)
        plt.plot(x, y, 'b*', ms=ms)
        plt.xlabel('x')
        plt.ylabel('y')
        # соединяем опорные точки с лежащими на кривой
        for segment in segments:
            xs, ys = segment
            ns = len(xs)
            if ns>=3:
                plt.plot([xs[0],xs[1]], [ys[0], ys[1]], 'k--', lw=0.5)
                plt.plot([xs[-2],xs[-1]], [ys[-2], ys[-1]], 'k--', lw=0.5)
        # задаем одинаковые масштабы по осям координат
        plt.gca().set_aspect("equal")
        return fig

    # draw_besier(np.array([0.,1., 2, 3, 4., 5, 6, 7, 8]), np.array([0.,1., 1, 0, 1., 1., 0, 1, 1]), nt=100)
    return (draw_besier,)


@app.cell
def _(mo):

    title = mo.md('''
    ## Рисование  и преобразование кривой
    Введите координаты точек кривой по горизонтальной и вертикальной осям
    ''')
    _mes = "Подкрался незаметно" # сообщение ошибках
    xb = mo.ui.text_area(label="x:", value="0,1,2", rows=2)
    yb = mo.ui.text_area(label="y:", value="0,1,0",rows=2)
    coefs = mo.ui.text_area(label="coefs:", value="1, 0, 0, \n0, 1, 0",
                            rows=2)
    fsize = mo.ui.number(label="Размер:", value=3, start=2, stop=10, step=0.5)
    layout = mo.vstack([title, xb, yb, coefs, fsize])
    layout
    return coefs, fsize, xb, yb


@app.cell
def _(mo):
    btn = mo.ui.run_button(label="Запустить приложение") #, on_change=change)
    mo.hstack([btn], justify="center")
    #btn #, second_button
    return (btn,)


@app.cell
def _(affine_transformation, btn, coefs, draw_besier, fsize, mo, np, xb, yb):
    resultb = mo.md("Нажмите кнопку **Запустить приложение**")
    mes =None
    if btn.value:    
        try:
            xbv = np.fromstring(xb.value, dtype=float, sep=',')
        except:
            mes = "Не смог преобразовать координаты x кривой"
        try:
            ybv = np.fromstring(yb.value, dtype=float, sep=',')
        except:
            mes = "Не смог преобразовать координаты y кривой"
        try:
            coefsv = np.fromstring(coefs.value, dtype=float, sep=',')
        except:
            mes = "Не удалось ввести коэффициенты аффинного преобразования"
        try:
            coefsv.shape =2,3
        except:
            mes = "Коэффициентоы аффиного преобразования обязательно должно быть шесть"
        figsz = fsize.value
        if not mes and xbv.shape != ybv.shape :
            mes = "Число точек кривой по осям x и y не совпадает"
        if not mes:
            # исходная кривая Безье
            fig21 = draw_besier(xbv, ybv, figsize=(figsz, figsz))
            _xy = affine_transformation(xbv, ybv, coefsv)        
            fig22 = draw_besier(_xy[0], _xy[1], figsize=(figsz, figsz))
            resultb = (fig21, fig22)

    resultb, mes
    return


if __name__ == "__main__":
    app.run()
