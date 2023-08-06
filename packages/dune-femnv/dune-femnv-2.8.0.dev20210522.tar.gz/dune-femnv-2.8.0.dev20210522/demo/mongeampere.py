from argparse import ArgumentParser
from dune.fem.function import integrate
from dune.grid import cartesianDomain
from math import sqrt
import scipy.sparse.linalg
import numpy as np
import dune.create as create
import time,sys

import ufl
from dune.ufl import DirichletBC, Space

from dune.fem import parameter
parameter.append({"fem.verboserank": 0, "fem.solver.verbose": 0,
    "fem.solver.errormeassure": "relative",
    "fem.preconditioning" : "true",
    "petsc.kspsolver.method": "gmres",
    "petsc.preconditioning.method": "hypre",
    "istl.preconditioning.method": "amg-jacobi",
    "istl.preconditioning.iterations": 0,
    "istl.preconditioning.relaxation": 0.9,
    "istl.gmres.restart": 50,
    "istl.preconditioning.fastilustorage": 1})
newtonParameter = {"linabstol": 1e-5, "reduction": 1e-5,
        "tolerance": 8e-10,
        "maxiterations": 100,
        "maxlineariterations": 1500,
        "lineSearch": "simple",
        "verbose": "true", "linear.verbose": "false"}
parameters={"fem.solver.newton." + k: v for k, v in newtonParameter.items()}
polorder = 2
#solver = "gmres"
solver = ("suitesparse","umfpack")

grid  = create.grid("ALUConform", cartesianDomain([0, 0], [1, 1], [4, 4]), dimgrid=2)
grid.hierarchicalGrid.globalRefine(1)
useDG = True
if useDG:
    space = create.space("dgonb", grid, dimrange=1, order=polorder, storage='fem')
    boundary = {"penalty":100} # better with 200?
else:
    space = create.space("Lagrange", grid, dimrange=1, order=polorder, storage='fem')
    boundary = {"constraints":"dirichlet"}
uh    = space.interpolate([0], name="solution")
uOld  = space.interpolate([0], name="old")

ufl_space = Space((grid.dimGrid, grid.dimWorld), 1)
u = ufl.TrialFunction(ufl_space)
v = ufl.TestFunction(ufl_space)
x = ufl.SpatialCoordinate(ufl_space.cell())
H = lambda u: ufl.grad(ufl.grad(u[0]))
#det = lambda H: H[0,0]*H[1,1] - 0.25*(H[0,1]+H[1,0])**2
detH = lambda u: ufl.det(H(u))
laplace = lambda u: ufl.grad(ufl.grad(u[0]))[0,0] + ufl.grad(ufl.grad(u[0]))[1,1]
problem = 1
if problem == 1:    # works
    exact = ufl.as_vector( [ufl.exp( 2.*((x[0]-0.5)**2+(x[1]-0.5)**2) ) ] )
    f = detH(exact)
elif problem == 2:  # works
    exact = ufl.as_vector( [ (x[0]-0.5)**4+(x[0]-0.5)**2+(x[1]-0.5)**4+(x[1]-0.5)**2 ] )
    f = detH(exact)
elif problem == 3:  # unclear...
    exact = ufl.as_vector( [ ufl.max_value( ((x[0]-0.5)**2+(x[1]-0.5)**2)/2.,0.08 ) ] )
    f = ufl.conditional((x[0]-0.5)**2+(x[1]-0.5)**2>0.16**2,1,0)
elif problem == 4:  # fails
    exact = ufl.as_vector( [-ufl.sqrt(2-x[0]**2-x[1]**2)] )
    f = detH(exact)
elif problem == 5:  # fails
    exact = ufl.as_vector( [1] )
    f = 1
elif problem == 6:  # works
    exact = ufl.as_vector( [abs(x[0])] )
    f = x[0]-x[0]

#####################################################
class ComputeH(object):
    def __init__(self, grid):
        self.space = create.space("dgonb", grid, dimrange=1, order=polorder, storage='fem')
        self.spc = create.space("product", [self.space]*4, components=["00","01","10","11"] )
        self.A = [ H(u)[0,0]*v[0]*ufl.dx, H(u)[0,1]*v[0]*ufl.dx,\
                   H(u)[1,0]*v[0]*ufl.dx, H(u)[1,1]*v[0]*ufl.dx ]
        self.scheme = [ create.scheme("nv", self.space, a==0, solver=solver,\
                penalty=0, polOrder=self.space.order) for a in self.A]
        # self.scheme = [ create.scheme("galerkin", self.space, a==0, solver=solver) for a in self.A]
        self.a = u[0]*v[0]*ufl.dx
        self.modelM  = create.model("integrands", grid, self.a == 0)
        self.schemeM = create.scheme("galerkin", self.space, self.modelM, solver=solver)
        self.H = self.spc.interpolate([0,0,0,0],name="H")
        self.rhs = self.space.interpolate([0],name="rhs")
    def setup(self, uh):
        for h, s in zip(self.H.components, self.scheme):
            s(uh, self.rhs)
            h.clear()
            self.schemeM.solve(rhs=self.rhs, target=h)
    def __call__(self, i, j):
        return 0.5*(self.H[i*2 + j]+self.H[j*2 + i])
