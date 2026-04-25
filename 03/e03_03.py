import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from decimal import Decimal, getcontext

    mo.md("# Работаем с десятичными числами")
    return Decimal, getcontext, mo, np, plt


@app.cell
def _(getcontext):
    print(getcontext())
    return


@app.cell
def _(Decimal, getcontext):
    def get_decimal_tolerance(prec=6, min_value='0.01'):
        getcontext().prec = prec # число значащих цифрр
        min_value = Decimal(min_value)
        value = Decimal('1')
        d10 = Decimal('10')
        for i in range(120):
            if value == (value + min_value):
                return value
            value *= d10 

    prec = getcontext().prec
    _r = get_decimal_tolerance(prec=prec)   
    print(f"{prec=}, {_r=:6.3e}")
    return (get_decimal_tolerance,)


@app.cell
def _(get_decimal_tolerance, plt):
    # определяем, где теряется копейка для данной разрядности
    precs =[3, 5, 6, 7, 8, 10, 12, 15, 20, 28]
    vals = []
    for _prec in precs:
        v = get_decimal_tolerance(prec=_prec)
        vals.append(v)

    _fig = plt.figure(figsize=(5, 3))
    plt.plot(precs, vals, lw =3)
    #plt.xscale('log')
    plt.yscale('log')
    plt.grid()
    plt.xlabel('Число значащих цифр')
    plt.ylabel('Когда теряется копейка')
    plt.tight_layout()
    plt.savefig("03_03.png", dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Проводим округление десятичных чисел
    """)
    return


@app.cell
def _(Decimal):
    print(
        Decimal('1.49').to_integral_value(),
        Decimal('1.5').to_integral_value(),
        Decimal('1.51').to_integral_value(),
        Decimal('2.49').to_integral_value(),
        Decimal('2.5').to_integral_value(),
        Decimal('2.51').to_integral_value()
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Подсчитываем баланс на большом числе транзакций
    """)
    return


@app.cell
def _(Decimal, getcontext, np):
    def balance(start=1e14, transactions=10_000, 
                maxsum=10_000_000, prec=50):
        getcontext().prec = prec
        decimals = Decimal('0')
        floats = np.float64(start)
        for i in range(transactions):
            roubles = np.random.randint(maxsum//2, maxsum)
            kops = np.random.randint(0, 99)
            sign = "" if np.random.randint(0,2) else "-"
            d = Decimal(f"{sign}{roubles}.{kops}")
            decimals += d
            floats +=np.float64(d)
            #print(f"{i=}, {sign=} {d=}, {decimals=}, {floats=}, {floats - start}")
        result = Decimal(floats) - Decimal(start) - decimals
        return result

    balance(start=1e12, transactions=1_000_000)
    return (balance,)


@app.cell
def _(balance):
    balance(start=1e13, transactions=1_000_000)
    return


if __name__ == "__main__":
    app.run()
