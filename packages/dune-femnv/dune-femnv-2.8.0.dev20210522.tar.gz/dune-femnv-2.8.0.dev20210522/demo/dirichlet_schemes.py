import dune.create as create
import ufl
import time
import numpy as np
from dune.fem import parameter
from dune.ufl import DirichletBC, Space
from math import sqrt
from scipy.optimize import newton_krylov
from scipy.sparse import coo_matrix, bmat
from scipy.sparse.linalg import LinearOperator, spsolve, cg, bicgstab, spilu, inv
from ufl import *

ufl_space = Space((2, 2), 1)
u = ufl.TrialFunction(ufl_space)
v = ufl.TestFunction(ufl_space)
x = ufl.SpatialCoordinate(ufl_space.cell())
n = FacetNormal(ufl_space.cell())
#hT = MaxCellEdgeLength(ufl_space.cell())
hT2 = CellVolume(ufl_space.cell())
hF = FacetArea(ufl_space.cell())
he = avg(hT2) / hF
he0 = hT2 / hF
dirichletBC0 = DirichletBC(ufl_space, as_vector([ 0 ]), 1)

def callback(system, rhs):
    def callback_(xk):
        global num_iters
        num_iters += 1
        tmp = system*xk - rhs
        print(num_iters, ", norm of err:", sqrt(tmp.dot(tmp)))
    return callback_

###################################################
# minimization using (B^T M^-1 B + S)u = B^T M^-1 f

def solve(scheme, uh, A, exact, dirichletBC, version=None, beta=20, use_cg=True):
    print("\n# version =", version)
    space = scheme.space
    grid = space.grid
    sol_coeff = uh.as_numpy
    polOrder = space.order
    start_time = time.time()

    # main assembly
    if version == 'l2H' or version == "l2D2":
        print("using l2 minimization")
        mass_model = inner(u, v)*dx == 0
        mainScheme = create.scheme("h1", mass_model, space)
    elif version == 'h1H' or version == "h1D2":
        print("using h1 minimization")
        subVersion = "weak"
        if subVersion == "strong":
            print("h1 with strong bc")
            laplace_model = inner(grad(u), grad(v))*dx == 0
            mainScheme = create.scheme("h1", [laplace_model, dirichletBC0], space)
        elif subVersion == "weak":
            print("h1 with weak bc")
            gamma = 10
            laplace = inner(grad(u), grad(v))*dx + gamma/he0*u[0]*v[0]*ds \
                        - dot(A*grad(u[0]), n)*v[0]*ds - dot(A*grad(v[0]), n)*u[0]*ds
            laplace_model = create.model("integrands", grid, laplace == 0)
            mainScheme = create.scheme("galerkin", laplace_model, space)
    else:
        print("not using minimization")
        mainScheme = None

    # penalty assembly
    if version == "l2H":
        s = beta/he0**3 * inner(u, v) * ds # weak Dirichlet
        penalty = create.scheme("galerkin", s == 0, space, solver='cg')
    elif version == "h1H":
        s = beta/he0 * inner(u, v) * ds
        penalty = create.scheme("galerkin", s == 0, space, solver='cg')
    elif version == "l2D2":
        sigma = 1
        beta = 1
        s  = sigma/he * inner( jump(grad(u[0])), jump(grad(v[0])) ) * dS \
             + sigma * inner(A, grad(grad(u[0] - exact[0]))) * inner(A, grad(grad(v[0]))) * dx \
             + beta/he0**3 * inner(u, v) * ds
        penalty = create.scheme("galerkin", s == 0, space, solver='cg')
    elif version == "h1D2":
        sigma = 0.1
        s  = sigma*he * inner( jump(grad(u[0])), jump(grad(v[0])) ) * dS \
             + sigma*hT2 * inner(A, grad(grad(u[0] - exact[0]))) * inner(A, grad(grad(v[0]))) * dx \
             + beta/he0 * inner(u, v) * ds
        penalty = create.scheme("galerkin", s == 0, space, solver='cg')
    else:
        penalty = None

    # system matrix assembly
    B  = scheme.assemble(uh).as_numpy
    if not mainScheme is None:
        BT = B.transpose(copy=True)
        M = mainScheme.assemble(uh).as_numpy.tocsc()
        S  = -penalty.assemble(uh).as_numpy
        system = bmat([[M, B], [BT, None]])
    else:
        system = B

    # rhs assembly
    rhs = uh.copy()
    rhs_pen = uh.copy()
    sigma = uh.copy()
    sigma.clear()
    rhs_coeff = rhs.as_numpy
    rhs_pen_coeff = rhs_pen.as_numpy
    sigma_coeff = sigma.as_numpy
    scheme(uh, rhs)
    rhs_coeff *= -1
    scheme.setConstraints(rhs)
    if not mainScheme is None:
        # penalty(uh, rhs_pen)
        full_rhs = np.concatenate((rhs_coeff, rhs_pen_coeff))
        full_sol = np.concatenate((sol_coeff, sigma_coeff))
    else:
        full_rhs = rhs_coeff

    assembly_time = time.time() - start_time
    print("assembly took ", assembly_time, "s")
    print("#####################################")
    print("starting solver")
    start_time = time.time()
    global num_iters
    num_iters = 0

    #system_inverse = spilu( system.tocsc()) # ,fill_factor=50,drop_tol=1e-6)
    #precond = LinearOperator( system.shape, system_inverse.solve)
    #print("NNZ:",system_inverse.nnz,system.nnz)
    precond = None

    if 1:
        from matrix import is_symmetric#, eigen
        print("system matrix is symmetric: ", is_symmetric(system))
        use_cg = is_symmetric(system)
        #eigen(-system)
    if use_cg:
        solver = 'cg'
    else:
        solver = 'bicgstab'

    from scipy.sparse.linalg.interface import IdentityOperator
    precond = None # IdentityOperator(shape=system.shape, dtype=system.dtype)
    if True:
        full_sol, info = cg(system, full_rhs, callback=callback(system, full_rhs), tol=1e-12, M=precond, maxiter=1e6)
    else:
        full_sol, info = bicgstab(system, full_rhs, callback=callback(system, full_rhs), tol=1e-12, M=precond, maxiter=1e6)
    if not mainScheme is None:
        sol_coeff[:] = np.split(full_sol, 2)[1]
    else:
        sol_coeff[:] = full_sol

    solve_time = time.time() - start_time
    print("solving took ", solve_time, "s")
    print("#####################################")
    return uh, {'convergence': info, 'linear_iterations': num_iters, 'time': assembly_time + solve_time }, solver

