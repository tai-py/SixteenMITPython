import marimo

__generated_with = "0.11.26"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md("# Навигационное меню и боковая панель")
    return (mo,)


@app.cell
def _(mo):
    menu = {
        f" {mo.icon('lucide:home')} **marimo**": {
            "/marimo/notebook": {
                "description": "Пользовательский интерфейс блокнота marimo",
                "label": f" {mo.icon('lucide:notebook-text')} Блокнот marimo",
            },
            "/marimo/reactive": {
                "description": "Реактивность переменных блокнотов marimo",
                "label": f" {mo.icon('lucide:rocket')} Реактивность",
            },
            "/marimo/widgets": {
                "description": "Элементы пользовательского интерфейса marimo",
                "label": f" {mo.icon('lucide:monitor')} Виджеты",
            },
            "/marimo/deploy": {
                "description": "Встраивание приложений marimo в веб-приложения",
                "label": f" {mo.icon('lucide:goal')} Встраивание",
            },
        }
    }

    nav_menu = mo.nav_menu(
        menu,
        orientation="vertical",
    )

    nav_menu
    return menu, nav_menu


@app.cell
def _(menu, mo):
    mo.vstack([
        mo.nav_menu(menu,    orientation="horizontal"),
        mo.ui.text_area(placeholder="Введите подсказку...", rows=6)
    ])
    return


@app.cell
def _(menu, mo):
    mo.sidebar(item=mo.nav_menu(menu=menu, orientation="vertical"),
               width="18rem")
    return


if __name__ == "__main__":
    app.run()
