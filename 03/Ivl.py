import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")

with app.setup:
    # Initialization code that runs before all other cells
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    import mpmath  # арифметика с произвольной точностью
    from mpmath import mpf, iv  # интервалы


    class Ivl:
        """
        Задаем массив интервалов с
        точными значениями data
        и погрешностью eps
        """

        @staticmethod
        def env(dps=15, pretty=False):
            """
            Задаем число значащих цифр и
            способ вывода значений
            """
            iv.dps = dps
            iv.pretty = pretty

        @staticmethod
        def zeros(n, eps=0.0):
            """
            Инициализация нулевого массива интервалов
            размерности n вида [-eps, eps]
            """
            data = np.zeros(n, dtype=Ivl)
            ivl = Ivl(data, eps)
            return ivl

        @staticmethod
        def ones(n, eps=0.0):
            """
            Инициализация единичного массива интервалов
            размерности n вида [-eps, eps]
            """
            data = np.ones(n, dtype=Ivl)
            ivl = Ivl(data, eps)
            return ivl

        def __init__(self, data, eps=0.0):
            """
            Инициализация массива интевалов
            Параметры:
            data - данные
            eps - абсолютная погрешность
            """
            if isinstance(data, (int, float, str)):
                self.shape = (1,)
                self.data = np.array([data], iv.mpf)
                self.data[0] = iv.mpf(
                    [
                        float(data) - float(eps),
                        float(data) + float(eps),
                    ]
                )
            elif isinstance(data, Ivl):
                self.shape = data.shape
                self.data = data.data
            elif isinstance(data, iv.mpf):
                self.data = np.zeros(1, dtype=object)
                self.shape = 1,
                self.data[0] = data
            elif isinstance(data, (list, tuple)):
                data = np.array(data, dtype=float)
                self.shape = data.shape
                size = data.size
                self.data = np.empty(size, dtype=object)
                data.shape = (size,)
                for i, d in enumerate(data):
                    self.data[i] = iv.mpf([d - eps, d + eps])
                self.data.shape = self.shape  # восстанавливаем размерности массива
            elif isinstance(data, np.ndarray):
                self.shape = data.shape
                size = data.size
                self.data = np.empty(size, dtype=object)
                data.shape = (size,)
                for i, d in enumerate(data):
                    self.data[i] = iv.mpf([d - eps, d + eps])
                self.data.shape = self.shape  # восстанавливаем размерности массива
            else:
                raise ValueError(
                    f"Недопустимые данные при инициализации массива интервалов: {data}, тип данных:{type(data)}"
                )

        def __str__(self):
            return str(self.data)

        def __repr__(self):
            return str(self)

        def __getitem__(self, ind):
            return self.data[ind]

        def __setitem__(self, ind, data):
            if isinstance(self, Ivl):
                self.data[ind] = data
            else:
                self[ind] = data

        @property
        def mid(self):
            size = self.data.size
            _mid = np.empty(size, dtype=float)
            self.data.shape = (size,)
            for i, d in enumerate(self.data):
                _mid[i] = float(d.mid)
            _mid.shape = self.shape
            self.data.shape = self.shape
            return _mid

        @property
        def a(self):
            size = self.data.size
            _a = np.empty(size, dtype=float)
            self.data.shape = (size,)
            for i, d in enumerate(self.data):
                _a[i] = float(d.a)
            _a.shape = self.shape
            self.data.shape = self.shape
            return _a

        @property
        def b(self):
            size = self.data.size
            _b = np.empty(size, dtype=float)
            self.data.shape = (size,)
            for i, d in enumerate(self.data):
                _b[i] = float(d.b)
            _b.shape = self.shape
            self.data.shape = self.shape
            return _b

        @property
        def delta(self):
            size = self.data.size
            _delta = np.empty(size, dtype=float)
            self.data.shape = (size,)
            for i, d in enumerate(self.data):
                _delta[i] = float(d.delta)
            _delta.shape = self.shape
            self.data.shape = self.shape

            return _delta

        def apply(self, f, args=(), delta=0.0):
            """
            Применение функции к массиву интервалов
            Параметры:
            f -функция с сигнатурой f(self.data, *args, delta=0.)
            args - дополнительные параметры, передаваемые функции,
            delta - аддитивная неопределенность, добавляемая при
                    вычислении функции.
            Функция возвращает массив интервалов
            """
            size = self.data.size
            self.data.shape = (size,)  # переходим к одномерному массиву
            _result = np.empty(size, dtype=object)
            for i, d in enumerate(self.data):
                _result[i] = iv.mpf(f(d, *args)) + iv.mpf([-delta, delta])
            _result.shape = self.shape
            self.data.shape = self.shape
            return Ivl(_result)

        def aggregate(self, f):
            """
            Применение функции агрегации (суммы, произведения)
            к данным экземпляра Ivl
            """
            s = f(self.data)       
            return Ivl(s)

        # унарные и бинарные операции
        def __pos__(self):
            return Ivl(self.data)

        def __neg__(self):
            return Ivl(-self.data)

        def __add__(self, other):       
            oth = other if isinstance(other, (int, float, str)) else other.data
            return Ivl(self.data + oth)

        def __radd__(self, other):
            oth = other if isinstance(other, (int, float, str)) else other.data
            return Ivl(self.data + oth)

        def __iadd__(self, other):
            oth = other if isinstance(other, (int, float, str)) else other.data
            return Ivl(self.data + oth)

        def __sub__(self, other):
            oth = other if isinstance(other, (int, float, str)) else other.data

            return Ivl(self.data - oth)

        def __rsub__(self, other):
            oth = other if isinstance(other, (int, float, str)) else other.data
            return Ivl(oth - self.data)

        def __isub__(self, other):
            oth = other if isinstance(other, (int, float, str)) else other.data
            return Ivl(self.data - oth)

        def __mul__(self, other):
            oth = other if isinstance(other, (int, float, str)) else other.data
            return Ivl(self.data * oth)

        def __rmul__(self, other):
            oth = other if isinstance(other, (int, float, str)) else other.data
            return Ivl(oth * self.data)

        def __imul__(self, other):
            oth = other if isinstance(other, (int, float, str)) else other.data
            return Ivl(self.data * oth)

        def __truediv__(self, other):
            oth = other if isinstance(other, (int, float, str)) else other.data
            return Ivl(self.data / oth)

        def __rtruediv__(self, other):
            oth = other if isinstance(other, (int, float, str)) else other.data
            return Ivl(oth / self.data)

        def __itruediv__(self, other):
            oth = other if isinstance(other, (int, float, str)) else other.data
            return Ivl(self.data / oth)

        def __pow__(self, other):
            oth = other if isinstance(other, (int, float, str)) else other.data
            return Ivl(self.data**oth)

        def __rpow__(self, other):
            oth = other if isinstance(other, (int, float, str)) else other.data
            return Ivl(oth**self.data)

        def __ipow__(self, other):
            oth = other if isinstance(other, (int, float, str)) else other.data
            return Ivl(self.data**oth)

        # элементарные функции
        def ln(self, delta=0.0):
            return self.apply(iv.ln)

        def ln10(self, delta=0.0):
            return self.apply(iv.ln10)

        def exp(self, delta=0.0):
            return self.apply(iv.exp)

        def sin(self, delta=0.0):
            return self.apply(iv.sin)

        def cos(self, delta=0.0):
            return self.apply(iv.cos)


