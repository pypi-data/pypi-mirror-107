from argparse import ArgumentParser
from dune.grid import cartesianDomain
from math import sqrt
from norms import compute_norms
from numpy import dot
import dune.create as create
import os.path,sys
import pickle
import time

parser = ArgumentParser()
parser.add_argument('problem', type=str, help='laplace, fullHessian, varyingCoeff, advection, nonD, nonD2, nonSmooth')
parser.add_argument('scheme', type=str, help='nvdg, h1H, h1D2, l2H, l2D2, mu, feng, var')
parser.add_argument('--sol', type=int, nargs='?', default=0, help='0=smooth, 1=rough, 2=exp')
parser.add_argument("-b", "--bicgstab", action="store_true", help="use bicgstab solver")
parser.add_argument("-c", "--cg", action="store_true", help="use cg solver")
parser.parse_args()
try:
    args = parser.parse_args()
except SystemExit:
    sys.exit(0)
problemName = args.problem
schemeName = args.scheme
solutionName = args.sol
if args.bicgstab:
    use_cg = False
else:
    use_cg = True

polOrder = 2
grid = create.grid("ALUSimplex", cartesianDomain([0, 0], [1, 1], [4, 4]))
space = create.space("Lagrange", grid, dimrange=1, order=polOrder, storage='fem')
uh = space.interpolate([0], name="solution")

from problems import problemDict, solutionList
A = problemDict[problemName]()
exact, dirichletBC = solutionList[solutionName]()

# penalty calculation
if problemName == "advection2":
    max_eval = 4
elif problemName == "nonD":
    max_eval = 2
else:
    max_eval = 1
beta = polOrder*(polOrder + 1)*max_eval

from schemes import schemeDict, solve
scheme = schemeDict[schemeName](A, exact, dirichletBC, space, beta=beta)

for eoc_loop in range(3):
    start_time = time.time()
    print("#### START")
    uh.clear()
    # solver = "fem"
    # uh, info = scheme.solve(target=uh)
    uh, info, solver = solve( scheme, uh, A, exact, dirichletBC, version=schemeName, use_cg=use_cg, beta=beta)
    print("#### END", info)
    total_time = time.time() - start_time
    errors = compute_norms(grid, uh - exact, A)
    if eoc_loop == 0:
        if polOrder == 2:
            file_path = 'pickle/' + problemName + '_' + schemeName + '_' + solver + '.p'
        else:
            file_path = 'pickle' + str(polOrder) + '/' + problemName + '_' + schemeName + '_' + solver + '.p'
        file = open(file_path, 'wb')
    pickle.dump([grid.size(0), errors, info['linear_iterations'], total_time], file)
    grid.writeVTK('paraview/' + problemName + '_' + schemeName + '_', pointdata=[uh], number=eoc_loop)
    grid.hierarchicalGrid.globalRefine(1)
file.close()

import results
if polOrder == 2:
    results.wp()
else:
    results.wp(polOrder=str(polOrder))

if False:
    nvdg = schemeDict["nvdg"]( A, exact, dirichletBC, space,
            parameters={"fem.solver.newton." + k: v for k, v in newtonParameter.items()})
    var  = schemeDict["var"]( A, exact, dirichletBC, space,
            parameters={"fem.solver.newton." + k: v for k, v in newtonParameter.items()})
    nvdg_A = nvdg.assemble(uh).as_numpy
    var_A  = var.assemble(uh).as_numpy
    matrix = (nvdg_A-var_A).todense()
    print(matrix)
    sys.exit(0)

