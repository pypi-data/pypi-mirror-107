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

# defining h for DG terms
ufl_space = Space((2, 2), 1)
u = ufl.TrialFunction(ufl_space)
v = ufl.TestFunction(ufl_space)
x = ufl.SpatialCoordinate(ufl_space.cell())
n = FacetNormal(ufl_space.cell())
hT2 = CellVolume(ufl_space.cell())
hF = FacetArea(ufl_space.cell())
he = avg(hT2) / hF
he0 = hT2 / hF

# solver callback showing iteration count and residual error
def callback(system, rhs):
    def callback_(xk):
        global num_iters
        num_iters += 1
        tmp = system*xk - rhs
        print(num_iters, ", norm of err:", sqrt(tmp.dot(tmp)))
    return callback_

# main solve method
def solve(scheme, uh, A, exact, dirichletBC, version=None, use_cg=True, beta=20):
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
            mainScheme = create.scheme("h1", [laplace_model, dirichletBC], space)
        elif subVersion == "weak":
            print("h1 with weak bc")
            laplace = inner(grad(u), grad(v))*dx + beta/he0*u[0]*v[0]*ds
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
        #beta = 1
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
        system = bmat([[M, B], [BT, S]])
    else:
        system = B

    # rhs assembly
    rhs = uh.copy()
    rhs_pen = uh.copy()
    sigma = uh.copy()
    rhs_coeff = rhs.as_numpy
    rhs_pen_coeff = rhs_pen.as_numpy
    sigma_coeff = sigma.as_numpy
    scheme(uh, rhs)
    rhs_coeff *= -1
    if not mainScheme is None:
        penalty(uh, rhs_pen)
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

    # preconditioning
    if version == 'l2D2':
        tol = 1e-12
    elif version == 'l2H' or version == 'h1H' or version == 'h1D2':
        tol = 1e-7
    elif version == 'mu' or version == 'feng' or version == 'nvdg' or version == 'var':
        tol = 1e-5
    system_inverse = spilu( system.tocsc(), fill_factor=50, drop_tol=tol)
    #print("non zero:", system.nnz, system_inverse.nnz, "factor:", system_inverse.nnz/system.nnz)
    precond = LinearOperator( system.shape, system_inverse.solve)
    # print("NNZ:",system_inverse.nnz,system.nnz)

    # check symmetry
    from matrix import is_symmetric, eigen
    print("system matrix is symmetric: ", is_symmetric(system))
    use_cg = is_symmetric(system)
    if use_cg:
        solver = 'cg'
    else:
        solver = 'bicgstab'
    eigen(system)

    if use_cg:
        full_sol, info = cg(system, full_rhs, callback=callback(system, full_rhs), tol=1e-9, M=precond, maxiter=1e6)
    else:
        full_sol, info = bicgstab(system, full_rhs, callback=callback(system, full_rhs), tol=1e-9, M=precond, maxiter=1e6)
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

def h1H(A, exact, dirichletBC, space, solver="cg", beta=0):
    a = inner(A, grad(grad(u[0])))*v[0]*dx
    b = -rhs(A, exact)
    scheme = create.scheme("nv", space, a==b, penalty=0, solver=solver, polOrder=space.order)
    # scheme = create.scheme("nv", space, [a==b, dirichletBC], constraints="dirichlet", solver=solver, polOrder=space.order)
    return scheme

def l2H(A, exact, dirichletBC, space, solver="cg", beta=0):
    return h1H(A, exact, dirichletBC, space, solver=solver)

def nvdg(A, exact, dirichletBC, space, solver="bicgstab", beta=20):
    a = -inner(A, grad(grad(u[0])))*v[0]*dx
    b = rhs(A, exact)
    scheme = create.scheme("nv", space, a==b, penalty=beta, solver=solver, polOrder=space.order)
    return scheme

def l2D2(A, exact, dirichletBC, space, solver="cg", beta=0):
    a = inner(A, grad(grad(u[0])))*v[0]*dx \
        - jump(A*grad(u[0]), n)*avg(v[0])*dS
    b = -rhs(A, exact)
    scheme = create.scheme("galerkin", a == b, space, solver=solver)
    return scheme

def h1D2(A, exact, dirichletBC, space, solver="cg", beta=0):
    return l2D2(A, exact, dirichletBC, space, solver=solver)

def var(A, exact, dirichletBC, space, solver="cg", beta=20):
    a = inner(A*grad(u[0]), grad(v[0]))*dx
    if div(A) != ufl.as_vector( [0, 0] ):
        print('non-constant A used')
        a += inner(div(A), grad(u[0]))*v[0]*dx
    a += beta/he0*inner(u, v)*ds \
         - dot(A*grad(u[0]), n)*v[0]*ds
         #- dot(A*grad(v[0]), n)*u[0]*ds
    b = rhs(A, exact)
    scheme = create.scheme("galerkin", a==b, space, solver=solver)
    return scheme

# http://www.math.ualberta.ca/ijnam/Volume-14-2017/No-2-17/2017-02-08.pdf
def mu(A, exact, dirichletBC, space, solver="cg", beta=1):
    a = inner(A, grad(grad(u[0] - exact[0])))*inner(A, grad(grad(v[0])))*dx
    s = 1/he * inner( jump(grad(u[0])), jump(grad(v[0])) ) * dS \
        + 1/hF**3 * inner(u, v) * ds
    scheme = create.scheme("galerkin", a + s == 0, space, solver=solver)
    return scheme

# https://arxiv.org/pdf/1505.02842.pdf
def feng(A, exact, dirichletBC, space, solver="bicgstab", beta=20):
    a = -inner(A, grad(grad(u[0])))*v[0]*dx
    b = rhs(A, exact)
    s = jump(A*grad(u[0]), n) * avg(v[0]) * dS \
        + beta/hF * inner(u, v) * ds
        #- dot(A*grad(u[0]), n)*v[0]*ds - dot(A*grad(v[0]), n)*u[0]*ds # reduces EOC to 1.5
    scheme = create.scheme("galerkin", a + s == b, space, solver=solver)
    return scheme

schemeDict = {"nvdg": nvdg, "h1H": h1H, "l2H": l2H, "var": var, "mu": mu, "feng": feng, "h1D2": h1D2, "l2D2": l2D2}
