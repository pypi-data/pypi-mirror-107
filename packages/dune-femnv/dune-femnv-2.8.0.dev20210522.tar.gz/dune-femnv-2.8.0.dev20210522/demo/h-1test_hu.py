# Demo for comparing H-1 norm of A:H[u - I_h u]
from dune.grid import cartesianDomain
from dune.fem import parameter
from dune.fem.plotting import plotPointData as plot
from math import sqrt, log
from dune.ufl import DirichletBC, Space, expression2GF
import math
import ufl
from ufl import cos, exp, sin, pi, inner, grad, div, dx, ds, as_vector, replace

import dune.create as create

order = 1
parameters = {"fem.solver.newton.verbose": 1,
              "fem.solver.newton.linear.verbose": 1}

grid = create.grid("ALUSimplex", cartesianDomain([0, 0], [1, 1], [8, 8]), dimgrid=2)
space1 = create.space("Lagrange", grid, dimrange=1, order=order, storage='istl')
space2 = create.space("Lagrange", grid, dimrange=1, order=order+1, storage='istl')

ufl_space = Space((grid.dimGrid, grid.dimWorld), 1)
u = ufl.TrialFunction(ufl_space)
v = ufl.TestFunction(ufl_space)
x = ufl.SpatialCoordinate(ufl_space.cell())
dirichletBC = DirichletBC(ufl_space, as_vector([ 0 ]), 1)
exact = as_vector( [sin(2*pi*x[0])*sin(2*pi*x[1])] )
uh = space1.interpolate(exact, name="uh")
E = exact - uh
laplace_E = grad(grad(E))[0, 0, 0] + grad(grad(E))[0, 1, 1]

if 1: # use H[exact-uh]
    aH = (grad(grad(u))[0, 0, 0] + grad(grad(u))[0, 1, 1]) * v[0] * dx
    modelH = create.model("nvdg", grid, aH==0, dirichletBC)
    schemeH = create.scheme("nvdg", space2, modelH, polOrder=4)
    Hu_v = space2.interpolate([0], name="H[u].v")
    b = 0
else:
    b = inner(laplace_E, v[0])*dx

a = inner(grad(u), grad(v))*dx
model = create.model("elliptic", grid, a==b, dirichletBC)
scheme = create.scheme("h1", space2, model)

for eocLoop in range(4):
    print('# step:', eocLoop, ", size:", grid.size(0))
    if 1:
        # schemeH(laplace_E, MHu) # bug: should get this to work...
        E_h = space2.interpolate(E, name="tmp")
        schemeH(E_h, Hu_v)
        solution,_ = scheme.solve(rhs=Hu_v)
    else:
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
    print('H-1 error:', h1_error, ', eoc:', h1eoc)
    # plot(solution)
    print('H-1 error with E:', h1_error2, ', eoc:', h1eoc2)
    #plot(h1_error2_gf)
    grid.hierarchicalGrid.globalRefine(1)
    uh.interpolate(exact)
exit()
