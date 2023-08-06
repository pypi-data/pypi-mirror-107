# Demo for comparing H-1 norm of A:D^2(u - I_h u)
from dune.grid import cartesianDomain
from dune.fem import parameter
from dune.fem.plotting import plotPointData as plot
import matplotlib.pyplot as plt
from math import sqrt, log
from dune.ufl import DirichletBC, Space
import math
import ufl
from ufl import cos, exp, sin, pi, inner, grad, div, dx, ds, as_vector, replace

import dune.create as create

parameters = {"fem.solver.newton.verbose": 1,
              "fem.solver.newton.linear.verbose": 1}

grid = create.grid("ALUSimplex", cartesianDomain([0, 0], [1, 1], [4, 4]), dimgrid=2)
space2 = create.space("Lagrange", grid, dimrange=1, order=2, storage='istl')
space3 = create.space("Lagrange", grid, dimrange=1, order=3, storage='istl')

ufl_space = Space((grid.dimGrid, grid.dimWorld), 1)
u = ufl.TrialFunction(ufl_space)
v = ufl.TestFunction(ufl_space)
x = ufl.SpatialCoordinate(ufl_space.cell())
exact = as_vector( [sin(2*pi*x[0])*sin(2*pi*x[1])] )
#exact = as_vector( [pow(x[0], 4/3) - pow(x[1], 4/3)] )
uh = space2.interpolate(exact, name="uh")
E = exact - uh

laplace_E = grad(grad(E))[0, 0, 0] + grad(grad(E))[0, 1, 1]
#laplace_E = (1 + x[0]*x[1])*grad(grad(E))[0, 0, 0] +\
#            (1 + x[0]*x[1])*grad(grad(E))[0, 1, 1]
#laplace_E = 16/9*(pow(x[0], 2/3)*grad(grad(E))[0, 0, 0] \
#            - pow(x[0], 1/3)*pow(x[1], 1/3)*grad(grad(E))[0, 0, 1] \
#            - pow(x[0], 1/3)*pow(x[1], 1/3)*grad(grad(E))[0, 1, 0] \
#            + pow(x[1], 2/3)*grad(grad(E))[0, 1, 1])
a = inner(grad(u), grad(v))*dx
b = inner(laplace_E, v[0])*dx
dirichletBC = DirichletBC(ufl_space, as_vector([ 0 ]), 1)
model = create.model("elliptic", grid, a==b, dirichletBC)

scheme = create.scheme("h1", space3, model)

for eocLoop in range(4):
    print('# step:', eocLoop, ", size:", grid.size(0))
    solution,_ = scheme.solve()
    l2_error_gf = create.function("ufl", grid, "l2error", 5, inner(laplace_E, laplace_E))
    l2_error = sqrt(l2_error_gf.integrate()[0])
    h1_error_gf = create.function("ufl", grid, "h1error", 5, inner(grad(solution), grad(solution)))
    h1_error = sqrt(h1_error_gf.integrate()[0])
    h1_error2_gf = create.function("ufl", grid, "h1error2", 5, inner(grad(E), grad(E)))
    h1_error2 = sqrt(h1_error2_gf.integrate()[0])
    if eocLoop == 0:
        l2eoc = 'n/a'
        h1eoc = 'n/a'
        h1eoc2 = 'n/a'
    else:
        l2eoc = log(l2_error/l2_error_old)/log(0.5)
        h1eoc = log(h1_error/h1_error_old)/log(0.5)
        h1eoc2 = log(h1_error2/h1_error2_old)/log(0.5)
    l2_error_old = l2_error
    h1_error_old = h1_error
    h1_error2_old = h1_error2
    print('L2 error:', l2_error, ', eoc:', l2eoc)
    plot(l2_error_gf)
    print('H-1 error:', h1_error, ', eoc:', h1eoc)
    plot(h1_error_gf)
    print('grad error:', h1_error2, ', eoc:', h1eoc2)
    plot(h1_error2_gf)
    grid.hierarchicalGrid.globalRefine(1)
    uh.interpolate(exact)
exit()