def rhs(A, exact):
    b = -inner(A, grad(grad(exact[0])))*v[0]*dx
    return b

def nvdg(A, exact, dirichletBC, space, solver="bicgstab", parameters=None, beta=20):
    grid = space.grid
    a = -inner(A, grad(grad(u[0])))*v[0]*dx
    b = rhs(A, exact)
    # scheme = create.scheme("nv", space, a==b, penalty=beta, solver=solver, parameters=parameters, polOrder=space.order)
    scheme = create.scheme("nv", space, [a==b, dirichletBC], constraints="dirichlet", solver=solver, parameters=parameters, polOrder=space.order)
    return scheme

def h1H(A, exact, dirichletBC, space, solver="cg", parameters=None):
    return nvdg(A, exact, dirichletBC, space, solver=solver, parameters=parameters, beta=0)

def l2H(A, exact, dirichletBC, space, solver="cg", parameters=None):
    return nvdg(A, exact, dirichletBC, space, solver=solver, parameters=parameters, beta=0)

def l2D2(A, exact, dirichletBC, space, solver="cg", parameters=None):
    grid = space.grid
    a = -inner(A, grad(grad(u[0])))*v[0]*dx \
        + jump(A*grad(u[0]), n)*avg(v[0])*dS
    b = rhs(A, exact)
    scheme = create.scheme("galerkin", a == b, space, solver=solver, parameters=parameters)
    return scheme

def h1D2(A, exact, dirichletBC, space, solver="cg", parameters=None):
    return l2D2(A, exact, dirichletBC, space, solver=solver, parameters=parameters)

