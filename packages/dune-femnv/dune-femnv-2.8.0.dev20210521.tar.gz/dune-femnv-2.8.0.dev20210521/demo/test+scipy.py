import math
from ufl import TrialFunction, TestFunction, SpatialCoordinate,FacetNormal,\
         inner, dot, grad, dx, ds, dS, as_vector, sin, pi, CellVolume, FacetArea, avg, jump
from dune.ufl import Space
from dune.grid import cartesianDomain
from dune.fem.function import integrate
import dune.create as create

from dune.fem import parameter

parameter.append({"fem.verboserank": 0, "fem.solver.verbose": 0,
    "fem.solver.errormeassure": "relative",
    "fem.preconditioning" : "true",
    "petsc.kspsolver.method": "gmres",
    "petsc.preconditioning.method": "hypre",
    "istl.preconditioning.method": "ilu",
    "istl.preconditioning.iterations": 0,
    "istl.preconditioning.relaxation": 0.9,
    "istl.gmres.restart": 50,
    "istl.preconditioning.fastilustorage": 1})
newtonParameters = {"linabstol": 1e-10, "reduction": 1e-10,
        "tolerance": 8e-7,
        "maxiterations": 20,
        "maxlineariterations": 15000,
        "verbose": "true", "linear.verbose": "false"}
solver = "cg"
# solver = ("suitesparse","umfpack")


def callback(xk):
    global num_iters
    num_iters += 1

grid = create.grid("ALUSimplex", cartesianDomain([0, 0], [1, 1], [4, 4]), dimgrid=2)
spc  = create.space("Lagrange", grid, dimrange=2, order=2, storage='eigen')
spc1 = create.space("Lagrange", grid, dimrange=1, order=2, storage='eigen')

space2 = Space((2,2),2)    # first component sigma, second u
u   = TrialFunction(space2)
v   = TestFunction(space2)
space1 = Space((2,2),1)    # for rhs
u1   = TrialFunction(space1)
v1   = TestFunction(space1)

cell = space2.cell()
x    = SpatialCoordinate(cell)
hT2  = CellVolume(cell)
hF   = FacetArea(cell)
he   = avg(hT2) / hF
he0  = hT2 / hF
n    = FacetNormal(cell)

f = 8.*pi*pi*sin(2*pi*x[0])*sin(2.*pi*x[1])
exact = as_vector([sin(2*pi*x[0])*sin(2.*pi*x[1])])

laplace = lambda w: grad(grad(w))[0,0] + grad(grad(w))[1,1]
b       = lambda w,q: dot(-laplace(w),q)*dx + jump(grad(w),n)*avg(q)*dS# + dot(grad(w),n)*q*ds

ah1  = lambda w,q: dot(grad(w),grad(q))*dx + 10./he0*w*q*ds
#ah1  = lambda w,q: dot(grad(w),grad(q))*dx + w*q*dx
sh1  = lambda w,q: 20./he0*w*q*ds \
                   + he * dot(jump(grad(w)), jump(grad(q)))*dS \
                   + hT2 * dot(laplace(w) + f, laplace(q)) * dx

al2  = lambda w,q: w*q*dx
sl2  = lambda w,q: 20./he0**3 * w*q*ds \
                   + 1./he * dot(jump(grad(w)), jump(grad(q)))*dS
                   #+ dot(laplace(w)+f,laplace(q)) * dx

a, s = ah1, sh1

#rhsForm = a(u1[0],v1[0]) - f*v1[0]*dx
#schemeRhs  = create.scheme("galerkin", spc1, rhsForm==0, solver=solver,
#                     parameters={"fem.solver.newton." + k: v for k, v in newtonParameters.items()})
#rhs = spc1.interpolate([0],name="rhs")

form = a(u[0],v[0]) + b(u[1],v[0]) - f*v[0]*dx +\
       b(v[1],u[0]) - s(u[1],v[1])
# form = a(u[0],v[0]) + b(u[1],v[0]) +\
#        b(v[1],u[0]+rhs[0]) - s(u[1],v[1])
# form = dot(grad(u[1]),grad(v[1]))*dx + u[0]*v[0]*dx + 20./he0*u[1]*v[1]*ds - f*v[1]*dx

scheme = create.scheme("galerkin", spc, form==0, solver=solver,
                     parameters={"fem.solver.newton." + k: v for k, v in newtonParameters.items()})
uh = spc.interpolate([0], name="solution")
import time
from math import log, sqrt
from norms import l2_norm, h1_norm
from scipy.sparse.linalg import LinearOperator, spsolve, cg, bicgstab, spilu, inv
l2_error = 10
h1_error = 10
for i in range(5):
    global num_iters
    num_iters = 0
    start_t = time.time()
    #schemeRhs.solve(target=rhs)
    #solution, info = scheme.solve()
    A = scheme.assemble(uh).as_numpy

    sol_coeff = uh.as_numpy
    rhs = uh.copy()
    rhs_coeff = rhs.as_numpy
    scheme(uh, rhs)
    rhs_coeff *= -1

    system_inverse = spilu( A )
    precond = LinearOperator( A.shape, system_inverse.solve)

    sol_coeff[:], info = cg(A, rhs_coeff, tol=1e-12, callback=callback, M=precond)
    total_t = time.time() - start_t
    l2_old_error = l2_error
    h1_old_error = h1_error
    l2_error = l2_norm(grid, uh[1] - exact[0])
    h1_error = h1_norm(grid, uh[1] - exact[0])
    #error = sqrt(integrate(grid,inner(solution[1]-exact[0],solution[1]-exact[0]),order=5))
    l2_eoc = log(l2_error/l2_old_error)/log(0.5)
    h1_eoc = log(h1_error/h1_old_error)/log(0.5)
    print(info,math.sqrt(l2_error),', l2 eoc:',l2_eoc,', h1 eoc:',h1_eoc,', time:',total_t, ', iters:', num_iters)
    #grid.writeVTK("test"+str(i),pointdata=[uh])
    grid.hierarchicalGrid.globalRefine(1)
