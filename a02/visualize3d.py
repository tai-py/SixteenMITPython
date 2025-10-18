import numpy as np
import matplotlib.pyplot as plt

def visualize3d_curve(x, y, z, lw=3, color="black", figsize=(6, 5),
                      axis=True, azim=-60, elev=30, roll=0):
    '''
    Рисование трехмерной кривой

    Parameters
    ----------
    x : ndarray[:] float
        данные по оси x
    y : ndarray[:] float
        данные по оси y
    z : ndarray[:] float
        данные по оси z
    lw : float, optional
        толщина линии, by default 5
    color : str, optional
        цвет линии, by default "black"
    figsize : tuple, optional
        размер рисунка, by default (6, 5)
    axis : bool, optional
        флажок отрисовки координатных осей, by default True
    azim : int, optional
        угол поворота вокруг оси z в градусах, by default -60
    elev : int, optional
         угол поворота вокруг оси y в градусах_, by default 30
    roll : int, optional
         угол поворота вокруг оси x в градусах, by default 0

    Returns
    -------
    object
        объект рисунка matplotlib
    '''
    fig = plt.figure(figsize=figsize) if figsize else plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot(x, y, z, linewidth=lw, color=color)
    
    # координатные оси
    if axis:
        plt.axis('on')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z') 
    else:
        plt.axis('off')    
        
    # повороты
    az = ax.azim if azim is None else azim
    el = ax.elev if elev is None else elev
    rl = ax.roll if roll is None else roll
    ax.view_init(azim=az, elev=el, roll=rl)
    return fig

def visualize3d_surface(x, y, z, figsize=(6,5), cmap="rainbow", 
                        alpha=1., stride=20, lw=0.2,
                        axis=True, azim=-60, elev=30, roll=0):
    '''
    Рисование поверхности и "проволочной" сетки

    Parameters
    ----------
    x : ndarray[:,:] float
        данные по x
    y : ndarray[:,:] float
        данные по y
    z : ndarray[:,:] float
        данные по z
    figsize : tuple | None, optional
        размеры рисунка, by default (6,5),        
    cmap : str | None, optional
       имя палитры matplotlib, by default "rainbow",
       если не задана, то поврехность не отображается 
    alpha : float, optional
        непрозрачность, by default 1.
    stride : int, optional
        расстояние между узлами "проволочной" сетки, by default 20,
        если не задана, то "проволочная" сетка не отображается" 
    lw : float, optional
       толщина линии сетки, by default 0.2
    axis : bool, optional
        отображение осей координат, by default True
    azim : int, optional
        поворот вокруг оси z в градусах, by default -60
    elev : int, optional
        поворот вокруг оси y в градусах, by default 30
    roll : int, optional
        поворот вокруг оси x в градусах, by default 0

    Returns
    -------
    object
        объект рисунка matplotlib
    '''
    fig = plt.figure(figsize=figsize) if figsize else plt.figure()
    ax = plt.axes(projection='3d')

    if cmap:
        ax.plot_surface(x, y, z, 
                        cmap=cmap, alpha=alpha)  

    if stride:
        # проволочная сетка     
        ax.plot_wireframe(x, y, z, linewidth = lw, color='k',
                cstride=stride, rstride=stride)
    
    # координатные оси
    if axis:
        plt.axis('on')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z') 
    else:
        plt.axis('off')    
        
    # повороты
    az = ax.azim if azim is None else azim
    el = ax.elev if elev is None else elev
    rl = ax.roll if roll is None else roll    
    ax.view_init(azim=azim, elev=elev, roll=rl)  

    return fig

if __name__ == "__main__":
    from trefoil import trefoil_curve_surface as data
    xc, yc, zc, xs, ys, zs = data()
    figc = visualize3d_curve(xc, yc, zc, axis=True, azim=-30, elev=60, roll=30)
    figs = visualize3d_surface(xs, ys, zs, cmap="rainbow",  axis=True, azim=-30, elev=60, roll=30, stride=25)
    
    plt.show()
    