@app.cell
def _():
    from scipy.integrate import quad

    def integral(f, ab=(0,1), n=10, epsx=0., epsf=0., dps=15):
        x = np.linspace(*ab, n+1) # разбиение ab на n частей
        h = (ab[1] - ab[0])/n
        xc = x + h/2
        xc = xc[:-1]
        Ivl.env(dps=dps)
        xci = Ivl(xc, eps=epsx)
        yi = xci.apply(f, delta=epsf)    
        sum = yi.aggregate(np.sum)*h # суммируем
        # погрешность
        err = np.abs(sum.mid - quad(f, ab[0], ab[1])[0])
        return sum, err, sum.delta

    integral(lambda x: x**4, n=100, epsx=1e-3, epsf=1e-3)

    return


@app.cell
def _():
    def diff(f, ab=(0,1), h=0.01, h_eps=0.):
        epsx = epsf = h * h_eps
        n = int((ab[1] - ab[0])/h)
        xi = Ivl(np.linspace(*ab, n+1), eps=epsx) 
        xim, xip = xi - h, xi + h
        yim = xim.apply(f, delta=epsf)
        yip = xip.apply(f, delta=epsf)
        d = (yip - yim)/(2*h)
        da = d.a
        dm = d.mid
        db = d.b
        ddelta = d.delta
    
        dmax = np.max(ddelta)
        return dmax

    _f = lambda x:x
    (diff(_f, h_eps=0.0001), diff(_f, h_eps=0.01),
     diff(_f, h_eps=1), diff(_f, h_eps=10),)
    return (diff,)


@app.cell
def _(diff):
    _f = lambda x:x**3
    (diff(_f, h_eps=0.0001), diff(_f, h_eps=0.01),
     diff(_f, h_eps=1), diff(_f, h_eps=10),)
    return


