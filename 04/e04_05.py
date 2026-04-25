import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    from time import perf_counter as pfc
    from itertools import permutations

    mo.md("# Буквенная головоломка")
    return np, permutations, pfc


@app.cell
def _(np):
    def check_solution(a, op, b, c):
        '''
        Проверяем корректность решения задачи
        a @ b = c,
        где a, b, c - целые числа
        @ - арифметическая операция: +, -, *  
        Функция возвращает True, если решение найдено    
        '''
        if op=='+':
            r = a + b
        elif op=="-":
            r = a - b
        elif op=="*":
            r = a*b
        else:
            r = np.nan # нераспознання операция дает результат "не число (nan)"
        return r == c

    (check_solution(123, '+', 456, 579), check_solution(456, '-', 123, 333),
     check_solution(16, '*', 16, 256))
    return (check_solution,)


@app.cell
def _(check_solution):
    check_solution(16, '/', 16, 1)
    return


@app.cell
def _():
    from itertools import combinations

    print((list(combinations([0,1,2,3,4,5,6,7,8, 9], 3))), end=" ")
    return


@app.cell
def _(permutations):


    perm = permutations([0,1, 2, 3, 4, 5, 6, 7, 8, 9], 2)

    #len(tuple(perm)) 
    return (perm,)


@app.cell
def _(perm):
    print(tuple(perm))
    return


@app.cell
def _():
    def str_2_number(s, d):
        '''
        Перевод строки s в число result.
        Сопоставление символов строки цифрам в словаре s
        '''
        result = 0 
        for i, c in enumerate(s[::-1]):
            result += d[c]*10**i
        return result

    str_2_number('abc', {'a':1, 'b':2, 'c':3})
    return (str_2_number,)


@app.cell
def _(check_solution, permutations, pfc, str_2_number):
    def solve_word_puzzle(one, op, two, result):
        op_in = op  in '+', '-', '*'
        if not op_in:
            raise ValueError(f"Некорректная операция op:{op}")

        time_stamp = pfc()
        # набор цифр
        digits = (0,1,2,3,4,5,6,7,8,9)
        # уникальные символы, входящие в головоломку
        # подзадача 3
        symbols = list(set(one + two + result))
        symbols_len = len(symbols) 
        #print(f"{symbols=}, {symbols_len=}")
        # максимальная длина слова в головоломке
        max_len = max(len(one), len(two), len(result))
        #print(f"{max_len=}")
        # генерируем все перестановки символов длиной max_len
        # подзадача 4
        prm = permutations(digits, symbols_len)
        #print(f"{len(tuple(prm))=}")
        solution = [] # решение задачи

        # пятая подзадача
        for p in prm:
            # сопоставляем  символам symbols цифры из p
            # в словаре d 
            d = dict(zip(symbols, p))
            #print(f"{p=}, {d=}")

            # превращаем строки в числа
            # подзадача 2
            number_one = str_2_number(one, d)
            number_two = str_2_number(two, d)
            number_result = str_2_number(result, d)

            # подзадача 1
            if check_solution(number_one, op, number_two, 
                                number_result):
                # сохраняем решение головоломки
                r = {'сопоставление_символов_и_цифр:':list(d.items()),
                     "первое_число": number_one,
                     "операция": op,
                     "второе_число": number_two,
                     "результат": number_result,
                    }
                solution.append(r)            

        elapsed_time = pfc() - time_stamp    
        print(f"{elapsed_time=:6.3e} c")
        return solution, elapsed_time


    solutions =  solve_word_puzzle("USA", '+', "USSR", "PEACE")  
    print(solutions)
    #solve_word_puzzle("ab", '+', "ba", "cc")  
    return (solve_word_puzzle,)


@app.cell
def _(solve_word_puzzle):
    solution2 = solve_word_puzzle("USA", '+', "IRAN", "PEACE") 
    print(solution2)
    return (solution2,)


@app.cell
def _(solution2):
    print(f"Число решений: {len(solution2[0])}")
    return


if __name__ == "__main__":
    app.run()
