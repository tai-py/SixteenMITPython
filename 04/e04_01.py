import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import base64

    mo.md("#Стеганография")
    return base64, mo, np, plt


@app.cell
def _(mo):
    mo.md(r"""
    ## Кодирование символов
    """)
    return


@app.cell
def _(base64):
    # исходная строка
    s = '01Ю\u5abf🐻'

    def str_2_bytes(s, encoding='utf-8'):
        '''
        Преобразование строки s в
        последовательность байтов
        ''' 
        print(f'Исходная строка: {s}, длина:{len(s)} кодировка: {encoding}')
        codes = [ord(c) for c in s]
        print(f"Коды символов исходной строки: {codes}. Длина:{len(codes)}")    
        b = bytes(s, encoding=encoding)
        print(f"Последовательность байтов: {b}. Длина:{len(b)}")
        b10 = [int(by) for by in b]
        print(f"Десятичное представление байтов: {b10}. Длина:{len(b10)}")
        b64 = base64.b64encode(b)
        print(f"Кодирование последовательности байтов в base64: {b64}. Длина:{len(b64)}\n")

    str_2_bytes(s, encoding='utf-32')
    str_2_bytes(s, encoding='utf-16')
    str_2_bytes(s, encoding='utf-8')
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Раскладываем биты числа 241 на биты
    """)
    return


@app.cell
def _(np):
    mask = 1, 2, 4, 8, 16, 32, 64, 128
    number = 241
    bits = np.zeros(8, dtype=np.uint8)
    for _, b  in enumerate(mask):
        if number & b:
            bits[_] = 1
    bits
    return bits, mask


@app.cell
def _(bits, mask, np):
    np.sum(bits * mask)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Устанавливаем или сбрасываем младший бит в байте
    """)
    return


@app.cell
def _():
    def set_bit(byte, bit):
        if bit:
            return byte | bit
        else: 
            return byte & 254

    (set_bit(240, False),  set_bit(240, True), 
     set_bit(241, False),  set_bit(241, True))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Читаем цитату к главе 4 из файловой системы
    """)
    return


@app.cell
def _():
    def read_utf8(fn):
        with open(fn, 'r', encoding='utf-8') as f:
            return f.read()

    cite = read_utf8('cite.txt')
    print(cite)
    cite_len = len(cite)
    print(f"Символов в цитате:{cite_len}")
    return (cite,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Читаем изображение заставки
    """)
    return


