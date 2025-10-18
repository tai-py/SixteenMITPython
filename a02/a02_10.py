import marimo

__generated_with = "0.11.20"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import plotly.express as px

    mo.md("# Научная визуализация с помощью plotly")
    return mo, np, pd, px


@app.cell
def _(pd, px):
    df = pd.DataFrame({"x":[0, 1, 4, 9, 16, 25], 
                       "y":[0, 1, 2, 3, 4, 5]})

    fig = px.scatter(df, x="x", y="y", color="y",
                     width=600, height=400)
    fig.update_traces(marker=dict(size=12, line=dict(width=2,
                      color='DarkSlateGrey')),
                      selector=dict(mode='markers'))
    fig
    return df, fig


@app.cell
def _(fig, mo):
    mo.md(f"""
    ## Интегрируем график plotly в Markdown 
    {mo.as_html(fig)}
    """).center()
    return


@app.cell
def _(mo):
    mo.md("""## Выводим трехмерные графики с помощью plotly""")
    return


@app.cell
def _(np):
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
    return trefoil, trefoil_curve_surface


@app.cell
def _(mo, pd, px, trefoil_curve_surface):
    xc, yc, zc, xs, ys, zs = \
        trefoil_curve_surface(n=300, rmin=-1, rmax=3, wmax=5)

    df_trefoil_curve = pd.DataFrame({"x":xc, "y":yc, "z":zc})
    fig_tc = px.line_3d(df_trefoil_curve, x="x", y="y", z="z")
    fig_tc.update_traces(line=dict(color="darkblue", width=7.))
    fig_tc.update_layout(width=600, height=500)

    mo.md(f"""## Трилистник - трехмерная кривая 
    {mo.as_html(fig_tc)}
    """).center()
    return df_trefoil_curve, fig_tc, xc, xs, yc, ys, zc, zs


@app.cell
def _(mo, xs, ys, zs):
    import plotly.graph_objects as go

    fig_ts = go.Figure(data=[go.Surface(x=xs, y=ys, z=zs)]) 
    mo.md(f"""## Трилистник - трехмерная поверхность 
    {mo.as_html(fig_ts)}
    """).center()
    return fig_ts, go


if __name__ == "__main__":
    app.run()
