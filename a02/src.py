import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from pathlib import Path, PurePosixPath
    import toml

    mo.md("""
    # Достаем данные из запроса и выводим исходный код модуля 

    Обращение:

    `marimo run src.py  -- --p путь_к_файлу`

    или

    `python toc.py` - запускаем  веб-приложение FastAPI

    Обращаемся к конечной точке вывода исходных текстов:

    `http://localhost/src/?p=путь_к_файлу` 

    или извлекаем путь к файлу из `toc.toml`

    или сам файл
    """)
    return Path, PurePosixPath, mo, toml


@app.cell
def _(Path, PurePosixPath, __file__, mo, mp):
    def source_code():
        """
        Выводим исходный текст файла в форматированном виде
        """

        # извлекаем имя файла из параметров, переданных блокноту
        ca = mo.cli_args()  # marimo run src.py -- --p путь_к_файлу
        qp = mo.query_params()

        # print(f"{ca=}, {qp=}")

        if ca and ca["p"]:
            path = str(PurePosixPath(ca["p"]))
        elif qp and qp["p"]:
            path = str(PurePosixPath(qp["p"]))
        else:
            # путь к файлу блокнота
            path = str(PurePosixPath(__file__))

        # проверяем, есть ли такой файл
        if not Path(path).exists():
            return mp.md("**Запрашиваемый файл отсутствует**")

        # выделяем расщирение файла
        k = path.rfind(".")
        ext = "" if k < 0 else path[k + 1 :]
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
            case "js":
                lang = "javascript"
            case "md":
                lang = "markdown"
            case "sql":
                lang = "sql"
            case "json":
                lang = "json"
            case "_":
                lang = ""
        return mo.md(f"""
    ```{lang}
    {text}
    ```
        """)
    return (source_code,)


@app.cell
def _(Path, mo, mp):
    def get_source_code(path: str) -> str:
        """
        Вывод подсвеченного  исходного
        кода файла, заданного
        параметром path - путем в локальной в фаловой системе
        """
        # проверяем, есть ли такой файл
        if not Path(path).exists():
            return mp.md(f"Запрашиваемый файл: **'{path}'** отсутствует")

        # выделяем расщирение файла
        k = path.rfind(".")
        ext = "" if k < 0 else path[k + 1 :]
        ext = ext.lower()

        # читаем файл
        text = ""
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as ex:
            return mo.md(
                f"Ошибка при чтении файла: **'{path}'**. Текст сообщения: {ex}"
            )

        # обрабатываем тип файла
        match ext:
            case "py":
                lang = "python"
            case "js":
                lang = "javascript"
            case "md":
                lang = "markdown"
            case "sql":
                lang = "sql"
            case "json":
                lang = "json"
            case "_":
                lang = ""
        return mo.md(f"""
    ```{lang}
    {text}
    ```
        """)
    return (get_source_code,)


@app.cell
def _(is_str, mo, sc):
    mo.md(f"## Иcходный текст файла: **{sc if is_str else sc.value}**")
    return


@app.cell
def _(Path, PurePosixPath, __file__, mo, toml):
    def source_code_path():
        """
        Функця возвращает путь к файлу, извлекаемый
        1) из параметра p, передаваемой в командной строке
        2) из параметра p веб-запроса
        3) из файла toc.toml, расположенного в той же папке, что их блокнот
        4) исходный код самого блокнота
        Функция возраращает путь к фалу
        """

        # извлекаем имя файла из параметров, переданных блокноту
        ca = mo.cli_args()  # marimo run name.py -- --p имя_файла.file
        # извлекаем данные из веб-запроса
        # marimo run 00_source_code.py?p=путь_к_файлу
        toc = "toc.toml"
        qp = mo.query_params()
        if ca and ca["p"]:
            return str(PurePosixPath(ca["p"]))
        elif qp and qp["p"]:
            return str(PurePosixPath(qp["p"]))
        elif Path(toc).exists():
            # имеется оглавление, извлекаем путь из него
            toc_dict = toml.load(toc)
            toc_dict = toc_dict["Оглавление"]
            options = []
            for key, value in toc_dict.items():
                # print(f"{value} | {value['title']}")
                options.append(value["url"])

            return mo.ui.dropdown(
                options=options,
                value=options[0],
                label="Выберите файл для вывода:",
            )
        else:
            # путь к файлу блокнота
            return str(PurePosixPath(__file__))


    sc = source_code_path()
    is_str = isinstance(sc, str)
    sc if not is_str else None
    return is_str, sc, source_code_path


@app.cell
def _(get_source_code, is_str, sc):
    get_source_code(sc if is_str else sc.value)
    return


if __name__ == "__main__":
    app.run()
