import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from collections import Counter
    import numpy as np
    import matplotlib.pyplot as plt


    mo.md("# Шифр Цезаря")
    return Counter, mo, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Частотный анализ символов в литературных произведениях
    """)
    return


@app.cell
def _(Counter):
    def load_texts(paths):
        counter = Counter()
        for path in paths:
            # читаем очередной файл с текстом
            with open(path, "r", encoding="utf-8") as f:
                txt = f.read()
                counter.update(txt)

        return counter


    symbols = load_texts(
        [
            "./texts/catch22.txt",
            "./texts/russian_nouns.txt",
            "./texts/Tolstoy_Lev_Voyna_i_mir_1-2.txt",
            "./texts/Tolstoy_Lev_Voyna_i_mir_3-4.txt",
        ]
    )
    symbols
    return (symbols,)


@app.cell
def _(symbols):
    # Набор символов
    symbols.keys()
    return


@app.cell
def _(symbols):
    # Число вхожденией символов
    symbols.values()
    return


@app.cell
def _(symbols):
    symbols_number = sum(list(symbols.values()))
    unique_symbols = len(symbols)
    print(f"Число загруженных символов: {symbols_number}")
    print(f"Число уникальных символов: {unique_symbols}")
    return (symbols_number,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Конструируем словарь частот символов
    """)
    return


@app.cell
def _(symbols, symbols_number):
    symbol_dict = {}
    for s in symbols:
        symbol_dict[s] = symbols[s] / symbols_number

    sorted_symbol_dict = dict(
        sorted(symbol_dict.items(), key=lambda item: item[1], reverse=True)
    )
    print(list(sorted_symbol_dict.keys()))
    return (sorted_symbol_dict,)


@app.cell
def _(sorted_symbol_dict):
    print(list(sorted_symbol_dict.values()))
    return


@app.cell
def _(plt, sorted_symbol_dict):
    _fig = plt.figure(figsize=(15, 6))
    _n = 50
    plt.bar(
        list(sorted_symbol_dict.keys())[:_n],
        list(sorted_symbol_dict.values())[:_n],
    )
    plt.xlabel("Символы")
    plt.ylabel("Частоты вхождения символов")
    plt.savefig("04_04.png", dpi=300, facecolor="white")
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Кумуллятивное распредение
    """)
    return


@app.cell
def _(plt, sorted_symbol_dict):
    c_sum = 0.0
    cum_sorted_symbol_dict = {}
    for _ in sorted_symbol_dict:
        c_sum += sorted_symbol_dict[_]
        cum_sorted_symbol_dict[_] = c_sum

    _fig = plt.figure(figsize=(15, 6))
    _n = 50
    plt.bar(
        list(cum_sorted_symbol_dict.keys())[:_n],
        list(cum_sorted_symbol_dict.values())[:_n],
    )
    plt.xlabel("Символы")
    plt.ylabel("Частоты вхождения символов")
    plt.savefig("04_05.png", dpi=300, facecolor="white")
    _fig
    return (cum_sorted_symbol_dict,)


@app.cell
def _(cum_sorted_symbol_dict):
    _cs = list(cum_sorted_symbol_dict)
    (
        cum_sorted_symbol_dict[_cs[10]],
        cum_sorted_symbol_dict[_cs[20]],
        cum_sorted_symbol_dict[_cs[30]],
        cum_sorted_symbol_dict[_cs[50]],
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Сортированные по возрастанию кодов  символы
    """)
    return


@app.cell
def _(symbols):
    sorted_symbols = sorted(list(symbols.copy().keys()))
    print(f"{sorted_symbols=}, {len(sorted_symbols)=}")
    return (sorted_symbols,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Зашифрование, расшифрование
    """)
    return


@app.cell
def _(sorted_symbols):
    def ceaser(open_text, symbols, key=3):
        """
        Шифр Цезаря
        Параметры:
        open_text - открытый текст
        symbols - набор символов
        key - секретный ключ

        Функция возвращает зашифрованный текст
        """
        symbols_dict = {s: i for i, s in enumerate(symbols)}
        symbols_len = len(symbols)
        сipher_text = ""

        for s in open_text:
            сipher_text += symbols[(symbols_dict[s] + key) % symbols_len]

        return сipher_text


    _key = 3
    _сipher_text = ceaser("12345", sorted_symbols, key=_key)
    _open_text = ceaser(_сipher_text, sorted_symbols, key=-_key)

    _сipher_text, _open_text
    return (ceaser,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Шифруем и расшифровываем роман "Уловка 22"
    """)
    return


