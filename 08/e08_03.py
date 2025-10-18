import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    mo.md("# Механизм для рисования")
    return mo, np, plt


@app.cell
def _(np):
    def circle(a, r=10):
        # окружность
        return r* np.cos(a), r*np.sin(a)

    def square(alpha, r=1):
        # квадрат
        # 0<=a<=8
        a = alpha/(2*np.pi)*8 
        a = a % 8
        # print(f"{np.min(a)=}, {np.max(a)=}")
        # print(f"{np.min(alpha)=}, {np.max(alpha)=}")

        x, y = np.asarray(a), np.asarray(a)
        #x[:], y[:] = -5, -5
        x = np.where(a<=1, r, x)
        y = np.where(a<=1, r*a, y)

        x = np.where((a>1) & (a<=3), r - r*(a-1), x)
        y = np.where((a>1) & (a<=3),  r, y) 

        x = np.where((a>3) & (a<=5), -r, x)
        y = np.where((a>3) & (a<=5),  r - r*(a - 3), y)  

        x = np.where((a>5) & (a<=7),  -r + r*(a -5), x)
        y = np.where((a>5) & (a<=7),  -r, y)  

        x = np.where(a>7,  r, x)
        y = np.where(a>7, -r + r*(a -7) , y) 

        return x, y

    return (square,)


@app.cell
def _(np, square):
    def mech(t0=30, fi=30,  n=1000,alpha=1, beta=1, r1=10, r2=10,
             l02=25., l14=20., l34=20.):
        ind = int(t0/180*n)%n
        x0, y0 = 0., 0. # точка 0
        t = np.linspace(0, 2*np.pi, n)
        # точка 1
        x1, y1 = r1*np.cos(alpha*t), r1*np.sin(alpha*t)
        x1t, y1t = x1[ind], y1[ind]
        x2, y2 = l02, 0. # точка 2
        # точка 3
        x3, y3 = (x2 + r2*np.cos(beta*t + fi/180*np.pi), 
                  r2*np.sin(beta*t + fi/180*np.pi))
        x3, y3  = square(beta*t + fi/180*np.pi, r=r2)
        x3 += x2
        x3t, y3t = x3[ind], y3[ind]
        l13 = np.sqrt((x1 - x3)**2 + (y1 - y3)**2)
        # координата повернутой точки x
        x4s = (l13**2 - l34**2 + l14**2)/(2*l13)
        y4s = np.sqrt(np.abs(l14**2 - x4s**2))
        gamma = np.arctan2(y3-y1, x3-x1) 
        delta = np.arctan2(y4s, x4s) 
        nu = gamma - delta
        x4, y4 = x1 + l14*np.cos(nu),  y1 + l14*np.sin(nu)
        #x4, y4 = x1 + l14*np.sin(gamma),  y1 + l14*np.cos(gamma)
        x4t, y4t = x4[ind], y4[ind]
        l14s = np.sqrt((x1t - x4t)**2 + (y1t - y4t)**2)
        l34s = np.sqrt((x3t - x4t)**2 + (y3t - y4t)**2)
        #print(f"{l14s=}, {l34s=}")

        return (x0, y0, x1, y1, x2, y2, x3, y3, x4, y4,
                x1t, y1t, x3t, y3t, x4t, y4t)



    return (mech,)


@app.cell
def _(mech, plt):
    def paint_mech(t0=30, fi=0, n=1000,alpha=1, beta=1, r1=15, r2=15,
                    l02=30., l14=40., l34=40.,
                    figsize=(6, 6), ms=5, lw1=1, lw2=3,
                    fs=8,pad=2):
        (x0, y0, x1, y1, x2, y2, x3, y3, x4, y4,
                x1t, y1t, x3t, y3t, x4t, y4t) = mech(t0= t0, fi=fi,  n=n, alpha=alpha, 
                beta=beta, r1=r1, r2=r2,
                l02=l02, l14=l14, l34=l34) 
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(x0, y0, 'ko', ms=ms)    
        ax.plot([x0, x2], [y0,y2], 'k-', lw=lw1)    
        ax.plot(x2, y2, 'ko', ms=ms)
        # окружности
        ax.plot(x1, y1, 'b--', lw=lw1)
        ax.plot(x3, y3, 'b--', lw=lw1)
        # радиусы
        ax.plot([x0,x1t], [y0, y1t], 'k-', lw=lw1)
        ax.plot(x1t, y1t, 'ko', ms=ms)
        ax.plot([x2,x3t], [y2, y3t], 'k-', lw=lw1)
        ax.plot(x3t, y3t, 'ko', ms=ms)
        # точка 4
        ax.plot(x4t, y4t, 'ro', ms=ms)
        # соединяющие линии
        ax.plot([x1t, x4t], [y1t, y4t], 'k-', lw=lw1)
        ax.plot([x3t, x4t], [y3t, y4t], 'k-', lw=lw1)
        # траектория точки 4
        ax.plot(x4, y4, 'r-', lw=lw2)
        ax.set_aspect(1)
        # надписи
        ax.text(x0+pad, y0+pad, '0', fontsize=fs)
        ax.text(x1t+pad, y1t+pad, '1', fontsize=fs)
        ax.text(x2+pad, y2+pad, '2', fontsize=fs)
        ax.text(x3t+pad, y3t+pad, '3', fontsize=fs)
        ax.text(x4t+pad, y4t+pad, '4', fontsize=fs)
        plt.axis('off')
        return ax

    paint_mech(t0=60, fi=0, n=500, 
               alpha=1., beta=1, r1=15, r2=15,
               l02=30, l14=40,  l34=40)

    return (paint_mech,)


@app.cell
def _(mo):
    tlt = mo.md("# Кинематический механизм").center() 
    t0 = mo.ui.slider(label='t0', start=0, stop=360, value=30,
                      debounce=False, show_value=True, full_width=True)
    fi = mo.ui.slider(label='fi', start=0, stop=360, value=0,
                      debounce=True, show_value=True, full_width=True)
    alpha = mo.ui.slider(label='alpha', start=1, stop=3, value=1,
                      debounce=True, show_value=True, full_width=True)
    beta = mo.ui.slider(label='beta', start=1, stop=3, value=1,
                      debounce=True, show_value=True, full_width=True)                 
    l02 = mo.ui.slider(label='l02', start=10, stop=100, value=30,
                      debounce=True, show_value=True, full_width=True)
    l14 = mo.ui.slider(label='l14', start=10, stop=100, value=30,
                      debounce=True, show_value=True, full_width=True)
    l34 = mo.ui.slider(label='l34', start=10, stop=100, value=30,
                      debounce=True, show_value=True, full_width=True)
    figsize = mo.ui.slider(label='size', start=3, stop=15, value=6,
                      debounce=True, show_value=True, full_width=True)
    ui = mo.vstack([t0, fi, alpha, beta, l02, l14, l34, figsize]) 
    return alpha, beta, fi, figsize, l02, l14, l34, t0, tlt, ui


@app.cell
def _(alpha, beta, fi, figsize, l02, l14, l34, paint_mech, t0):
    pic = paint_mech(t0=t0.value, fi=fi.value, 
                alpha=alpha.value, beta=beta.value,                 
                l02=l02.value, l14=l14.value, l34=l34.value,
                figsize=(figsize.value, figsize.value))
    return (pic,)


@app.cell
def _(mo, pic, tlt, ui):
    mo.vstack([tlt, mo.hstack([ui, pic],justify="space-around")])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
