import marimo

__generated_with = "0.11.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md("""
    # Достаем данные из запроса и выводим исходный код модуля 
    Обращение:

    `marimo run source_code.py  -- --p путь_к_файлу`
    """)
    return (mo,)


@app.cell
def _(__file__, mo, mp):
    from pathlib import Path, PurePosixPath

    def source_code():
        '''
        Выводим исходный текст файла в форматированном виде
        '''  

        # извлекаем имя файла из параметров, переданных блокноту
        ca = mo.cli_args() # marimo run name.py -- --p имя_файла.file 
        qp = mo.query_params()
        if (ca and ca['p']):
            path = str(PurePosixPath(ca['p']))
        elif (qp and qp['p']):
            path = str(PurePosixPath(qp['p']))
        else:
            # путь к файлу блокнота 
            path =  str(PurePosixPath(__file__)) 

        # проверяем, есть ли такой файл
        if not Path(path).exists():
            return mo.md("**Запрашиваемый файл отсутствует**")

        # выделяем расщирение файла
        k =  path.rfind('.')
        ext = "" if k<0 else path[k+1:]
        ext = ext.lower()

        # читаем файл
        text = ""
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()        
        except Exception as ex:
            return mo.md(f"Ошибка при чтении файла: {ex}")

        # обрабатываем тип файла
        match ext:
            case "py":
                lang = "python"
            case 'js':
                lang = "javascript"
            case 'md':
                lang = "markdown"
            case 'sql':
                lang = 'sql'
            case 'json':
                lang = 'json'
            case '_':
                lang = ''     
        return mo.md(f"""
    ```{lang}
    {text}
    ```
        """)

    source_code()
    return Path, PurePosixPath, source_code


if __name__ == "__main__":
    app.run()
