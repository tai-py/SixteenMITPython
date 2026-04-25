import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    mo.md('''
    # Текстовые выделения в Markdown
    ## Подробности
    ''')
    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    /// details | Разворачиваемая заметка

    Дополнительное описание заметки, отображаемое при развертывании.
    ///

    /// details | Разворачиваемая заметка типа info
            type: info

    Дополнительное описание заметки типа info, отображаемое при развертывании.
    ///

    /// details | Разворачиваемая заметка типа warn
        type: warn

    Дополнительное описание заметки типа warn, отображаемое при развертывании.
    ///

    /// details | Разворачиваемая замечтка типа danger
        type: danger

    Дополнительное описание заметки типа danger, отображаемое при развертывании.
    ///
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    /// attention | Внимание!

    Это замечание является важным,
    уделите ему внимание!
    ///
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    /// admonition | Совет

    Эта заметка может быть советом, напоминанием или
    предупреждением.
    ///
    """)
    return


if __name__ == "__main__":
    app.run()
