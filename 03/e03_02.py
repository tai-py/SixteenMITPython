import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from decimal import Decimal, getcontext

    mo.md("# Потеря значащих цифр для различных типов данных")
    return mo, np


@app.cell
def _(mo):
    mo.md(r"""## 32-разрядные числа с плавающей точкой (float32)""")
    return


@app.cell
def _(np):
    def get_tolerance_float32(min_value=0.01):
        min_value = np.float32(min_value)
        value = np.float32(1.)
        d10 = np.float32(10.)
        for i in range(12):
            new_value = value + min_value
            if np.abs(value - new_value)<min_value*0.1:
                return value, value - new_value
            value *= d10  

    get_tolerance_float32()
    return


@app.cell
def _(mo):
    mo.md(r"""## 64-разрядные числа с плавающей точкой  (float64)""")
    return


@app.cell
def _(np):
    def get_tolerance_float64(min_value=0.01):
        min_value = np.float64(min_value)
        value = np.float64(1.)
        d10 = np.float64(10.)
        for i in range(30):
            new_value = value + min_value
            if np.abs(value - new_value)<min_value*0.1:
                return value
            value *= d10  

    f"{get_tolerance_float64():6.3e}" 
    return


if __name__ == "__main__":
    app.run()
