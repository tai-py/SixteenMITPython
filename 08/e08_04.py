import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    mo.md("# Спирограф").center()
    return mo, np, plt


@app.cell
def _(np):
    def spirograph(ax, R=1., r=0.75, ρs=(1.25, 1., .75, 0.5, .25), 
                   T=10, n = 1000,  lw=3 
                  ): 
        r = r if abs(r)>0.1 else 0.05*np.sign(r)
        a = (R-r, r/R) 
        b = (1, -R/r+1)
        t = np.linspace(0, 2*np.pi*T, n) 
        m = len(ρs)
        z = np.zeros((n, m), dtype=np.complex128)
    
        for i in range(m): 
            z[:, i] = a[0]*np.exp(1j*b[0]*t) +\
                      a[1]*ρs[i]*np.exp(1j*b[1]*t)
        
    
        ax.set_aspect(1)
        for i in range(m):         
            ax.plot(z[:, i].real, z[:,i].imag, lw=lw,
                     label=f'ρ={ρs[i]:5.3f}')
        
        ax.legend() 
        ax.set_title(f"{R=}, {r=}")
        ax.axis('off')


    return (spirograph,)


@app.cell
def _(plt, spirograph):
    fig, ax = plt.subplots(nrows=2, ncols=2,figsize=(10, 10)) 
    rs = ((.9, 0.75), (0.7, 0.3))
    for i in range(2):
        for j in range(2):
            spirograph(ax[i, j], r=rs[i][j], lw=3)
    plt.tight_layout()
    plt.savefig('08_12.png', dpi=300, facecolor="white")
    fig
    return


@app.cell
def _(plt, spirograph):
    def paint_curves(r, figsize=(6,6)):
        fig, ax = plt.subplots(figsize=figsize)
        spirograph(ax, r)
        return fig
    return (paint_curves,)


@app.cell
def _(mo):
    r = mo.ui.slider(label="r:", start=.1, stop=1.5, step=0.1, value=1., debounce=True,show_value=True)
    return (r,)


@app.cell
def _(mo, paint_curves, r):
    mo.vstack([r, paint_curves(r.value, figsize=(12,12))])
    return


if __name__ == "__main__":
    app.run()
