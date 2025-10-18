import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    mo.md("# Римские и арабские")
    return (mo,)


@app.cell
def _():
    def withdraw(s):
        '''
        Имитация выдачи банкоматом
        набора купюр на сумму s
        Параметры:
        s - выдаваемая сумма
        Функция возвращает последовательность купюр
        '''
        # набор банкнот
        banknotes = {
            '5000 р':5000, '2000 р':2000, '1000 р':1000, 
             '500 р': 500,  '200 р': 200,  '100 р': 100, 
              '50 р':  50,   '10 р': 10 
        }
        # последовательность выдаваемых банкнот
        if s%10:
            print("Выдаются суммы, кратные 10 рублям")
            return []
        seq = []
        for banknote in banknotes:
            nominal = banknotes[banknote]
            if s >= nominal:
                num = s // nominal
                seq += [banknote] * num
                s -= nominal * num

        return seq

    print( withdraw(7120))
    withdraw(7123),  withdraw(18770)  
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Перевод арабских чисел в римские""")
    return


@app.cell
def _():
    def arabic_number_2_roman(a):
        '''
        Перевод арабских чисел в римские.
        Параметры:
        a - арабское число
        Функция возращает строку с 
        переводом числа арабского числа в римское
        '''
        arab_roman_dict = {
            1000: "M", 900: "CM", 500: "D", 400: "CD",
             100: "C",  90: "XC",  50: "L",  40: "XL",
              10: "X",   9: "IX",   5: "V",   4: "IV",
               1: "I", 
        }
        r = ''
        for arab_nominal in arab_roman_dict:
            while a - arab_nominal >= 0:
                r += arab_roman_dict[arab_nominal]
                a -= arab_nominal
        return r

    arabic_number_2_roman(1828)
    return (arabic_number_2_roman,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Перевод римских чисел в арабские методом грубой силы""")
    return


@app.cell
def _(arabic_number_2_roman):
    def roman_number_2_arabic(r):
        n = 10_000
        for i in range(n):
            roman = arabic_number_2_roman(i)
            if roman == r:
                return i
        return "Решение не найдено"


    roman_number_2_arabic('MDCCCXXVIII'),  roman_number_2_arabic('MMDCCCXXVIII')      
    return


if __name__ == "__main__":
    app.run()
