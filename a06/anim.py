#import marimo

import marimo as mo
import gif
#__generated_with = "0.12.5"
#app = mo.App(width="medium")
  

def build_gif_animation_py(f, nframes, duration=50, fn="public/anim.gif"):
    """
    Построение анимации:
    f- функция, формирующая с помощью matplotlib кадр анимации,
    функции передается номер формируемого кадра.
    duration - время демонстрации кадра анимации в мс.
    nframes - чило кадров в анимации.
    fn - путь к файлу с сохраненной анимацией.
    """


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
