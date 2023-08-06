import math
import ufl
from ufl import *
from dune.ufl import Space, DirichletBC
import dune.create as create

dimGrid = 2
dimWorld = 2
ufl_space = Space((dimGrid, dimWorld), 1)
u = ufl.TrialFunction(ufl_space)
v = ufl.TestFunction(ufl_space)
x = ufl.SpatialCoordinate(ufl_space.cell())
n = FacetNormal(ufl_space.cell())
hT = CellVolume(ufl_space.cell())
hF = FacetArea(ufl_space.cell())
heInv = hF / avg( hT )
mu = 1.

def exp_solution():
    exact = as_vector( [exp(-10*(x[0]*x[0] + x[1]*x[1]))] )
    dirichletBC = DirichletBC(ufl_space, as_vector([ 0 ]), 1)
    return exact, dirichletBC

def smooth_solution():
    exact = as_vector( [sin(2*pi*x[0])*sin(2*pi*x[1])] )
    dirichletBC = DirichletBC(ufl_space, as_vector([ 0 ]), 1)
    return exact, dirichletBC

def rough_solution():
    exact = as_vector( [pow(x[0], 4/3) - pow(x[1], 4/3)] )
    dirichletBC = DirichletBC(ufl_space, as_vector([ 0 ]), 1)
    return exact, dirichletBC

def advection():
    A = as_matrix( [[sqrt(x[0] + 1e-12), 0], [0, sqrt(x[1] + 1e-12)]] )
    return A

def advection2():
    A = as_matrix( [[1, 0], [0, atan(5000*(x[0]*x[0] + x[1]*x[1] - 1)) + 2]] )
    return A

def full_hessian():
    A = as_matrix( [[1, 0.4], [0.4, 1]] )
    return A

def laplace():
    A = as_matrix( [[1, 0], [0, 1]] )
    return A

def nonD():
    A = as_matrix( [[1, 0],
        [0, ((x[0] - 0.51)**(2) * (x[1] - 0.61)**(2))**(1/12) + 1]] )
    return A

def nonD1():
    A = as_matrix( [ [100.*(abs(x[0] - 0.251) + abs(x[1] - 0.2565))**0.1 + 1, 0] ,
                     [0, (abs(x[0] - 0.251) + abs(x[1] - 0.2565))**0.1 + 1]] )
    return A


def nonD2():
    A = as_matrix( [[1, pow(x[0], 2/3)*pow(x[1], 2/3)],
                    [pow(x[0], 2/3)*pow(x[1], 2/3), 2]] )
    return A

def nonD3():
    A = as_matrix( [[1, 0],
                    [0, ((x[0] - 0.51)**(2) * (x[1] - 0.61)**(2))**(1.8+1/12) + 1]] )
    return A

def non_smooth():
    A = as_matrix( [[abs(x[0] - 0.5)**0.5*abs(x[1] - 0.5)**0.5 + 1, 0],
                    [0, abs(x[0] - 0.5)**0.5*abs(x[1] - 0.5)**0.5 + 1]] )
    return A


def feng3():
    A = 16/9*as_matrix( [[pow(x[0], 2/3), -pow(x[0], 1/3)*pow(x[1], 1/3)],
                        [-pow(x[0], 1/3)*pow(x[1], 1/3), pow(x[1], 2/3)]] )
    return A

def varying_coeff():
    A = as_matrix( [[ 1 + x[0]*x[1], 0], [0, 1 + x[0]*x[1] ]] )
    return A

#def advection2(): # atan not available in integrands
#    A = as_matrix( [[atan(1e-5*(x[0]**2 + x[1]**2) - 1) + 2, 0],
#                    [0, atan(1e-5*(x[0]**2 + x[1]**2) - 1) + 2]] )
#    return A

def pLaplace(space, exact, dirichletBC, solver, beta, parameters=None):
    #exact = as_vector( [x[0]*x[1]*(1.-x[0]**2)*(1.-x[1]**2)] )
    d = 0.001
    p = 1.7
    norm_gradu = pow(d + inner(grad(u), grad(u)), (p-2)/2)
    pLaplace_u = grad(norm_gradu*grad(u))[0, 0, 0] + grad(norm_gradu*grad(u))[0, 1, 1]
    a = (-inner(pLaplace_u, v[0])) * dx # + 10*inner(u, v) * ds
    b = ufl.replace(a, {u: exact} )
    scheme = create.scheme("nv", space, [a==b, dirichletBC], constraints='dirichlet', solver=solver, polOrder=space.order, parameters=parameters)
    return scheme

def pLaplace_var(space, exact, dirichletBC, solver, beta, parameters=None):
    #exact = as_vector( [x[0]*x[1]*(1.-x[0]**2)*(1.-x[1]**2)] )
    d = 0.001
    p = 1.7
    norm_gradu = pow(d + inner(grad(u), grad(u)), (p-2)/2)
    a = norm_gradu*inner(grad(u), grad(v))*dx# + inner(u, v)*dx# + 10*inner(u, v) * ds
    b = ufl.replace(a, {u: exact} )
    scheme = create.scheme("galerkin", space, [a==b, dirichletBC], solver=solver, parameters=parameters)
    #scheme = create.scheme("nv", space, [a==b, dirichletBC], constraints='dirichlet', solver=solver, parameters=parameters)
    return scheme

def simple(space, exact, dirichletBC, solver, beta, parameters=None):
    #exact = as_vector( [(1. - x[0]*x[0])*(1. - x[1]*x[1])] )
    laplace = grad(grad(u))[0, 0, 0] + grad(grad(u))[0, 1, 1]
    a = inner(sin(laplace) + 2*laplace, v[0])*dx
    b = ufl.replace(a, {u: ufl.as_vector(exact)} )
    scheme = create.scheme("nv", space, [a==b, dirichletBC], constraints='dirichlet', solver=solver, polOrder=space.order, parameters=parameters)
    return scheme

solutionList = [smooth_solution, rough_solution, exp_solution]
problemDict = {'advection': advection, 'advection2': advection2, 'fullHessian': full_hessian, 'feng3': feng3, 'laplace': laplace,
                'nonD': nonD, 'nonD1': nonD1, 'nonD2': nonD2, 'nonD3': nonD3, 'nonSmooth': non_smooth, 'varyingCoeff': varying_coeff}
nonlinDict = {'pLaplace': pLaplace, 'pLaplace_var': pLaplace_var, 'simple': simple}