@app.cell
def _():
    # Загружаем текст
    with open("./texts/catch22.txt", "r", encoding="utf-8") as f:
        catch22 = f.read()

    catch22[:100], len(catch22)
    return (catch22,)


@app.cell
def _(catch22, ceaser, sorted_symbols):
    key = 42  # задачем ключ
    cipher_catch22 = ceaser(catch22, sorted_symbols, key=key)
    print(f"Первые 100 символов зашифрованного текста:\n{cipher_catch22[:100]}")
    return (cipher_catch22,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Пытаемся расшифровать текст методом грубой, предполагая, что он зашифрован цифром Цезаря, а где-то в тексте присутствует имя главного героя Йоссариан (иначе нам пришлось бы вручную просматривать каждый расшифрованный текст)
    """)
    return


@app.cell
def _(ceaser, cipher_catch22, sorted_symbols):
    from time import perf_counter as pfc

    time_stamp = pfc()
    key_ = -1
    for k in range(len(sorted_symbols)):
        open_text_ = ceaser(cipher_catch22, sorted_symbols, key=-k)
        if "Йоссариан" in open_text_:
            key_ = k
            break

    t = pfc() - time_stamp
    if k >= 0:
        print(f"Ключ найден: {key_=}, время счета {t:6.3f} c")
    else:
        print(f"Ключ не найден, время счета {t:6.3f} c")
    return (pfc,)


@app.cell
def _():
    8.208 * 181 / 42
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Алгоритм Вернама (одноразовые блокноты)
    """)
    return


@app.cell
def _(sorted_symbols):
    from random import SystemRandom 

    def one_time_pad(symbols=sorted_symbols, l=1_000_000):
        '''
        Генерация одноразового блокнота
        (последовательности сдвигов)
        Параметры:
        symbols - набор символов
        l - размер одноразового блокнота
        Функция возвращает одноразовый блокнот:
        список из l случайных чисел в диапазоне [rng[0], rng[1]]
        '''
        sr = SystemRandom()
        return  [sr.randrange(1, len(symbols)) for _ in range(l)]

    pad = one_time_pad()
    min(pad), max(pad), len(pad)
    return (one_time_pad,)


@app.cell
def _(sorted_symbols):
    def vernam(open_text, pad, symbols=sorted_symbols, encrypt = True):
        '''
        Зашифрование / расшифрования с помощью алгоритма Вернама
        Параметры:
        open_text - преобразуемый текст
        pad - одноразовый блокнот (ключ)
        symbols - набор символов
        encrypt - признак зашифрования (True), расшифровния (False)
        Функция возвращает преобразованный текст
        '''
        symbols_dict = {s: i for i, s in enumerate(symbols)}
        symbols_len = len(symbols)
        сipher_text = ""

        if len(open_text) > len(pad):
            raise NotImplementedError("Длина одноразового блокнота (ключа) меньше длины текста")
        result = ""

        for _, s in enumerate(open_text):        
            k = pad[_] if encrypt else -pad[_]       
            сipher_text += symbols[(symbols_dict[s] + k) % symbols_len] 

        return сipher_text

    _pad = [1,1,1,1,1,1,1,1]
    _t ="12345ЭЮЯ"
    _ct = vernam(_t, _pad)
    _ot = vernam(_ct, _pad, encrypt=False)
    _pad, _t, _ct, _ot
    return (vernam,)


@app.cell
def _(catch22, one_time_pad, pfc, vernam):
    _time_stamp = pfc()
    _n = 10000
    _t = catch22 #[:_n]
    _pad = one_time_pad(l=len(_t))
    _cf = vernam(_t, _pad, encrypt = True)
    _of = vernam(_cf, _pad, encrypt = False)
    elapsed_time = pfc() - _time_stamp
    print(f"Успешность зашифрования/расшифрования: {_t==_of}")
    print(f"Длина текста: {len(_t)}")
    print(f"Время счета: {elapsed_time:6.3f} c")
    return


if __name__ == "__main__":
    app.run()
