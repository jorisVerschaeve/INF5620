"""
Examples on approximating functions by global basis functions,
using the approx1D.py module.
"""
from approx1D import *
from Lagrange import *
from scitools.std import figure
import sympy as sm
import sys
x = sm.Symbol('x')


def sines(x, N):
    return [sm.sin(sm.pi*(i+1)*x) for i in range(N+1)]

def cosines(x, N):
    return [sm.cos(sm.pi*i*x) for i in range(N+1)]

def sines_cosines(x, N):
    c = [sm.cos(sm.pi*i*x) for i in range(N+1)]
    s = [sm.sin(sm.pi*i*x) for i in range(1, N+1)]
    return c + s

def taylor(x, N):
    return [x**i for i in range(N+1)]


# ----------------------------------------------------------------------

def run_linear():
    f = 10*(x-1)**2 - 1
    psi = [1, x]
    Omega = [1, 2]
    u = least_squares(f, psi, Omega)
    comparison_plot(f, u, Omega, 'parabola_ls_linear.pdf')

def run_linear2(N=2):
    """
    Test Taylor approx to a parabola and exact symbolics vs
    ill-conditioned numerical approaches.
    """
    f = 10*(x-1)**2 - 1
    u = least_squares(f, psi=[x**i for i in range(N+1)], Omega=[1, 2])
    # Note: in least_squares there is extra code for numerical solution
    # of the systems
    print 'f:', sm.expand(f)
    print 'u:', sm.expand(u)
    comparison_plot(f, u, [1, 2], 'parabola_ls_taylor%d.pdf' % N)

def run_sines(help=False):
    for N in (4, 12):
        f = 10*(x-1)**2 - 1
        psi = sines(x, N)
        Omega = [0, 1]
        if help:  # u = 9 + sum
            f0 = 9; f1 = -1
            term = f0*(1-x) + x*f1
            u = term + least_squares_orth(f-term, psi, Omega)
        else:
            u = least_squares_orth(f, psi, Omega)
        figure()
        comparison_plot(f, u, Omega, 'parabola_ls_sines%d%s.pdf' %
                        (N, '_wfterm' if help else ''))


def run_sine_by_powers(N):
    f = sm.sin(x)
    psi = taylor(x, N)
    Omega=[0, 2*sm.pi]
    u = least_squares(f, psi, Omega)
    comparison_plot(f, u, Omega)

def run_Lagrange_poly(N):
    # Test of symbolic and numeric evaluation of Lagrange polynomials
    psi, points = Lagrange_polynomials_01(x, N)
    print psi
    print points
    x = 0.5
    psi, points = Lagrange_polynomials_01(x, N)
    print psi
    print points


def run_Lagrange_sin(N):
    # Least-squares use of Lagrange polynomials
    f = sm.sin(2*sm.pi*x)
    psi, points = Lagrange_polynomials_01(x, N)
    Omega=[0, 1]
    u = least_squares(f, psi, Omega)
    comparison_plot(f, u, Omega, filename='Lagrange_ls_sin_%d.pdf' % (N+1),
                    plot_title='Least squares approximation by '\
                    'Lagrange polynomials of degree %d' % N)

def run_Lagrange_abs(N):
    """Least-squares with of Lagrange polynomials for |1-2x|."""
    f = sm.abs(1-2*x)
    # This f will lead to failure of sympy integrate, fallback on numerical int.
    psi, points = Lagrange_polynomials_01(x, N)
    Omega=[0, 1]
    u = least_squares(f, psi, Omega)
    comparison_plot(f, u, Omega, filename='Lagrange_ls_abs_%d.pdf' % (N+1),
                    plot_title='Least squares approximation by '\
                    'Lagrange polynomials of degree %d' % N)

def run_linear_interpolation1():
    f = 10*(x-1)**2 - 1
    psi = [1, x]
    Omega = [1, 2]
    points = [1 + sm.Rational(1,3), 1 + sm.Rational(2,3)]
    u = interpolation(f, psi, points)
    comparison_plot(f, u, Omega, 'parabola_interp1_linear.pdf')


def run_linear_interpolation2():
    f = 10*(x-1)**2 - 1
    psi = [1, x]
    Omega = [1, 2]
    points = [1, 2]
    u = interpolation(f, psi, points)
    comparison_plot(f, u, Omega, 'parabola_interp2_linear.pdf')


