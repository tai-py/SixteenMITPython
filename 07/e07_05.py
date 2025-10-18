import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium")

with app.setup:
    # Initialization code that runs before all other cells
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.path import Path
    from matplotlib.patches import PathPatch, Rectangle
    from svgpath2mpl import parse_path
    from matplotlib.transforms import Affine2D as T


@app.cell
def _():
    mo.md(
        r"""
    # Пишем вспомогательные функции для отображения и преобразования фигур
    ## Функция рисования фигур
    """
    )
    return


@app.function
def draw(*paths, box=True, fill=False, 
         axis=True, equal=True, nrows=1, ncols=1,
         figsize =(3,3), lims=None): 
    ''' 
    Рисование последовательности фигур, заданных с помощью matplotlib Path
    Параметры:
    paths - подследовательность фигур,
    box - флажок, управляющий отображением единичного прямоугольника,
    fill - флажок заполнения отображаемой фигуры цветом,
    axis - флажок отображения осей и оцифровки по осям,
    equal - флажок, задающий одинаковые масштабы по горизонтальной и 
           вертикальной осям,
    nrows - число рисунков по вертикальной оси,
    ncols - число рисунков по горизонтальной оси,
    figsize - размер холста, на котором отображаются рисунки,
    lims - признак принудительного задания границ рисунка  по осям координат
          в виде (xmin, ymin, xmax, ymax)
   

    Функция возвращает объект холста matplotlib (Figure)
    '''
    l = len(paths) # число рисунков

    fig, axs = plt.subplots(figsize=figsize,ncols=ncols, nrows=nrows)

    # subplots возвращет различные объекты при задании nrows, ncols,
    # поэтому приходится по-разному извлекать объект рисунка
    for k in range(l): # цикл по рисункам
        i = k // ncols
        j = k %  ncols
        k = i*ncols + j # номер рисунка  

        if nrows==1 and ncols==1:
            ax = axs
            path = paths[0]
        elif ncols==1:
            path = paths[i]
            ax = axs[i]
        elif nrows==1:            
            path = paths[j]
            ax = axs[j]
        else: # общий случай
            path = paths[k]
            ax = axs[i, j]

        # отображаем фигуру
        if path: 
            ax.add_patch(PathPatch(path, fill = fill))
            if box: # отображаем единичный квадрат  
                r = Rectangle((0,0), 1, 1, fill = False, 
                              linestyle = 'dotted')
                ax.add_patch(r)

            if equal: # равенство масштабов по осям координат
                ax.axis('equal')

            if not axis: # отображение осей и оцифровки
                ax.axis('off')
                plt.axis('off')

            if lims: # границы рисунка
                xmin, ymin, xmax, ymax = lims
                ax.set_xlim(xmin, xmax)
                ax.set_ylim(ymin, ymax)
        else:
            # подавляем оси и оцифровку для отсутствующего рисунка
            ax.axis('off')
    plt.tight_layout()

    return fig


@app.cell
def _():
    mo.md(r"""## Задаем фигуру для символа Г виде функции""")
    return


@app.function
def get_G():
    # буква Г
    g = '''
        M 0.0, 0.0
        L 0.0, 1.0
        L 0.7, 1.0
        L 0.7, 0.9
        L 0.1, 0.9
        L 0.1, 0.0
        L 0.0, 0.0    
    '''
    return parse_path(g)


@app.cell
def _():
    mo.md(r"""## Тестируем функцию draw""")
    return


@app.cell
def _():
    _G = get_G()
    draw(_G, _G,_G,_G,_G,  figsize=(8,3),axis=False, box=False, 
         equal=True, lims=None, ncols=3, nrows=2 )
    return


@app.cell
def _():
    draw(get_G())
    return


@app.cell
def _():
    mo.md(
        r"""
    ## Создаем простые фигуры, которые можно импортировать в другие блокноты
    ### Пустая фигура
    """
    )
    return


@app.function
def get_blank():
    # пустая фигура
    b = 'M 0., 0.'
    return parse_path(b)


@app.cell
def _():
    # тестируем пустую фигуру
    draw(get_blank())
    return


@app.cell
def _():
    mo.md(r"""### Простая фигура, из которой мы далее соберем контур рвбы""")
    return


