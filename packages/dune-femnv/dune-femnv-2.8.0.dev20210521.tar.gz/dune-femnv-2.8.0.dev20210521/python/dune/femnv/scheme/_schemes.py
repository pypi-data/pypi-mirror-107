from dune.fem.scheme import getSolver, femschemeModule
# from dune.fem.scheme import module

from ufl.equation import Equation

def nv(space, model, penalty=None, polOrder=2, solver=None, constraints=None, **kwargs):
    """create a scheme for solving non variational second order pdes with discontinuous finite element

    Args:

    Returns:
        Scheme: the constructed scheme
    """

    modelParam = None
    if isinstance(model, (list, tuple)):
        modelParam = model[1:]
        model = model[0]
    if isinstance(model,Equation):
        from dune.femnv.model import nvelliptic
        if modelParam:
            model = nvelliptic(space.grid, model, *modelParam)
        else:
            model = nvelliptic(space.grid, model)

    includes = ["dune/femnv/schemes/nvdgelliptic.hh"]
    storageStr, dfIncludes, dfTypeName, linearOperatorType, defaultSolver,_ = space.storage
    _, solverIncludes, solverTypeName,_ = getSolver(solver,space.storage,defaultSolver)
    includes += ["dune/fem/schemes/femscheme.hh"] +\
                space._includes + dfIncludes + solverIncludes +\
                ["dune/femnv/schemes/diffusionmodel.hh", "dune/fempy/parameter.hh"] +\
                ["dune/fem/schemes/dirichletwrapper.hh"]

    op = lambda linOp, model: "DifferentiableNVDGEllipticOperator< " +\
                              ",".join([linOp, model]) + ", " +\
                              str(polOrder) + ">"
    if model.hasDirichletBoundary and constraints=="dirichlet":
        operator = lambda linOp,model: "DirichletWrapperOperator< " + op(linOp,model) + " >"
    else:
        operator = op

    ###

    if constraints=="dirichlet":
        if penalty is None:
            penalty = 0
        else:
            raise KeyError("dirichlet constraints can not be used together with penalty terms")
    else:
        if penalty is None:
            raise KeyError("either use dirichlet constraints or set a value for the penalty (can be zero)")

    try:
        param = kwargs["parameters"]
        param["penalty"] = param.get("penalty",penalty)
    except:
        kwargs["parameters"] = {}
        kwargs["parameters"]["penalty"] = penalty

    spaceType = space._typeName
    modelType = "NVDiffusionModel< " +\
          "typename " + spaceType + "::GridPartType, " +\
          spaceType + "::dimRange, " +\
          spaceType + "::dimRange, " +\
          "typename " + spaceType + "::RangeFieldType >"
    # operatorType = operator(linearOperatorType, modelType)
    # typeName = "FemScheme< " + operatorType + ", " + solverTypeName + " >"

    # should use this somehow
    return femschemeModule(space,model,includes,solver,operator,
            parameters = kwargs["parameters"],
            modelType = modelType)
    # return module(includes, typeName).Scheme(space, model ,**kwargs)
