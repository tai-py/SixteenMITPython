import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import sympy as  smp
    from scipy.optimize import root

    mo.md("# Строим переходную кривую виде кубической параболы")
    return mo, np, plt, root, smp


@app.cell
def _(np):
    def rh(t, R=1):
        '''
        Система уравнений для определения
        параметров переходного участка
        Параметры:
        t - кортеж параметров, включающий:
        xс - горизонтальная координата точки пересенеия
             переходного участка и поворотного круга,
        x0, y0 - координаты центра повортного круга,
        R - радиус поворотного круга.
        Функция возвращает кортеж невязок в точке пересечения для:
        1. координат переходного участка и повортного круга,
        2. касательных,
        3. кривизны.
        '''
        xc, x0, y0 = t # распаковываем параметры
        yc = xc**3 # вертикальная координата  для переходного участка
        # невязки
        eq1 = (xc - x0)**2 +(yc - y0)**2 - R**2 # уравнение 1
        eq2 = 3*xc**2*(yc - y0) + (xc - x0) # уравнение 2
        eq3 = 6*xc/np.sqrt(1 + 9*xc**4)**3 - 1/R # уравнение 3
        return eq1, eq2, eq3

    return (rh,)


@app.cell
def _(rh, root):
    _t, _R = (0.1, 0.1, 1), 1
    root(rh, _t, args=(_R,))
    return


@app.cell
def _(rh, root):
    _t, _R = (0., 0., 0), 1
    root(rh, _t, args=(_R,))
    return


@app.cell
def _(rh, root):
    def solve(xc=0, x0=0, y0=0, R=1.):
        '''
        Ищем решение при заданном начальном приближении
        '''
        result = root(rh, (xc, x0, y0), args=(R,))
        if result.success:       
            return result.x
        else:
            return None

    solve()
    return (solve,)


@app.cell
def _(solve):
    solve(.1, .1, .1)
    return


@app.cell
def _(np, solve):
    def scan_initials(m=5, xcs=(0.,1.), x0s=(0.,1.), 
                      y0s=(0.,1.), R=1., eps=1e-6,
                      key=2):
        '''
        Сканирование начальных приближений при опредлении
        вариантов параметров переходного пути
        m - число разбиений,
        xcs, x0s, y0s - интервалы начальный значений параметров,
        R - радиус поворотного круга,
        eps - постоянная для проверки идентичности решений,
        key - номер столбца, по которому происходит упорядочение,
        по умолчанию y0.

        Функция возвращает список решений задачи
        '''
        roots = []
        for xc in np.linspace(xcs[0], xcs[1], m):
            for x0 in np.linspace(x0s[0], x0s[1], m):
                for y0 in np.linspace(y0s[0], y0s[1], m):
                    r = solve(xc=xc, x0=x0, y0=y0, R=R)
                    #print(f"{r=}")
                    if not (r is None):
                        if len(roots)==0:
                            roots.append(r)
                        else:
                            diff = 1.e100
                            for rr in roots:
                                d = np.max(np.abs(r - rr))
                                diff = min(diff,d)
                            if diff >eps:
                               roots.append(r) 
        # упорядочение корней
        roots = np.array(roots)
        roots = roots[roots[:, key].argsort()]
        return roots

    scan_initials(m=20)
    return (scan_initials,)


@app.cell
def _(np, plt, scan_initials):
    def visualize_solutions(m=20, R=.7, n=1000, figsize=(6,6), lw=2, 
                           ms=10, equal=True, fs=8):
        '''
        Визуализируем список полученных решений
        m - число разинений диапазонов начальных значений параметров,
        R - радиус поворотного круга,
        n - число разбиений кривых на графиках,
        figsize - размер рисунка,
        lw - толщина линий,
        ms - размер маркера
        equal - флажок задания равных размеров по осям,
        fs - размер шрифта легенды
        Функция возвращает объект рисунка и списко решений
        '''
        # получаем список решений
        r = scan_initials(m=m, xcs=(0.,1.), x0s=(0.,1.), 
                      y0s=(0.,1.), R=R, eps=1e-6)

        t = np.linspace(-R, R, n)
        yc = np.where(t>=0, t**3, 0) # кубическая парабола
        fig = plt.figure(figsize=figsize) 
        colors = 'blue', 'red', 'brown', 'orange', 'lime'

        for i, rr in enumerate(r): # рисую окружности
            xc, x0, y0 = rr
            x, y = R*np.cos(2*np.pi*t) + x0, R*np.sin(2*np.pi*t) + y0        
            plt.plot(x, y, color=colors[i+1], lw=lw,  
                     label=f"круг №{i+1}")
            plt.plot(x0, y0, marker='+', color=colors[i+1], ms=ms)
            plt.plot(xc, xc**3, marker='+', color=colors[i+1], ms=ms)

        plt.plot(t, yc, color=colors[0], lw=lw, label='парабола')   
        plt.grid()
        plt.legend(fontsize=fs) 
        if equal:
            plt.axis('equal')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f"{R=}")
        return fig, r


    _fig = visualize_solutions(figsize=(4, 4), R=0.6)
    plt.savefig('01.04a.png', dpi=300, facecolor="white")
    _fig
    return (visualize_solutions,)


