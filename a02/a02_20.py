import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md("# Работаем с toml")
    return (mo,)


@app.cell
def _(mo):
    toc_ = "toc_.toml"
    with open(toc_, "r", encoding="utf-8") as f:
        toc_text = f.read()
    mo.md(f"""
    ## Исходный текст файла {toc_}
    ```
    {toc_text}
    ```
    """)
    return (toc_,)


@app.cell
def _(mo):
    mo.md("""
    ## Непосредственно отображаем загруженный файл **{toc_}**
    """)
    return


@app.cell
def _(toc_):
    import toml
    toc_dict = toml.load(toc_)
    toc_dict
    return (toc_dict,)


@app.cell
def _(mo, toc_, toc_dict):
    mo.output.append(mo.md(f"## Итеририруем содержимое загруженного файла **{toc_}**"))

    for item in toc_dict["Оглавление"].items():
        mo.output.append(mo.md(f"{item[0]}: {item[1]}"))
    return


@app.cell
def _(toc_dict):
    items = []
    for key, value in toc_dict["Оглавление"].items():
        items.append({key: value})
    items
    return


if __name__ == "__main__":
    app.run()