@app.function
def get_edge():
    '''
    Простая фигура для сборки контура рыбы
    '''
    edge= '''
        M 1.,1.
        C 0.78,0.95 0.78,0.95 0.58,0.97
        C 0.38,0.80 0.38,0.80 0.25,0.73
        L 0.,1.    
    '''
    return parse_path(edge)


@app.cell
def _():
    draw(get_edge(), fill=True, equal=True)
    return


@app.cell
def _():
    mo.md(r"""### Перевернутый символ F""")
    return


@app.function
def get_F():
    '''
    Перевернутый символ F
    '''
    F = '''
        M .1, .1
        L .9, .1
        L .9, .2
        L .2, .2
        L .2, .4
        L .6, .4
        L .6, .5
        L .2, .5
        L .2, .9
        L .1, .9
        L .1, .1    
    '''
    return parse_path(F)


@app.cell
def _():
    draw(get_F(), fill=True, equal=True)
    return


@app.cell
def _():
    mo.md(r"""### Рыба""")
    return


@app.function
def get_fish():
    fish = '''
        M 0.00 0.00
        C 0.08 0.02 0.22 0.18 0.29 0.28
        M 0.30 0.50
        C 0.34 0.60 0.43 0.68 0.50 0.74
        M 0.50 0.74
        C 0.58 0.79 0.66 0.78 0.76 0.80
        M 0.76 0.80
        C 0.82 0.88 0.94 0.95 1.00 1.00
        M 1.00 1.00
        C 0.90 0.97 0.81 0.96 0.76 0.95
        M 0.76 0.95
        C 0.69 0.96 0.62 0.96 0.55 0.96
        M 0.55 0.96
        C 0.49 0.90 0.40 0.83 0.35 0.80
        M 0.35 0.80
        C 0.29 0.76 0.19 0.72 0.14 0.69
        M 0.14 0.69
        C 0.09 0.65 -0.03 0.57 -0.05 0.28
        M -0.05 0.28
        C -0.04 0.18 -0.02 0.05 0.00 0.00
        M 0.10 0.15
        C 0.14 0.18 0.18 0.22 0.18 0.25
        M 0.18 0.25
        C 0.16 0.26 0.14 0.27 0.12 0.27
        M 0.12 0.27
        C 0.11 0.23 0.11 0.19 0.10 0.15
        M 0.05 0.18
        C 0.10 0.20 0.08 0.26 0.09 0.30
        M 0.09 0.30
        C 0.07 0.32 0.06 0.34 0.04 0.33
        M 0.04 0.33
        C 0.04 0.27 0.04 0.19 0.05 0.18
        M 0.11 0.30
        C 0.16 0.44 0.24 0.61 0.30 0.66
        M 0.30 0.66
        C 0.41 0.78 0.62 0.84 0.80 0.92
        M 0.23 0.20
        C 0.35 0.20 0.44 0.22 0.50 0.25
        M 0.50 0.25
        C 0.50 0.33 0.50 0.41 0.50 0.49
        M 0.50 0.49
        C 0.46 0.53 0.42 0.57 0.38 0.61
        M 0.29 0.29
        C 0.36 0.26 0.43 0.27 0.48 0.31
        M 0.34 0.39
        C 0.38 0.34 0.44 0.36 0.48 0.37
        M 0.34 0.49
        C 0.38 0.44 0.41 0.42 0.48 0.43
        M 0.45 0.58
        C 0.46 0.60 0.47 0.61 0.48 0.61
        M 0.42 0.61 
        C 0.43 0.64 0.46 0.68 0.48 0.67
        M 0.25 0.74
        C 0.17 0.83 0.08 0.91 0.00 0.99
        M 0.00 0.99
        C -0.08 0.91 -0.17 0.82 -0.25 0.74
        M -0.25 0.74
        C -0.20 0.63 -0.11 0.53 -0.03 0.43
        M -0.17 0.74
        C -0.13 0.66 -0.08 0.60 -0.01 0.56
        M -0.12 0.79
        C -0.07 0.71 -0.02 0.66 0.05 0.60
        M -0.06 0.86
        C -0.03 0.77 0.03 0.72 0.10 0.66
        M -0.02 0.92
        C 0.02 0.84 0.09 0.77 0.16 0.70    
    '''
    return parse_path(fish)


