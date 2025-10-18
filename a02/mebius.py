import numpy as np
import matplotlib.pyplot as plt

def mebius(u, v):
    # контроль ограничений
    # u = np.min(np.max(u, 0), 2*np.pi)
    # v = np.min(np.max(v, -1), 1) 
    x = (1 + v/2*np.cos(u/2))*np.cos(u)
    y = (1 + v/2*np.cos(u/2))*np.sin(u)
    z = v/2*np.sin(u/2)
    return x, y, z


def mebius_curve_surface(n=1500):
    umin, umax = 0, 2*np.pi
    vmin, vmax = -1, 1
    u = np.linspace(umin, umax, n)
    v = np.linspace(vmin, vmax, n)
    U, V = np.meshgrid(u, v)
    
    uc = u
    vc = np.sign(np.sin(10*uc))
    
    xc, yc, zc = mebius(uc, vc)    
    xs, ys, zs = mebius(U, V)
    
    return xc, yc, zc, xs, ys, zs
    
    
    
if __name__ == "__main__":
    n, stride = 1500, 25
    xc, yc, zc, xs, ys, zs = mebius_curve_surface(n)
    figc = plt.figure(figsize=(5,6))
    axc = plt.axes(projection='3d')
    axc.plot(xc, yc, zc, linewidth=3, color="black")
    axc.set_xlim(-2,2)
    axc.set_ylim(-2,2)
    axc.set_zlim(-2,2)
    #plt.show()
    figs = plt.figure(figsize=(5,6))
    axs = plt.axes(projection='3d')   
    axs.plot_surface(xs, ys, zs, 
                    cmap="rainbow", alpha=1.,)
                   
    axs.plot_wireframe(xs, ys, zs,
                        linewidth = 0.2, color='k',
                        cstride=stride, rstride=stride) 
    axs.set_xlim(-2,2)
    axs.set_ylim(-2,2)
    axs.set_zlim(-2,2)
    #plt.show()
         
    plt.show()    
    
    