@app.cell
def _(plt, visualize_solutions):
    _fig = visualize_solutions(figsize=(4, 4), R=.8)
    plt.savefig('01.04b.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(plt, visualize_solutions):
    _fig = visualize_solutions(figsize=(4, 4), R=1.)
    plt.savefig('01.04c.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(plt, visualize_solutions):
    _fig = visualize_solutions(figsize=(4, 4), R=1.5)
    plt.savefig('01.04d.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(visualize_solutions):
    _fig = visualize_solutions(figsize=(4, 4), R=.5675)
    #plt.savefig('01.04e.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(plt, visualize_solutions):
    _fig = visualize_solutions(figsize=(4, 4), R=.56745)
    plt.savefig('01.05.png', dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(np):
    _xc = 0.38698833
    _R = .56745
    _Kr = 1/_R
    _Kc = 6*_xc/np.sqrt(1 + 9*_xc**4)**3
    _Kc, _Kr 
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Строим области притяжения корней
    """)
    return


@app.cell
def _(np, plt, scan_initials, solve):
    def root_traction(m=20, R=1, y0=0, cmap='rainbow',
                     eps=1e-6, figsize=(6,4)):
        r = scan_initials(m=m, xcs=(0.,1.), x0s=(0.,1.), 
                      y0s=(0.,1.), R=R, eps=1e-6)
        area = np.zeros((m, m))

        for i, xc in enumerate(np.linspace(0, 1, m)):
            for j, x0 in enumerate(np.linspace(0, 1, m)):
                c = solve(xc=xc, x0=x0, y0=y0, R=R)
                if not (c is None):
                    for k, rr in enumerate(r):
                        if np.max(np.abs(c - rr))< eps:
                            area[i, j] = k +1
        fig = plt.figure(figsize=figsize)
        cb = plt.imshow(area, cmap=cmap)
        plt.colorbar(cb)
        plt.axis('off')
        plt.title(f"{y0=:5.2f}")
        return fig

    # _fig = root_traction(m = 20)
    # plt.savefig('01.03a.png', dpi=300, facecolor="white")
    # _fig 
    return (root_traction,)


@app.cell
def _(plt, root_traction):
    _fig = root_traction(m = 50)
    plt.savefig('01.03a.png', dpi=300, facecolor="white")
    _fig 
    return


@app.cell
def _(plt, root_traction):
    _fig = root_traction(m = 50, y0=0.5)
    plt.savefig('01.03b.png', dpi=300, facecolor="white")
    _fig 
    return


@app.cell
def _(plt, root_traction):
    _fig = root_traction(m = 50, y0=1.0)
    plt.savefig('01.03c.png', dpi=300, facecolor="white")
    _fig 
    return


@app.cell
def _(root_traction):
    _fig = root_traction(m = 50, y0=0.0, R=0.6)
    _fig
    return


@app.cell
def _(root_traction):
    _fig = root_traction(m = 50, y0=0.5, R=0.6)
    _fig
    return


@app.cell
def _(root_traction):
    _fig = root_traction(m = 50, y0=1.0, R=0.6)
    _fig
    return


@app.cell
def _(root_traction):
    _fig = root_traction(m = 50, y0=1.0, R=0.57)
    _fig
    return


@app.cell
def _(root_traction):
    _fig = root_traction(m = 50, y0=.5, R=0.57)
    _fig
    return


@app.cell
def _(root_traction):
    _fig = root_traction(m = 50, y0=0., R=0.57)
    _fig
    return


@app.cell
def _(root_traction):
    _fig = root_traction(m = 50, y0=.5, R=0.5675)
    _fig
    return


@app.cell
def _(root_traction):
    _fig = root_traction(m = 50, y0=0., R=0.5675)
    _fig
    return


@app.cell
def _(root_traction):
    _fig = root_traction(m = 50, y0=1., R=0.5675)
    _fig
    return


@app.cell
def _(rh, root):
    _x, _x0, _y0, _R = .1, 0., .9, 1
    root(rh, (_x, _x0, _y0), args=(_R,)).x
    return


@app.cell
def _(mo):
    mo.md('# Определяем параметры переходной кривой').center()
    return


@app.cell
def _(mo):
    mo.md(r"""
    Забыли о том, что кривизну лучше рассматривать как функцию от длины окружности. Для кривой $y(x)$ длину окружности $l(x)$ можно вычислить по формуле

    $$\int_0^x {\sqrt{1+\left( \frac{dy(x)}{dx}  \right)^2} dx}$$
    """)
    return


@app.cell
def _(smp):
    smp.init_printing()
    l, t, x, y = smp.symbols('l t x y')
    y = x**3
    ys = y.diff(x)
    l = smp.integrate(smp.sqrt(1+ys**2), (t, 0, x))
    l
    return


@app.cell
def _(np, plt, rh, root):
    def visualize_parabola(
        xc=0.38315340372300777,
        x0=0.15441668062767192,
        y0=0.5760693641668141,
        R=0.5675,
        figsize=(4, 4),
        equal = True,
        lw=3, ms=15, fs=10, loc=2
    ):
        def curve_len(x):
            ''' Длина кривой '''
            return x*np.sqrt(1 + 9*x**4)

        def K(x, xc, R):
            '''Кривизна параболы'''
            k = 6*x/(np.sqrt(1+9*x**4))**3
            return np.where(x<xc, k, 1/R)

        slv = root(rh, (xc, x0, y0), args=(R,))
        if slv.success:
            fig = plt.figure(figsize=figsize)
            xc, x0, y0 = slv.x
            yc = xc**3
            n = 1000
            x = np.linspace(-xc, 2 * xc, n) # парабола
            # параметры дуги поворотного круга
            t0 = np.arctan2(yc-y0, xc-x0)
            t1, t2 = t0 - np.pi/4,  t0 + np.pi/4
            t = np.linspace(t1+np.pi/2, t2+np.pi/2, n)        
            xr, yr = R * np.sin(t) + x0, y0 - R * np.cos(t)
            # рисуем
            ax = plt.subplot(111) 
            if equal:
                ax.axis("equal")
            y = np.where(x>0, x**3, 0) # парабола
            line1 = ax.plot(x, y, 'b-', lw=lw, label='парабола')
            ax.plot(xc, xc**3, "b+", ms=ms)
            line2 = ax.plot(xr, yr, 'r-', lw=lw, label="круг")
            ax.grid()
            ax.set_xlabel('x')
            ax.set_ylabel('y(x)')
            ax2 = ax.twinx()
            # кривизна
            x = np.linspace(0, 2 * xc, n)        
            line3 = ax2.plot(x, K(x, xc, R), 'c-', lw=lw, 
                     label=f'К(x)')
            # lxc = curve_len(xc)
            # ##print(f"{lxc=}, {xc=}")
            # xx = np.linspace(0, xc, n)
            # ll = curve_len(xx)
            line4 = ax2.plot(x, K(curve_len(x), xc, R), 'm-', lw=lw, 
                     label=f'К(l(x))') 
            #line5

            ax2.set_ylabel('$K(x), K(l(x))$')
            # выводим легенду
            lines = line1 + line2 + line3 + line4   # линии
            labels = [l.get_label() for l in lines]
            ax.legend(lines, labels, loc=loc, fontsize=fs)        
            plt.tight_layout()        
            plt.title(f"{R=:5.3f}, {xc=:5.3f},{x0=:5.3f},{y0=:5.3f}",
                     fontsize=fs)
            plt.tight_layout()
            return fig, (xc, x0, y0)


    _fig = visualize_parabola(R=0.5675) 
    plt.savefig('01.06.png', dpi=300, facecolor='white')
    _fig
    return (visualize_parabola,)


@app.cell
def _(plt, visualize_parabola):
    _fig = visualize_parabola(R=1.0,xc=0.168, x0=0.08, y0=1., equal=True)
    plt.savefig('01.07a.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(plt, visualize_parabola):
    _fig = visualize_parabola(R=1.0,xc=0.631, x0=1.398, y0=00.389, equal=True)
    plt.savefig('01.07b.png', dpi=300, facecolor='white')
    _fig
    return


if __name__ == "__main__":
    app.run()