@app.cell
def _():
    draw(get_fish(), fill=True, equal=True)
    return


@app.cell
def _():
    mo.md(r"""### Треугольник""")
    return


@app.function
def get_triangle():
    t = '''
        M 0.,1.
        L 1.,1.
        L 0.,0.
        L 0.,1.    
    '''
    t = parse_path(t)
    return t


@app.cell
def _():
    draw(get_triangle())
    return


@app.cell
def _():
    mo.md(
        r"""
    ## Выводим подготовленные фигуры
    get_blank() – пустая фигура, get_edge() – фрагмент для рисования контура рыбы (контур мы соберем позже), get_F – перевернутый символ F get_fish – рыбка и, наконец, треугольник – функция get_tiriangle
    """
    )
    return


@app.cell
def _():
    draw(get_G(), get_blank(), get_edge(), get_F(),
         get_fish(), get_triangle(),
         axis=False, box=True, fill=True, 
         ncols=3, nrows=2, figsize=(5, 3))
    return


@app.cell
def _():
    mo.md(
        r"""
    ## Аффинные преобразования средствами matplotlib
    Нам нужно из одной фигуры скомпоновать контур рыбы. Сделать это можно, 
    только написав вспомогательные  функции для преобразования фигур и
    их компоновки.
    """
    )
    return


@app.function
def transform(f, transformation):
    ''' 
    Применение к фигуре преобразования
    f - преобразуемая фигура
    transformation - преобразование
    Функция возвращает преобразованную фигуру
    '''
    return f.transformed(transformation)


@app.function
def union(*fs):
    '''
    Объединение последовательности фигур
    fs - последовательность объединяемых фигур
    Функция возвращает фигуру, созданную с помощью 
    объединения фигур
    '''
    if not fs:
        return get_blank() # возращаем пустую фигуру
    else:
        result = fs[0]
        for f in fs[1:]:
            result = Path.make_compound_path(result, f)
        return result


@app.cell
def _():
    # тестируем union
    union(), union(get_G()), union(get_G(), get_F())
    return


@app.cell
def _():
    mo.md(
        r"""
    ### Реализуемые преобразования
    Напишем функции, позволяющие осуществлять основные афинные преобразования,
    которые понадобятся нам в дальнейшем:

    - translate - перемещение фигуры на dx, dy
    - scale - масштабирование по осям координат в kx, ky раз
    - flip_x - отражение относительно вертикальной оси
    - flip_y - отражение относительно горизонтальной оси -rot_90 - поворот на 90 градусов по часовой стрелке
    - rot_45 - поворот на 45 градусов по часовой стрелке
    - rotate_deg_around - вращение фигуры вокруг точки x, y на deg градусов по часовой стрелке
    - over - псеводоним объединения фигур
    - beside - размещение двых фигур рядом с друг другом с масштаброванием по x в n1 и n2 раз
    - above - размещение двух фигур друг над другом с масштабированием по оси x
    """
    )
    return


@app.function
def translate(f, dx, dy):
    ''' 
    Перемещение фигуры на dx, dy
    '''
    return transform(f, T().translate(dx,dy))


@app.cell
def _():
    # тестирование transform и union
    draw(union(get_G(), translate(get_G(), 2,1)))
    return


@app.function
def scale(f, kx, ky):
    ''' 
    Масштабирование фигуры по осям
    kx - коэффициент преобразования по горизонтальной оси
    ky - коэффициент преобразования по вертикальной оси
    Функция возвращает преобразованную фигуру
    '''
    return transform(f, T().scale(kx,ky))


@app.cell
def _():
    # тестирование scale
    draw(union(get_G(), translate(scale(get_G(), 2,3),2, 1)))
    return


@app.function
def flip_y(f):
    ''' 
    Отражение от вертикальной оси
    с переносом вправо на 1 влево
    '''
    return transform(f, T().scale(-1, 1).translate(1, 0))


@app.cell
def _():
    # тестирование flip_y
    draw(union(get_G(), flip_y(get_G())))
    return


