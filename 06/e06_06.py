import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from collections import Counter, OrderedDict
    import numpy as np

    import matplotlib.pyplot as plt
    import seaborn as sns

    mo.md('# Частота символов в романе Л.Н. Толстого "Война и мир" и словаре русских существительных')
    return plt, sns


@app.cell
def _():
    def read_text(fn):
        with open(fn,encoding="utf8") as f:
            return f.read().lower()

    text1 = read_text(r"texts\Tolstoy_Lev_Voyna_i_mir_1-2.txt") +\
            read_text(r"texts\Tolstoy_Lev_Voyna_i_mir_3-4.txt")

    text = text1
    text2 = read_text(r"texts\russian_nouns.txt")
    l1, l2 = len(text1), len(text2)

    l1, l2
    return text1, text2


@app.cell
def _(plt, sns, text1, text2):
    def ru_symbols(text, blank_e=True):
        # формируем русский алфавит
        a = ord('а')
        alphabet = [chr(i) for i in range(a,a+32)]
       #print(f"{alphabet=}, {type(alphabet)=}")
        if blank_e:
            alphabet.insert(0, ' ')
            alphabet.insert(7, 'ё')
        symbols = [s for s in text if s in alphabet]    

        return symbols, alphabet

    symbs_tolstoi, _ = ru_symbols(text1)
    symbs_nouns_dict, _ = ru_symbols(text2)
    alpha = 0.8

    _fig,_ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))

    sns.histplot(symbs_tolstoi, stat="density",
                 ax=_ax, alpha=alpha, label="Война и мир ")
    sns.histplot(symbs_nouns_dict, stat="density", 
                 ax=_ax, alpha=alpha, label="Словарь существительных русского языка")
    _ax.set_xlabel('Символы русского алфавита')
    _ax.set_ylabel('Частота')
    plt.grid()
    plt.legend()
    plt.savefig('06_20.png', dpi=300, facecolor='white')
    _fig
    return symbs_nouns_dict, symbs_tolstoi


@app.cell
def _(plt, sns, symbs_nouns_dict, symbs_tolstoi):
    _fig, _ax = plt.subplots(nrows=1, ncols=2, figsize=(6, 6))
    sns.violinplot(symbs_tolstoi, ax=_ax[0])
    _ax[0].set_xlabel("Война и мир")
    sns.violinplot(symbs_nouns_dict, ax=_ax[1])
    _ax[1].set_xlabel('Словарь существительных')
    plt.savefig('06_21.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _(plt, sns, symbs_nouns_dict, symbs_tolstoi):
    _fig,_ax = plt.subplots(nrows=1, ncols=2, figsize=(6, 6))
    sns.boxplot(symbs_tolstoi, ax=_ax[0])
    _ax[0].set_xlabel("Война и мир")
    sns.boxplot(symbs_nouns_dict, ax=_ax[1])
    _ax[1].set_xlabel('Словарь существительных')
    plt.savefig('06_22.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
