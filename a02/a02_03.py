import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md("""
    # Типы  ячеек блокнота marimo
    """)
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Ячейка Markdown
    В ячейках такого типа могут быть формулы, закодированные с помомю Latex, например, функция ошибок:

    $$erf(x)=\frac{2}{\sqrt{\pi}} \int_0^x e^{-t^2} dt.$$
    """
    )
    return


if __name__ == "__main__":
    app.run()
