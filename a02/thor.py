import numpy as np
import matplotlib.pyplot as plt

def thor(u, v, r=.5, R=5):
    x = R*(2+np.sin(2*np.pi*v))*np.cos(2*np.pi*u)
    y = R*(2+np.sin(2*np.pi*v))*np.sin(2*np.pi*u)
    z = r*np.cos(2*np.pi*v)
    return x, y, z


def thor_curve_surface(n=1500):
    umin, umax = 0, 1
    u = np.linspace(umin, umax, n)
    v = np.linspace(umin, umax, n)
    U, V = np.meshgrid(u, v)
    
    uc = u 
    vc = 20*v #np.sign(np.sin(20*np.pi*uc))
    
    xc, yc, zc = thor(uc, vc)    
    xs, ys, zs = thor(U, V)
    return xc, yc, zc, xs, ys, zs

if __name__ == "__main__":
    n, stride = 1500, 25
    xc, yc, zc, xs, ys, zs = thor_curve_surface(n)
    
    figc = plt.figure(figsize=(5,6))
    axc = plt.axes(projection='3d')
    axc.plot(xc, yc, zc, linewidth=3, color="black")
    # axc.set_xlim(-5,5)
    # axc.set_ylim(-5,5)
    # axc.set_zlim(-2,2)
    #plt.show()
    figs = plt.figure(figsize=(5,6))
    axs = plt.axes(projection='3d')   
    axs.plot_surface(xs, ys, zs, 
                    cmap="rainbow", alpha=1.,)
                   
    axs.plot_wireframe(xs, ys, zs,
                        linewidth = 0.2, color='k',
                        cstride=stride, rstride=stride) 
    # axs.set_xlim(-15,15)
    # axs.set_ylim(-15,15)
    # axs.set_zlim(-2,2)
    #plt.show()
         
    plt.show()        