@app.function
def flip_x(f):
    ''' 
    Отражение от горизонтальной оси
    с переносом вверх на единицу 
    '''
    return transform(f, T().scale(1, -1).translate(0, 1))


@app.cell
def _():
    # тестирование flip_x
    draw(union(get_G(), flip_x(get_G())))
    return


@app.function
def rot_90(f):
    ''' 
    поворот на 90 градусов против часовой стрелки 
    с переносом на единицу вправо
    '''
    return transform(f, T().rotate_deg(90).translate(1, 0))


@app.cell
def _():
    # тестирование rot_90
    draw(union(get_G(), rot_90(get_G())))
    return


@app.function
def rot_45(f):
    '''
    поворот на 45 градусов против часовой стрелке 
    с масштабированием и переносом
    '''
    return transform(f, T().rotate_deg(45).
                     scale(1/np.sqrt(2), 
                           1/np.sqrt(2)).translate(1/2, 1/2))


@app.cell
def _():
    # тестирование rot_45
    draw(union(get_G(), rot_45(get_G())))
    return


@app.function
def rotate_deg_around(f, x=0, y=0, deg=90):
    ''' 
    вращение фигуры вокруг точки x, y  на deg градусов против часовой стрелке'''
    return  transform(f, T().rotate_deg_around(x, y, deg))


@app.cell
def _():
    # тестирование rotate_deg_around
    draw(union(get_G(), 
               rotate_deg_around(get_G(),deg=-30),
               rotate_deg_around(get_G(),deg=-60),
               rotate_deg_around(get_G(),deg=-150)
              ))
    return


@app.function
def over(*paths):
    '''
    Псевдоним объединения фигур 
    '''
    return union(*paths)


@app.cell
def _():
    # тестирование over
    draw(
        over(
            get_G(),
            rotate_deg_around(get_G(), deg=30),
            rotate_deg_around(get_G(), deg=60),
            rotate_deg_around(get_G(), deg=150),
        )
    )
    return


@app.function
def beside(f1, f2, n1=1, n2=1):
    '''
    Размещение двух фигур рядом с друг другом     
    с масштабированием по x в n1 и по y в n2 раз
    для размещения в единичном квадрате
    f1, f2 - фигуры
    n1, n2 - коэффициенты масштабирования по оси x и y
    '''
    s = n1 + n2
    return union(transform(f1, T().scale(n1/s, 1)),
                 transform(f2, T().scale(n2/s, 1).
                           translate(n1/s, 0)))


@app.cell
def _():
    # тестирование beside
    draw(beside(get_G(), get_G()))
    return


@app.function
def above(f1, f2, n1=1, n2=1):
    ''' 
    Размещение двух фигур друг над другом 
    с масштабированием по оси y
    для размещения в единичном квадрате
    '''
    s = n1 + n2
    return union(transform(f1, T().scale(1, n1/s).translate(0, n2/s)),
                 transform(f2, T().scale(1, n2/s)))


@app.cell
def _():
    # тестирование above
    draw(above(get_G(), get_G()))
    return


@app.function
def four(a, b, c, d):
    '''
    Размещение четырех фигур
    a, b, c, d
    по углам единичного квадрата
    '''
    return above(beside(a, b), beside(c, d))


@app.cell
def _():
    # Тестирование four
    _G = get_G()
    draw(four(_G, flip_y(_G), flip_x(_G), flip_x(flip_y(_G))))
    return


@app.function
def nine(p1, p2, p3, p4, p5, p6, p7, p8, p9):
    '''
    Укладываем девять фигур p1-p9
    на сетке 3 на 3
    '''
    return above(
            beside(p1, beside(p2, p3), 1, 2),
            above(beside(p4, beside(p5, p6), 1, 2),
                  beside(p7, beside(p8, p9), 1, 2), 
            ),
            1, 2)


@app.cell
def _():
    # тестируем nine
    _Gs = [get_G()]*9
    _Gs[4] = get_blank()
    draw(nine(*_Gs))
    return


@app.cell
def _():
    mo.md(r"""## Делам иллюстрацию  применения рассмотренных выше функций""")
    return