def var(A, exact, dirichletBC, space, solver="cg", parameters=None, beta=20):
    grid = space.grid
    a = inner(A*grad(u[0]), grad(v[0]))*dx
    if div(A) != ufl.as_vector( [0, 0] ):
        print('non-constant A used')
        a += inner(div(A), grad(u[0]))*v[0]*dx
    if False:
        a += beta/he0*inner(u, v)*ds \
             - dot(A*grad(u[0]), n)*v[0]*ds \
             - dot(A*grad(v[0]), n)*u[0]*ds
    b = rhs(A, exact)
    scheme = create.scheme("galerkin", [a==b,dirichletBC], space, solver=solver, parameters=parameters)
    # scheme = create.scheme("nv", space, a==b, solver=solver, penalty=beta, parameters=parameters)
    return scheme

# http://www.math.ualberta.ca/ijnam/Volume-14-2017/No-2-17/2017-02-08.pdf
def mu(A, exact, dirichletBC, space, solver="cg", parameters=None, beta=1):
    a = inner(A, grad(grad(u[0] - exact[0])))*inner(A, grad(grad(v[0])))*dx
    s = beta/he * inner( jump(grad(u[0])), jump(grad(v[0])) ) * dS \
        + beta/hF**3 * inner(u, v) * ds
    scheme = create.scheme("galerkin", a + s == 0, space, solver=solver, parameters=parameters)
    return scheme

# https://arxiv.org/pdf/1505.02842.pdf
def feng(A, exact, dirichletBC, space, solver="bicgstab", parameters=None, beta=20):
    a = -inner(A, grad(grad(u[0] - exact[0])))*v[0]*dx
    s = jump(A*grad(u[0]), n) * avg(v[0]) * dS \
        + beta/hF * inner(u - exact, v) * ds
        #- dot(A*grad(u[0]), n)*v[0]*ds - dot(A*grad(v[0]), n)*u[0]*ds # reduces EOC to 1.5

    scheme = create.scheme("galerkin", a + s == 0, space, solver=solver, parameters=parameters)
    return scheme

#http://eprints.maths.ox.ac.uk/1623/1/NA-12-17.pdf - p9
def smears(A, exact, dirichletBC, space, solver="bicgstab", parameters=None):
    gamma = (A[0][0] + A[1][1])/inner(A, A)
    mu = 20.
    eta = 20.
    a = gamma*inner(A, grad(grad(u[0] - exact[0])))*div(grad(v[0]))*dx \
        + 0.5*inner( grad(grad(u[0] - exact[0])), grad(grad(v[0])) )*dx \
        - 0.5*div(grad(u[0] - exact[0]))*div(grad(v[0]))*dx
    s1 = 0.5*(avg(div(grad(u[0])))*jump(grad(v[0]), n)
         + avg(div(grad(v[0])))*jump(grad(u[0]), n))*dS \
         + mu*jump(grad(u[0]), n)*jump(grad(v[0]), n)*dS
    s2 = -0.5*( inner(grad(inner(grad(u[0] - exact[0]), n)), grad(v[0]))
         + inner(grad(inner(grad(v[0]), n)), grad(u[0] - exact[0])) )*ds \
         + mu*inner(grad(u[0] - exact[0]), grad(v[0]))*ds \
         + eta*inner(u - exact, v)*ds

    scheme = create.scheme("galerkin", a + s1 + s2 == 0, space, solver=solver, parameters=parameters)
    return scheme

schemeDict = {"nvdg": nvdg, "h1H": h1H, "l2H": l2H, "var": var, "mu": mu, "feng": feng, "smears": smears, "h1D2": h1D2, "l2D2": l2D2}

######################################
# matrix free (newton-krylov) approach

def matrix_free(scheme, uh):
    sol_coeff = uh.as_numpy
    space = scheme.space
    res = uh.copy()
    res_coeff = res.as_numpy
    def f(x_coeff):
        x = space.numpyFunction(x_coeff, "tmp")
        scheme(x, res)
        return res_coeff
    sol_coeff[:] = newton_krylov(f, sol_coeff, verbose=1, f_tol=1e-8)
