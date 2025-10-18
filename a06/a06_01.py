import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md("""# Создаем анимацию
    Для создания анимации нам необходимы:

    1. Функция, которой передается номер кадра i, 
    функция с помощью matplotlib, формирует i-ый кадр.
    2. Задание числа кадров анимации.
    3. Путь к формируемой аниации. Мы будем формировать анимацию в папке public,
    расположенной рядом с блокнотом, формирующим анимацию. Файл должен иметь расширение .gif
    4. Время демонстрации кадра пользователю (duration).
    4. Терпение, так как в анимации много кадров, на их формирование, объединение в анимацию и сохранение в файлой системе нужно время.
    """)
    return (mo,)


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    return np, plt


@app.function
def build_gif_animation(f, nframes, duration=50, fn="public/anim.gif"):
    """
    Построение анимации:
    f- функция, формирующая с помощью matplotlib кадр анимации,
    функции передается номер формируемого кадра.
    duration - время демонстрации кадра анимации в мс.
    nframes - чило кадров в анимации.
    fn - путь к файлу с сохраненной анимацией.
    """
    import gif
    import marimo as mo

    @gif.frame
    def play(i):
        f(i)  # формирование кадра анимации

    frames = []  # последовательность кадров анимации
    # формируем последовательность кадров
    with mo.status.progress_bar(
        total=nframes,
        remove_on_exit=True,
        title="Строим последовательность кадров",
        completion_title="Построили",
    ) as bar:
        for i in range(nframes):
            frames.append(play(i))
            bar.update()

    # сохраняем анимацию
    with mo.status.spinner(title="Сохраняем анимацию...") as _spinner:
        gif.save(frames, fn, duration=duration)
        md_sp = mo.md("**Сохранение gif-анимации успешно заверщено**")
        _spinner.update("Почти сохранено...")
    return mo.image(fn)


@app.cell
def _(mo):
    mo.md("""## Создаем простую gif-анимацию""")
    return


@app.cell
def _(np, plt):
    a0, astep = 0.5, 0.05
    xx = np.linspace(0, 5, 1000)


    def f1(i):
        fig = plt.figure(figsize=(3, 3))
        yy = np.sinc((a0 + astep * i) * xx)
        plt.plot(xx, yy, lw=3)
        plt.title(f"Кадр:{i + 1}")
        plt.ylim(-0.3, 1.1)
        plt.grid()


    build_gif_animation(f1, 100)
    return


@app.cell
def _(mo):
    mo.image('public/anim.gif')
    return


@app.cell
def _(mo):
    mo.md("""## Игра "Жизнь" Конвея""")
    return


@app.cell
def _():
    return


@app.cell
def _(np, plt):
    # Шаг игры
    from scipy.signal import convolve  # свертка

    mask = np.array(
        [[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=bool
    )  # окружение ячейки
    nx = 200  # размерность поля
    extended_field = np.zeros((nx + 2, nx + 2))  # расширенное поле
    field = extended_field[1:-1, 1:-1]  # поле игры
    # начальная расстановка
    field[0, :] = field[-1, :] = 1
    field[:, 0] = field[:, -1] = 1


    def step_of_game(i):
        # замыкание на торе
        extended_field[-1, :] = extended_field[1, :]
        extended_field[0, :] = extended_field[-2, :]
        extended_field[:, -1] = extended_field[:, 1]
        extended_field[:, 0] = extended_field[:, -2]
        # число соседей каждой яейки
        c = convolve(extended_field, mask, method="direct", mode="valid")
        # правила рождения и смрти
        birth_confition = (field == 0) & (c == 3)
        dyeing_condition = (field == 1) & ((c < 2) | (c > 3))
        field[birth_confition] = 1
        field[dyeing_condition] = 0

        fig = plt.figure(figsize=(3, 3))
        plt.imshow(extended_field, cmap="binary")
        plt.axis("off")


    build_gif_animation(step_of_game, 500, duration=50, fn="public/life4.gif")
    return


@app.cell
def _(mo):
    mo.image("public/life4.gif")
    return


if __name__ == "__main__":
    app.run()
