import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    mo.md('''# Работаем с мультимедиа в Markdown
    Вставляем  изображения, аудио и видео в блокноты marimo
    ''')
    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Выводим изображение средствами Markdown
    ![Логотип marimo](public/marimo_logo.png)
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Выводим аудио средствами HTML
     <audio controls autoplay muted>
      <source src="public/audio_700KB.mp3" type="audio/mp3">
      Ваш баузер не поддерживает вывод аудио.
    </audio>
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Выводим видео средствами HTML
    <video width="320" height="240" controls>
      <source src="public/attr.mp4" autoplay type="video/mp4">
      Ваш браузер не поддерживает проигрывание видео.
    </video>
    """)
    return


@app.cell
def _(mo):
    logo = mo.image("public/marimo_logo.png", width="50%")
    audio = mo.audio("public/audio_700KB.mp3")
    video = mo.video('public/hd.mp4', width="50%",
                    autoplay=True, loop=True) 

    logo, audio, video
    return audio, logo, video


@app.cell
def _(mo):
    mo.md(r"""
    ## Выводим изображения, аудио и видео  с помощью функции mo.as_html
    """)
    return


@app.cell
def _(audio, logo, mo, video):
    mo.as_html((logo, audio, video))
    return


if __name__ == "__main__":
    app.run()