#####################################################

def compute():
    a  = (detH(u)-f)*v[0]*ufl.dx
    dirichletBC = DirichletBC(ufl_space, exact, 1)
    scheme = create.scheme("nv", space, [a==0,dirichletBC],
               solver=solver, polOrder=space.order,
               **boundary,
               parameters=parameters)

    # for initial guess
    a = laplace(u) * v[0] * ufl.dx
    a -= ufl.sqrt(laplace(uOld)**2+2*(f-detH(uOld)))*v[0]*ufl.dx
    scheme0 = create.scheme("nv", space, [a==0,dirichletBC],
                solver=solver, polOrder=space.order,
                **boundary,
                parameters=parameters)

    # for Newton solver
    Huh = ComputeH(grid)
    dirichletBC0 = DirichletBC(ufl_space, ufl.as_vector([0]), 1)
    C = ufl.as_matrix( [[Huh(1,1), -Huh(1,0)], [-Huh(0,1), Huh(0,0)]] )
    a = ufl.inner(C, H(u))*v[0]*ufl.dx
    schemeC = create.scheme("nv", space, [a==0, dirichletBC0],
            solver=solver, polOrder=space.order,
            **boundary,
            parameters=parameters)

    for eoc_loop in range(5):
        print("#### START", flush=True)
        uh.clear()
        uOld.clear()
        if True:
            if not useDG:
                bnd = uh.copy("bnd")
                bnd.clear()
                scheme.constraint(bnd)
            res = uh.copy('residual')
            n = 0
            while True:
                scheme0.solve(target=uh)
                scheme(uh,res)
                if not useDG:
                    res.as_numpy[:] -= bnd.as_numpy[:]
                absF   = np.dot(res.as_numpy,res.as_numpy)
                absRes = integrate(grid, res[0]**2, order=5)[0]
                diff   = integrate(grid, (uOld[0]-uh[0])**2,order=5)[0]
                error  = integrate(grid, (exact[0]-uh[0])**2,order=5)[0]
                uOld.assign(uh)
                n += 1
                print("iterate:",n,absF,absRes,diff,"   ",error,flush=True)
                if diff < 1e-14:
                    break
        ###############################################
        if False:
            scheme0.solve(target=uh)
            # uh.interpolate(exact)
            uOld.assign(uh)
            scheme.solve(target=uh)
        if False:
            scheme0.solve(target=uh)
            uOld.assign(uh)
            if not useDG:
                bnd = uh.copy("bnd")
                bnd.clear()
                scheme.constraint(bnd)
            res = uh.copy('residual')
            n = 0
            while True:
                res.clear()
                scheme(uh, res)                     # Au-b, u
                if not useDG:
                    res.as_numpy[:] -= bnd.as_numpy[:]  # Au-b, 0
                absF = sqrt( np.dot(res.as_numpy,res.as_numpy) )
                absRes = integrate(grid, res[0]**2, order=5)[0]
                if n == 50 or absF < 1e-8:
                    break
                Huh.setup(uh)
                S  = schemeC.assemble(uh).to_numpt
                uh.as_numpy -= scipy.sparse.linalg.spsolve(S, res.as_numpy[:])
                      # u - A^{-1}(Au-b), u-0 = u-u+b, u
                n += 1
                diff = integrate(grid, (uOld[0]-uh[0])**2,order=5)[0]
                error = integrate(grid, (exact[0]-uh[0])**2,order=5)[0]
                uOld.assign(uh)
                print("iterate:",n,absF,absRes,diff,"   ",error,flush=True)
                grid.writeVTK('paraview/mongeampere_newton',
                        pointdata={'solution':uh,'res':res,
                            'H00':Huh(0,0),'H01':Huh(0,1),'H11':Huh(1,1)},
                        number=n)
        print("#### END", flush=True)
        grid.writeVTK('paraview/mongeampere',
                pointdata={'solution':uh,'difference':uh-exact,
                    'initial':uOld, 'initialDiff':uOld-exact,
                    'Hdiff':detH(uh-exact) },
                number=eoc_loop)
        print( 'l2 error:', integrate(grid, (uh[0]-exact[0])**2,order=5)[0],
               'h1 error:', integrate(grid, ufl.inner(ufl.grad(exact[0]-uh[0]), ufl.grad(exact[0]-uh[0])), 5)[0] )
        grid.hierarchicalGrid.globalRefine(1)

compute()