def run_poly_interp_sin(N):
    f = sm.sin(sm.pi*x)
    psi = taylor(x, N)
    Omega = [1, 2]
    import numpy as np
    points = np.linspace(1, 2, N+1)
    u = interpolation(f, psi, points)
    comparison_plot(f, u, Omega, 'sin_interp_poly%d.pdf' % N)


def run_Lagrange_interp_sin(N):
    f = sm.sin(2*sm.pi*x)
    psi, points = Lagrange_polynomials_01(x, N)
    u = interpolation(f, psi, points)
    comparison_plot(f, u, Omega=[0, 1],
                    filename='Lagrange_interp_sin_%d.pdf' % (N+1),
                    plot_title='Interpolation by Lagrange polynomials '\
                    'of degree %d' % N)

def run_Lagrange_interp_poly(n, N):
    f = x**n
    psi, points = Lagrange_polynomials_01(x, N)
    u = interpolation(f, psi, points)
    comparison_plot(f, u, Omega=[0, 1],
                    filename='Lagrange_interp_p%d_%d.pdf' % (n, N+1),
                    plot_title='Interpolation by Lagrange polynomials '\
                    'of degree %d' % N)

def run_Lagrange_interp_abs(N, ymin=None, ymax=None):
    f = abs(1-2*x)
    psi, points = Lagrange_polynomials_01(x, N)
    u = interpolation(f, psi, points)
    comparison_plot(f, u, Omega=[0, 1],
                    filename='Lagrange_interp_abs_%d.pdf' % (N+1),
                    plot_title='Interpolation by Lagrange polynomials '\
                    'of degree %d' % N, ymin=ymin, ymax=ymax)
    # Make figures of Lagrange polynomials (psi)
    figure()
    xcoor = linspace(0, 1, 1001)
    for i in (2, (N+1)/2+1):
        fn = lambdify([x], psi[i])
        ycoor = fn(xcoor)
        plot(xcoor, ycoor)
        legend(r'\psi_%d' % i)
        hold('on')
        plot(points, [fn(xc) for xc in points], 'ro')
    #if ymin is not None and ymax is not None:
    #    axis([xcoor[0], xcoor[-1], ymin, ymax])
    savefig('Lagrange_basis_%d.pdf' % (N+1))

def run_Lagrange_interp_abs_Cheb(N, ymin=None, ymax=None):
    f = abs(1-2*x)
    psi, points= Lagrange_polynomials(x, N, [0, 1],
                                      point_distribution='Chebyshev')
    u = interpolation(f, psi, points)
    comparison_plot(f, u, Omega=[0, 1],
                    filename='Lagrange_interp_abs_Cheb_%d.pdf' % (N+1),
                    plot_title='Interpolation by Lagrange polynomials '\
                    'of degree %d' % N, ymin=ymin, ymax=ymax)

def run_Lagrange_interp_abs_conv(N=[3, 6, 12, 24]):
    f = sm.abs(1-2*x)
    f = sm.sin(2*sm.pi*x)
    fn = lambdify([x], f, modules='numpy')
    resolution = 50001
    import numpy as np
    xcoor = np.linspace(0, 1, resolution)
    fcoor = fn(xcoor)
    Einf = []
    E2 = []
    h = []
    for _N in N:
        psi, points = Lagrange_polynomials_01(x, _N)
        u = interpolation(f, psi, points)
        un = lambdify([x], u, modules='numpy')
        ucoor = un(xcoor)
        e = fcoor - ucoor
        Einf.append(e.max())
        E2.append(np.sqrt(np.sum(e*e/e.size)))
        h.append(1./_N)
    print Einf
    print E2
    print h
    print N
    # Assumption: error = CN**(-N)
    print 'convergence rates:'
    for i in range(len(E2)):
        C1 = E2[i]/(N[i]**(-N[i]/2))
        C2 = Einf[i]/(N[i]**(-N[i]/2))
        print N[i], C1, C2
    # Does not work properly...


if __name__ == '__main__':
    functions = \
        [eval(fname) for fname in dir() if fname.startswith('run_')]
    from scitools.misc import function_UI
    cmd = function_UI(functions, sys.argv)
    eval(cmd)
