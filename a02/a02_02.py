import marimo

__generated_with = "0.12.8"
app = marimo.App(width="medium")


@app.cell
def _():
    # ячейка 0
    import marimo as mo

    a = 42
    mo.md("""
    # Типы  ячеек блокнота marimo
    Это ячейка Python, но в ней мы можем работать с языком разметки Markdown
    """)
    return a, mo


@app.cell
def _(a, mo):
    # ячейка 1
    mo.md(f"**Значение переменной a={a}**")
    return


if __name__ == "__main__":
    app.run()
