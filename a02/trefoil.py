import numpy as np
import matplotlib.pyplot as plt


def trefoil(u, v, r):
    x = r * np.sin(3 * u) / (2 + np.cos(v))

    y = r * (np.sin(u) + 2 * np.sin(2 * u)) / \
    (2 + np.cos(v + np.pi * 2 / 3))

    z = r / 2 * (np.cos(u) - 2 * np.cos(2 * u)) * \
    (2 + np.cos(v)) * (2 + np.cos(v + np.pi * 2 / 3)) / 4
    return np.array([x, y, z], dtype=np.float64)
    
    
def trefoil_curve_surface(n=1500, rmin=-1, rmax=3, wmax=5):
    
    r = (rmin*np.pi, rmax*np.pi)
    
    i = np.linspace(r[0], r[1], n)

    # поверхность
    U, V = np.meshgrid(i, i)
    W = trefoil(U, V, wmax)
    S = np.swapaxes(W, 0, 2)
    xs, ys, zs = S[:, :,0], S[:, :,1], S[:, :,2]

    # кривая
    T =  trefoil(i, i, 5) 
    xc, yc, zc = T[0], T[1], T[2]
    
    return  xc, yc, zc, xs, ys, zs 


if __name__ == "__main__":
    n, rmin, rmax, wmax, stride = 1500, -1, 3, 5, 25
    xc, yc, zc, xs, ys, zs = trefoil_curve_surface(n, rmin, rmax, wmax)
    figc = plt.figure(figsize=(5,6))
    axc = plt.axes(projection='3d')
    axc.plot(xc, yc, zc, linewidth=5, color="black")
    #plt.show()
    figs = plt.figure(figsize=(5,6))
    axs = plt.axes(projection='3d')   
    axs.plot_surface(xs, ys, zs, 
                    cmap="rainbow", alpha=1.,)
                   
    axs.plot_wireframe(xs, ys, zs,
                        linewidth = 0.1, color='k',
                        cstride=stride, rstride=stride)     
    plt.show()
    