import marimo

__generated_with = "0.12.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from anim1 import build_gif_animation
    import matplotlib.pyplot as plt
    import numpy as np
    return build_gif_animation, mo, np, plt


@app.cell
def _(build_gif_animation, np, plt):
    a0 = 0.5
    astep = 0.05
    xx = np.linspace(0, 5, 600)

    def f1(i):
        fig = plt.figure(figsize=(3, 3))
        yy = np.sinc((a0 + astep * i) * xx)
        plt.plot(xx, yy, lw=3)
        plt.title(f"Кадр:{i + 1}")
        plt.ylim(-0.3, 1.1)
        plt.grid()


    build_gif_animation(f1, 100)
    return a0, astep, f1, xx


@app.cell
def _(f1):
    from anim2 import build_gif_animation_py

    build_gif_animation_py(f1, 200)
    return (build_gif_animation_py,)


if __name__ == "__main__":
    app.run()
