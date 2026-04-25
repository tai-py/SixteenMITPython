import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md("""
    # Исходный текст программ в Markdown
    """)
    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    ```sql
    select column1, column2 from df
    ```
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ```python
    import plotly.express as px

    vv = np.linspace(-np.pi, 3 * np.pi, 300)
    xtr, ytr, ztr = trefoil(vv, vv, r=5)
    figtr = px.line_3d(x=xtr, y=ytr, z=ztr)
    figtr.update_traces(line={"width": 15})
    plotly_fig = mo.ui.plotly(figtr)
    ```
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    В Markdown же можно кодировать исходный текст на раздичных языках программирования, заключенный  в тройных обратных апострофах.
    Например, SQL:
    ```sql
    select column1, column2 from df
    ```
    Аналогично кодируется исходный текст на JavaScript и Python:
    ```python
    import plotly.express as px

    vv = np.linspace(-np.pi, 3 * np.pi, 300)
    xtr, ytr, ztr = trefoil(vv, vv, r=5)
    figtr = px.line_3d(x=xtr, y=ytr, z=ztr)
    figtr.update_traces(line={"width": 15})
    plotly_fig = mo.ui.plotly(figtr)
    ```
    """)
    return


if __name__ == "__main__":
    app.run()