@app.cell
def _():
    def bar_ivl(
        u0=0.0,
        dx=0.1,
        tmax=0.1,
        dt=1e-5,
        alpha=1.0,
        C=1.0,
        D=10.0,
        p=1000.0,
        draw=True,
        xs=0.5,
        ls="-",
        eps=1e-6,
    ):
        nx = int(1.0 / dx + 1)  # число разбиений по x
        x = np.linspace(0.0, 1.0, nx)
        nt = int(tmax / dt + 1)  # число разбиений по t
        t = np.linspace(0.0, tmax, nt)
        A = dt / C * D / dx**2
        B = 2 * A + alpha * dt / C - 1
        P = Ivl.ones((nt, nx), eps=0) * (p + alpha * u0) * dt / C
        u = Ivl.zeros((nt, nx), eps=eps) + u0
        i = 0
        print(f"{u[i+1, 1:-1].shape=}, {type(u[i+1, 1:-1])=}")
        print(f"{A=}, {type(A)=}")
        print(f"{(A*u[i, 2:]).shape=}, {type(A*u[i, 2:])=}")
        print(f"{(A*u[i, 0:-2]).shape=}, {type(A*u[i, 0:-2])=}")
        print(f"{P[i, 1:-1].shape=}, {type(P[i, 1:-1])=}")
        print(f"{(B*u[i, 1:-1]).shape=}, {type(B*u[i, 1:-1])=}")
        u[i + 1, 1:-1] = (
            A * u[i, 2:] + A * u[i, 0:-2] + P[i, 1:-1] - B * u[i, 1:-1]
        )
        print(f"{u[i+1, 1:-1].shape=}, {type(u[i+1, 1:-1])=}")
        # print(f"{u.shape}")
        # v = - B*u[i, 1:-1]
        # print(f"{v.shape=}, {type(v)=}, {type(u)=}")
        # print(f"{type(B)=}, {type(u[i, 1:-1])=}")
        # u[i+1, 1:-1] += v
        # print(f"{u[i+1, 1:-1].shape=}")

        for i in range(nt - 1):  # цикл по времени
            print(f"{i=}, {type(u[i+1, 1:-1])=}, {type(u[i, 2:])=}")
            u[i + 1, 1:-1] = u[
                i, 2:
            ]  # A*u[i, 2:] #+ A*u[i, 0:-2] +  P[i, 1:-1] - B*u[i, 1:-1]
            # u[i+1, 1:-1] = A*u[i, 2:] - B*u[i, 1:-1] + A*u[i, 0:-2] + P[i, 1:-1]
        # return u, t, x

        # if draw:
        #     ix = int(u.shape[1]*xs)
        #     dxdt = dx/dt
        #     plt.plot(t, u[:, ix], lw=2, ls=ls,
        #              label=f'{dx=:7.5e}, dx/dt={dxdt:7.5e} ')
        #     plt.xlabel('t')
        #     plt.ylabel('u(t,x)')
        #     plt.legend(fontsize=8)
        # return u, t, x


    # bar_ivl(dt = 0.01)
    return


@app.cell
def _():
    _i = Ivl([1, 3, 4])
    4 * _i
    return


@app.cell
def _():
    # dx, dt, tmax = 0.05, 5e-6, 0.1
    # C, D, p, alpha, u0, eps = 1, 10, 1000, 1.0, 0, 1e-3
    # nx = int(1./dx + 1) # число разбиений по x
    # x = np.linspace(0.,1., nx)
    # nt = int(tmax/dt+1) # число разбиений по t
    # t = np.linspace(0., tmax, nt)
    # A = dt/C*D/dx**2
    # B = 2*A + alpha*dt/C - 1
    # P = Ivl.ones((nt, nx), eps=0)*(p + alpha*u0)*dt/C
    # u = Ivl.zeros((nt, nx), eps=eps)+u0
    # i = 0
    # print(f"{nt=}")
    # for i in range(nt-1):
    #     if i%100==0:
    #         print(f"{i=}, {nt=}")
    #     u[i+1, 1:-1] = A*u[i, 2:] + A*u[i, 0:-2] +  P[i, 1:-1] - B*u[i, 1:-1]
    #     #u.data[i+1, 1:-1] = A*u.data[i, 2:] + A*u.data[i, 0:-2] + P[i, 1:-1] - B*u.data[i, 1:-1]

    # u[-1, nx//2]
    return


@app.cell
def _():
    # u[-1, nx//2].delta, u[0, nx//2].delta, u[2, nx//2].delta
    return


@app.cell
def _():
    # Ivl([1,2,3], eps=0.1).mid
    return


if __name__ == "__main__":
    app.run()
