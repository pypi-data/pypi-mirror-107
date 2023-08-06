from argparse import ArgumentParser
from dune.fem.function import integrate
from dune.grid import cartesianDomain
from math import sqrt
from norms import compute_norms
from numpy import dot
import dune.create as create
import time

import ufl
from dune.ufl import Space

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
        "tolerance": 8e-5,
        "maxiterations": 20,
        "maxlineariterations": 1500,
        "verbose": "true", "linear.verbose": "false"}
parameters={"fem.solver.newton." + k: v for k, v in newtonParameter.items()}

# solver = "gmres"
solver = ("suitesparse","umfpack")

ufl_space = Space((2,2), 1)
u = ufl.TrialFunction(ufl_space)
v = ufl.TestFunction(ufl_space)
x = ufl.SpatialCoordinate(ufl_space.cell())
D = lambda u: ufl.grad(ufl.grad(u[0]))

class ComputeH(object):
    def __init__(self,grid):
        self.space = create.space("dgonb", grid, dimrange=1, order=2, storage='fem')
        self.spc = create.space("product", [self.space]*4, components=["00","01","10","11"] )
        self.A = [ D(u)[0,0]*v[0]*ufl.dx, D(u)[0,1]*v[0]*ufl.dx,\
                   D(u)[1,0]*v[0]*ufl.dx, D(u)[1,1]*v[0]*ufl.dx ]
        self.scheme = [ create.scheme("nvdg", self.space, a==0, solver=solver,\
                penalty=0, polOrder=self.space.order) for a in self.A]
        self.a = u[0]*v[0]*ufl.dx
        self.modelM  = create.model("integrands", grid, self.a == 0)
        self.schemeM = create.scheme("galerkin", self.space, self.modelM, solver=solver)
        self.H = self.spc.interpolate([0,0,0,0],name="H")
        self.rhs = self.space.interpolate([0],name="rhs")
    def setup(self, uh):
        for h,s in zip(self.H.components,self.scheme):
            s(uh, self.rhs)
            h.clear()
            self.schemeM.solve(rhs=self.rhs, target=h)
    def __call__(self,i,j):
        return self.H[i*2+j]

# monge ampere equation
exact = ufl.as_vector( [x[0]**4*ufl.exp( 2.*((x[0]-0.5)**2+(x[1]-0.5)**2) ) ] )
# exact = ufl.as_vector( [((x[0]-0.5)**4+(x[1]-0.5)**4) ] )

# Either provide a linear model NLmodel : u -> a*H[0][0]+b*H[1][0]+c*H[0][1]+d*H[1][1]
# or two models (one linear one non linear) so that
# NL(u) = DL(u)u (where DL(u) is the linearization around u
# 1) compute L^2 projection of 'exact'      -> u_h
# 2) solve u*v*dx = nvOp(u_h)               -> H
# 3) assemble nvOp and solve u*v*dx = Au_h  -> MH
# 4) compare L^2 difference between
#    a) NLmodel(u_h) and NLmodel(exact)
#    b) H and NLmodel(exact)
#    c) MH and NLmodel(exact)
# Note: due to the linearity of the model we should have H=MH
def test(model,i=None,j=None):
    grid  = create.grid("ALUSimplex", cartesianDomain([0, 0], [1, 1], [10, 10]), dimgrid=2)
    space = create.space("Lagrange", grid, dimrange=1, order=2, storage='fem')
    uh    = space.interpolate([0], name="solution")

    NLmodel,Lmodel,init = model(grid)

    A        = NLmodel(u)*v[0]*ufl.dx
    schemeNL = create.scheme("nvdg", space, A==0, solver=solver, penalty=0, parameters=parameters, polOrder=space.order)
    if Lmodel is None:
        schemeL = schemeNL
    else:
        A       = Lmodel(u)*v[0]*ufl.dx
        schemeL = create.scheme("nvdg", space, A==0, solver=solver, penalty=0, parameters=parameters, polOrder=space.order)

    # for initial projection (L^2 projection)
    a  = u[0]*v[0]*ufl.dx
    a -= exact[0]*v[0]*ufl.dx
    model0  = create.model("elliptic", grid, a == 0)
    scheme0 = create.scheme("h1", space, model0, solver=solver,
             parameters=parameters)

    # to compute finite element hessian
    a = u[0]*v[0]*ufl.dx
    modelM  = create.model("elliptic", grid, a == 0)
    schemeM = create.scheme("h1", space, modelM, solver=solver,
             parameters=parameters)

    rhs = uh.copy()
    H   = uh.copy()
    MH  = uh.copy()

    Huh = ComputeH(grid)

    print("Hu_h-Hexact","H-Hexact","MH-Hexact","    # output",flush=True)
    for eoc_loop in range(4):
        uh.clear()
        scheme0.solve(target=uh)

        rhs.clear()
        schemeNL(uh,rhs)
        H.clear()
        schemeM.solve(rhs=rhs,target=H)

        rhs.clear()
        if init is not None:
            init(uh)
        M = schemeL.assemble(uh).as_numpy
        rhs.as_numpy[:] = M.dot(uh.as_numpy[:])
        MH.clear()
        schemeM.solve(rhs=rhs,target=MH)

        grid.writeVTK('paraview/mongeampere',
                pointdata={'solution':uh,'difference':uh-exact,
                    'detD2u':NLmodel(uh), 'detD2U':NLmodel(exact),
                    'detH':H, 'detH_M':MH},
                number=eoc_loop)
        error = [integrate(grid,(NLmodel(uh)-NLmodel(exact))**2,order=5)[0],
                 integrate(grid,(H[0]-NLmodel(exact))**2,order=5)[0],
                 integrate(grid,(MH[0]-NLmodel(exact))**2,order=5)[0]]
        print(grid.size(0),error,"   # output", flush=True)

        if i is not None and j is not None:
            Huh.setup(uh)
            error = integrate(grid,(Huh(i,j)-NLmodel(exact))**2,order=5)[0]
            print("testing ",i,j,error,"    # output", flush=True)

        grid.hierarchicalGrid.globalRefine(1)

# linear example
def H(i,j):
    def H_(grid):
        print("i=",i,"j=",j,"    # output",flush=True)
        return lambda u: D(u)[i,j],\
               None,None
    return H_
# Monge-Ampere example - note:
#    NL(u) = H00*H11 - H01*H01
# and taking L(u) = 1/2 NL(u)
#    DL(baru):H[u] = 1/2 [[barH11 -barH10],[-barH01 barH00]] : D^2u
#                  = 1/2 ( barH11*H00-barH10*H01-barH01*H10+barH00*H11)
# so
#    DL(u):H[u]    = NL(u)
# as required
def MAD(grid):
    print("MAD:    # output",flush=True)
    return lambda u: ufl.det(D(u)),\
           lambda u: ufl.det(D(u)) / 2.,\
           None

def MAD2(grid):
    print("MAD:    # output",flush=True)
    Huh = ComputeH(grid)
    C = ufl.as_matrix( [[Huh(1,1), -Huh(1,0)], [-Huh(0,1), Huh(0,0)]] )
    return lambda u: ufl.det(D(u)),\
           lambda u: ufl.inner(C, D(u))/2.,\
           lambda uh: Huh.setup(uh)


test(H(0,0),0,0)
test(H(0,1),0,1)
test(H(1,0),1,0)
test(H(1,1),1,1)

test(MAD)
test(MAD2)