@app.cell
def _():
    # первый ряд рисунка
    # объединение, перенос
    _f1 = union(get_G(), translate(get_G(), 2,1)) 
    # объединение, масштабирование
    _f2 = union(get_G(), translate(scale(get_G(), 2,3),2, 1))
    # flip_y
    _f3 = union(get_G(), flip_y(get_G()))
    # flip_x
    _f4 = union(get_G(), flip_x(get_G()))
    # второй ряд рисунка
    # rot_90
    _f5 = union(get_G(), rot_90(get_G()))
    # rot_45
    _f6 = union(get_G(), rot_45(get_G()))
    # rotate_deg_around
    _f7 = union(get_G(), 
               rotate_deg_around(get_G(),deg=-30),
               rotate_deg_around(get_G(),deg=-60),
               rotate_deg_around(get_G(),deg=-150)
              )
    # beside
    _f8 = beside(get_G(), get_G())
    # третий ряд рисунка
    # above
    _f9 = above(get_G(), get_G())
    # four
    _G = get_G()
    _f10 = four(_G, flip_y(_G), flip_x(_G), flip_x(flip_y(_G)))
    # nine
    _Gs = [get_G()]*9
    _Gs[4] = get_blank()
    _f11 = nine(*_Gs)

    draw(_f1,  _f2,  _f3, _f4,
         _f5,  _f6,  _f7, _f8,
         _f9, _f10, _f11,
         axis=False, box=True, fill=False, 
         ncols=4, nrows=3, figsize=(12, 9))
    return


@app.cell
def _():
    mo.md(
        r"""
    ## Сборка контура рыбки
    Исходная фигура:
    """
    )
    return


@app.cell
def _():
    p0 = get_edge() 
    draw(p0)
    return (p0,)


@app.cell
def _():
    mo.md(r"""первый элемент контура""")
    return


@app.cell
def _(p0):
    p1 = flip_x(p0)
    draw(p1)
    return (p1,)


@app.cell
def _():
    mo.md(r"""второй элемент контура""")
    return


@app.cell
def _(p1):
    p2 = translate(rot_90(p1), -1, 0)
    draw(p2)
    return (p2,)


@app.cell
def _():
    mo.md(r"""Собираем первые два элемента""")
    return


@app.cell
def _(p1, p2):
    p12 = union(p1, p2)
    draw(p12)
    return (p12,)


@app.cell
def _():
    mo.md(r"""третий элемент""")
    return


@app.cell
def _(p1):
    p3 = flip_y(rot_45(p1))
    draw(p3)
    return (p3,)


@app.cell
def _():
    mo.md(r"""Собираем три элемента вместе""")
    return


@app.cell
def _(p1, p2, p3):
    p123 = union(p1, p2, p3)
    draw(p123)
    return (p123,)


@app.cell
def _():
    mo.md(r"""четвертый элемент""")
    return


@app.cell
def _(p3):
    p4 = flip_x(flip_y(p3))
    draw(p4)
    return (p4,)


@app.cell
def _():
    mo.md(r"""Собираем все вместе""")
    return


@app.cell
def _(p1, p2, p3, p4):
    draw(union(p1, p2, p3, p4))
    return


@app.cell
def _():
    mo.md(
        r"""
    Как и ранее оформим контур рыбки в виде функции
    для последующего использования
    """
    )
    return


@app.function
def get_fish_outline():
    '''
    Компоновка контура рыбки
    из фигуры edge
    '''
    p0 = get_edge()
    p1 = flip_x(p0)
    p2 = translate(rot_90(p1), -1, 0)
    p3 = flip_y(rot_45(p1))
    p4 = flip_x(flip_y(p3))    
    return flip_x(union(p1, p2, p3, p4))


@app.cell
def _():
    # тестируем контур
    draw(get_fish_outline())
    return


@app.cell
def _():
    mo.md(r"""Теперь скомпонуем картинку процесса сборки контура рыбки""")
    return


@app.cell
def _(p0, p1, p12, p123, p2, p3, p4):
    _fig = draw(p0,   p1,   p2, p3,    p4,
         None, None, p12, p123, get_fish_outline(), 
         equal=True, axis=True,
           nrows=2, ncols=5, figsize=(15, 5)    
    )


    return


if __name__ == "__main__":
    app.run()
