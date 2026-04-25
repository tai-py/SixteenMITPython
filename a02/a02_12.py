import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md("# Работаем с элементами пользовательского интерфейса")
    return (mo,)


@app.cell
def _(mo):
    btn = mo.ui.button(label="Нажми меня", kind='success', 
                 tooltip="Кнопка с надписью 'Нажми меня'")
    chk = mo.ui.checkbox(label="Флажок", value=True)
    data = mo.ui.date(label="Задаем дату: ", start="2025-03-09", stop="2025-03-18", value="2025-03-14")
    data_range =mo.ui.date_range(label="Задаем диапазон дат: ", start="2025-03-09", stop="2025-03-18")
    date_time = mo.ui.datetime(label="Задание даты/времени: ")
    dropdown = mo.ui.dropdown(label="Выпадающее меню: ", options=("раз","два", "три", "четыре"), value="три")
    multi_select = mo.ui.multiselect(label="Множественный выбор: ", 
                                     options=("раз","два", "три", "четыре"), 
                                     value=["три", "раз"])
    number = mo.ui.number(label="Ввод числа: ", start=1, stop=15, step=2, value=5 )
    radios = mo.ui.radio(label="Набор переключателей:", options=("раз","два", "три", "четыре"), value="три")
    range_slider = mo.ui.range_slider(label="Выбор диапазона: ", start=1, stop=20, step=1, value=[5, 15])
    slider = mo.ui.slider(label="Слайдер: ", start=0., stop=1., step=0.05, value=0.8)
    switch = mo.ui.switch(label="Переключатель: ", value=True)
    text = mo.ui.text(label="Поле ввода: ", placeholder="Введите текст")
    text_area = mo.ui.text_area(label="Текствая область: ", rows=6,
                    value="Текст в текстовой области...")

    (mo.md("## Аналоги элементов управления JN, JL"),
     mo.hstack([btn, chk, data]), 
     mo.hstack([data_range, date_time]),
     mo.hstack([dropdown, multi_select, number]),
     mo.hstack([radios, range_slider, slider]),  
     mo.hstack([switch, text, text_area]), 
    )
    return


@app.cell
def _(mo):
    with open('a02_09.py', encoding="utf-8") as f:    
        source_text = f.read()
    mo.ui.code_editor(label="### Редактор кода", value=source_text, 
                      language="python")
    return


@app.cell
def _(mo):
    from plotly.express.data import iris

    df = iris()
    mo.ui.dataframe(df)
    return (df,)


@app.cell
def _(df, mo):
    mo.ui.table(data=df, label="## Пример таблицы", selection="multi")
    return


@app.cell
def _(df, mo):
    mo.ui.data_explorer(df)
    return


@app.cell
def _(mo):
    mo.ui.file_browser(label="## Просмотр файлов")
    return


@app.cell
def _(mo):
    mo.ui.file(label="Кнопка для загрузки файла")
    return


@app.cell
def _(mo):
    frm = mo.ui.text_area(placeholder="...").form(label="Текстовая область в форме",
                                           submit_button_label="Нажми").callout()
    frm
    return


@app.cell
def _(mo):
    mo.ui.microphone(label="Скажи что-нибудь...")
    return


@app.cell
def _(mo):
    refresh = mo.ui.refresh(label="Кнопка обновления", options=["1s", "2s", "5s", '10s'], default_interval="5s")
    return (refresh,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Кнопка обновления
    """)
    return


@app.cell
def _(mo, refresh):
    mo.md(f"""
    {refresh}, число обновлений: {refresh.value}
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Кнопки запуска
    """)
    return


@app.cell
def _(mo):
    btn1 = mo.ui.run_button(label="Кнопка запуска 1")
    btn2 = mo.ui.run_button(label="Кнопка запуска 2")
    btn1, btn2
    return btn1, btn2


@app.cell
def _(btn1, btn2):
    if btn1.value:
        print("Нажата кнопка 'Кнопка запуска 1'")
    elif btn2.value:
        print("Нажата кнопка 'Кнопка запуска 2'")
    else:
        print("Нажми любую кнопку")
    return


@app.cell
def _(df, mo):
    tbl = mo.ui.table(data=df, label="## Пример таблицы", selection="multi") 
    tbl
    return (tbl,)


@app.cell
def _(tbl):
    tbl.value
    return


@app.cell
def _(mo):
    tabs = mo.ui.tabs(label="## Пример вкладок", 
                     tabs = {
                         'Вкладка1': [mo.ui.slider(start=0, stop=100, value=42)],
                         'Вкладка2': [mo.ui.number(value=42)],
                         'Вкладка3': [mo.ui.text_area(placeholder="Введите текст...")],             
                     }, value = 'Вкладка3',

    )
    tabs, mo.defs(), mo.refs()
    return


if __name__ == "__main__":
    app.run()
