import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md("# Диаграммы Mermaid")
    return (mo,)


@app.cell
def _(mo):
    diag = """
    graph LR    
        A[Трудное решение] --> B{Быть или не быть?}
        B --> C[Быть]
        B --> D[Не быть]  
    """

    mo.mermaid(diag)
    return


@app.cell
def _(mo):
    gantt = """
    gantt
        title Диаграмма Ганта
        dateFormat YYYY-MM-DD
        section Глава 0
            Постановка задачи       :done, 2025-01-10, 3d
            STEAM                   :      2025-01-12, 7d
            Технологии, marimo      :      2025-01-15, 12d
        section Глава 1
            План главы              :crit, 2025-01-13, 3d
            Подготовка скриптов     :5d
            Написание текста        :2025-01-20, 12d
    """

    mo.mermaid(gantt)
    return


@app.cell
def _(mo):
    seq_diag = """
    sequenceDiagram
        Клиент -->> Сервер: Открыть TCP-соединение
        Клиент <<-->> Сервер: Рукопожатие TLS
        Клиент ->> Сервер: Запрос
        Сервер ->> Клиент: Ответ
        #Клиент ->> Сервер: Есть новые запросы?
        #Сервер ->> Клиент: Нет
        Клиент -->> Сервер: Закрыть TCP-соединение   
        Note right of Клиент: Запрос-ответ HTTPS


    """
    mo.mermaid(seq_diag)
    return (seq_diag,)


@app.cell
def _(mo, seq_diag):
    s = mo.mermaid(seq_diag)
    mo.md(f"""
    ## Диаграмма, погруженная в Markdown
    {s}
    """).center()
    return


@app.cell
def _(mo):
    mo.mermaid("""
    mindmap
    root )16 этюдов... (
    """)
    return


@app.cell
def _(mo):
    mo.mermaid("""
    mindmap
    root(marimo)
        Ячейки
          [Реактивные]
          Связанные 
        Особенности
          **Python**
          *Блокноты*
          Гибкие раскладки
        Отображение мультимедиа 
          mo.ui
          mo.md
          mo.mermaid
    """)
    return


@app.cell
def _(mo):
    mo.mermaid("""
    mindmap
    root )**16 занятий...**(
        [**Главы**]  
            1. Математический анализ трамвайных путей
            2. Вычислительный Реннесанс: метод Ньютона
            3. В этом мире нет совершенства...
            4. Криптография и головоломки
            5. Наш старый знакоиый маятник
            6. Мистер Х или немного статистики
            7. Проверить алгеброй геометрию, а заодно и гармонию
            8. Путешествие в мир науки и исскуства на стопоходящей машине Чёбышеап
        [**Приложения**]
            П1. Cоздаём рабочую среду с помощью менеджера пакетов uv
            П2. marimo – не только украшение аквариума
            П3. Краткий обзор языка разметки Мarkdown
            П4. Формулы в блокнотах Jupyter и marimo
            П5. NumPy массивы и изображения
            П6. Анимация    

    """)
    return


if __name__ == "__main__":
    app.run()