@app.cell
def _(np, plt):
    def read_image(fn):
        img =  plt.imread(fn) # массив изображения
        ndim, dtype, shape = img.ndim, img.dtype, img.shape
        max_brightness = np.max(img)
        # преобразуем в массив целых чисел
        imgn = np.asarray(img, dtype=np.uint8)
        if ndim==2:
            imgn[:, :] = img[:, :]*255 if  max_brightness<=1 \
                         else  img[:, :] 
        else:
            imgn[:, :, :] = img[:, :, :]*255 if  max_brightness<=1 \
                         else  img[:, :, :]         
        return imgn

    img = read_image("04_00.png") 
    print(f"Размер массива изображения: {img.shape}")
    print(f"Тип элементов массива: {img.dtype}")
    print(f"Количество байтов в массиве: {img.nbytes}")
    return (img,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Вставляем сообщение в изображение
    """)
    return


@app.cell
def _(cite, img, plt):
    def embed_message_into_array(message, a, 
                                 figsize=None, fn='', info=True):
        '''
        Встраивание сообщения в массив
        Параметры:
        message - строка с сообщением обязательно 
                  в кодировке utf-8
        a - двухмерный или трехмерный массив
        figsize - размер рисунка, если задан,
                  то отображается рисунок со встроенным сообщением 
        fn - путь для сохранения рисунка
        info - признак распечатки информации
        Функция возвращает:
        a - массив со вспренным сообщением
        fig - объект изображения, если задан figsize,
              None в противном случае
        '''
        # преобразуем сообщение в последовательность байтов
        messageb = bytes(message, encoding='utf-8')
        l = len(messageb) + 6 # длина сообщения с префиксом
        slen = str(l) # строковое представление длины
        # дополнение строкового представления длины нулями слева
        # длина префикса всегда 6 символов
        prefix = '0'*(6 - len(slen)) + slen 
        # преобразуем сообщение с префиксом длины
        pmessage = prefix + message # сообщение с префиксом
        pmessageb = bytes(pmessage, encoding='utf-8')
        l, lb = len(pmessage), len(pmessageb)
        shape = a.shape
        nbytes = a.nbytes
        nbits = lb * 8
        if info:
            print(f"Сообщение с префиксом: {pmessage}")
            print(f"Байтовое представление pmessage: {pmessageb}")
            print(f"Длина сообщения: {l}")
            print(f"Длина байтового представления сообщения: {lb}")
            print(f"Размер массива: {shape}")
            print(f"Число байтов в массиве: {nbytes}")
            print(f"Число битов в байтовом представлении сообщения: {nbits}")

        if nbytes >=nbits:
            # делаем массив одномерным
            a.shape = nbytes,

            # для выборки битов из байта сообщения нам понадобится маска
            mask = 1, 2, 4, 8, 16, 32, 64, 128
            # Изменяем младший бит в байтах массива
            for i in range(lb): # цикл по байтам сообщения
                for j in range(8): # цикл по битам байта сообщения
                    # выбираем очередной бит из байта сообщения
                    b = pmessageb[i] & mask[j]
                    # модифицируем младший бит байта массива
                    # пишем в него 1, если b>0, и 0, иначе
                    if b:
                        a[i*8 + j] |= 1 
                    else:
                        a[i*8 + j] &= 254 

            # возвращаемся к первоначальному размеру массива
            a.shape = shape
            # визуализация
            fig = None
            if figsize:
                fig = plt.figure(figsize=figsize)
                plt.imshow(a)
                plt.axis('off')
                if fn:
                    plt.savefig(fn, dpi=300, facecolor="white")
            # возвращаем модифицированный массив и изображение
            return a, fig
        else:
            raise ValueError("Слишком длинное сообщение!")




    am, _fig =embed_message_into_array(cite, img.copy(), 
                                       figsize=(6,6), fn='04_01.png')        
    _fig    
    return am, embed_message_into_array


@app.cell
def _(np):
    print("Число затронутых строк изображения: ", int(np.ceil(15312/(768*3))))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Формируем разностное изображение
    """)
    return


@app.cell
def _(am, img, np, plt):
    diff = img ^ am
    _n = 7
    print(f"Максимальное различие элементов: {np.max(diff)}")
    _fig = plt.figure(figsize=(15,1))
    plt.subplot(121)
    #plt.imshow(diff[:_n])
    plt.imshow(255 - diff[:_n])
    plt.axis('off')
    plt.subplot(122)
    plt.imshow(255 - diff[:_n]*255)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('04_02.png', dpi=300, facecolor='white')
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Извлекаем сообщение из массива
    """)
    return


@app.cell
def _(cite, embed_message_into_array, img, np):
    def extract(a, n):
        '''
        Извлечение из массива сообщение заданной длины
        a - одномерный массив
        n - число байтов сообщения
        Функция возвращает строку сообщения
        '''
        # заготовка массива сообщения
        bt = np.zeros(n, dtype=np.uint8)
        mask = 1, 2, 4, 8, 16, 32, 64, 128
        # сборка байтов из младших битов массива
        for i in range(n*8):
            b = a[i] & 1 # бит сообщения
            if b:
                bt[i//8] |= mask[i % 8]

        s = str(bt, encoding='utf-8')  # преобразование в строку   
        return s

    def extract_message(a):
        '''
        Извлечение сообщения из массива a.
        Длина сообщения закодирована в префиксе
        Функция возвращает декодированное сообщение
        '''
        shape = a.shape
        nbytes = a.nbytes
        # преобразуем в одномерный массив
        a.shape = nbytes, 

        # текстовое представление длины сообщения
        s_len = extract(a, 6)   
        l = int(s_len) # длина сообщения в префиксом
        s = extract(a, l) # извлекаем сообщение с префиксом
        # возвращаемся к первоначальному размеру массива
        a.shape = shape 
        return s[6:] # удаляем префикс

    _ar, _fig = embed_message_into_array(cite, img)
    message = extract_message(_ar)
    cite == message
    return


if __name__ == "__main__":
    app.run()
