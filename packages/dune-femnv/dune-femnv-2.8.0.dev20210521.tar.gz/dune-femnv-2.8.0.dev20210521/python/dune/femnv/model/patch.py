from __future__ import division, print_function, unicode_literals

from dune.source.builtin import get, make_shared
from dune.source.cplusplus import UnformattedExpression
from dune.source.cplusplus import AccessModifier, Constructor, Declaration, Function, Method, NameSpace, Struct, TypeAlias, UnformattedBlock, Variable
from dune.source.cplusplus import assign, construct, dereference, nullptr, return_, this
from dune.source.cplusplus import SourceWriter
from dune.source.fem import declareFunctionSpace

def codeNV(self, name='Model', targs=[]):
    constants_ = Variable('std::tuple< ' + ', '.join('std::shared_ptr< ' + c  + ' >' for c in self._constants) + ' >', 'constants_')
    # coefficients_ = Variable('std::tuple< ' + ', '.join(c['name'] if c['name'] is not None else 'Coefficient' + str(i) for i, c in enumerate(self._coefficients)) + ' >', 'coefficients_')
    coefficients_ = Variable('std::tuple< ' + ', '.join(self.cppTypeIdentifier(c['name'],"coefficient",i) for i, c in enumerate(self._coefficients)) + ' >', 'coefficients_')

    entity_ = Variable('const EntityType *', 'entity_')

    # code = Struct(name, targs=(['class GridPart'] + ['class ' + c['name'] if c['name'] is not None else 'class Coefficient' + str(i) for i, c in enumerate(self._coefficients)] + targs))
    code = Struct(name, targs=(['class GridPart'] + ['class ' + self.cppTypeIdentifier(c['name'],"coefficient",i) for i, c in enumerate(self._coefficients)] + targs))

    code.append(TypeAlias("GridPartType", "GridPart"))
    code.append(TypeAlias("EntityType", "typename GridPart::template Codim< 0 >::EntityType"))
    code.append(TypeAlias("IntersectionType", "typename GridPart::IntersectionType"))

    # code.append(declareFunctionSpace("typename GridPartType::ctype", SourceWriter.cpp_fields(self.field), UnformattedExpression("int", "GridPartType::dimensionworld"), self.dimRange))
    code.append(declareFunctionSpace("typename GridPartType::ctype", SourceWriter.cpp_fields(self.field), UnformattedExpression("int", "GridPartType::dimensionworld"), self.dimDomain,
        name="DFunctionSpaceType",prefix="D",
        dimDomainName="dimDomain", dimRangeName="dimD"
        ))
    code.append(declareFunctionSpace("typename GridPartType::ctype", SourceWriter.cpp_fields(self.field), UnformattedExpression("int", "GridPartType::dimensionworld"), self.dimRange,
        name="RFunctionSpaceType",prefix="R",
        dimDomainName=None, dimRangeName="dimR"
        ))
    code.append(Declaration(Variable("const int", "dimLocal"), initializer=UnformattedExpression("int", "GridPartType::dimension"), static=True))

    if self.hasConstants:
        code.append(TypeAlias("ConstantType", "typename std::tuple_element_t< i, " + constants_.cppType + " >::element_type", targs=["std::size_t i"]))
        code.append(Declaration(Variable("const std::size_t", "numConstants"), initializer=len(self._constants), static=True))

    if self.hasCoefficients:
        #coefficientSpaces = ["Dune::Fem::FunctionSpace< DomainFieldType, " + SourceWriter.cpp_fields(c['field']) + ", dimDomain, " + str(c['dimRange']) + " >" for c in self._coefficients]
        code.append(TypeAlias('CoefficientType', 'std::tuple_element_t< i, ' + coefficients_.cppType + ' >', targs=['std::size_t i']))
        coefficientSpaces = ["typename CoefficientType<"+str(i)+">::FunctionSpaceType" for i,c in enumerate(self._coefficients)]
        code.append(TypeAlias("CoefficientFunctionSpaceTupleType", "std::tuple< " + ", ".join(coefficientSpaces) + " >"))

    arg_param = Variable("const Dune::Fem::ParameterReader &", "parameter")
    args = [Declaration(arg_param, initializer=UnformattedExpression('const ParameterReader &', 'Dune::Fem::Parameter::container()'))]
    init = None
    if self.hasCoefficients:
        # args = [Variable("const Coefficient" + str(i) + " &", "coefficient" + str(i)) for i, c in enumerate(self._coefficients)] + args
        # args = [Variable("const " + c['name'] if c['name'] is not None else "const Coefficient" + str(i) + " &", "coefficient" + str(i)) for i, c in enumerate(self._coefficients)] + args
        args = [Variable("const " + self.cppTypeIdentifier(c['name'],"coefficient",i) + " &", "coefficient" + str(i)) for i, c in enumerate(self._coefficients)] + args

        init = ["coefficients_( " + ", ".join("coefficient" + str(i) for i, c in enumerate(self._coefficients)) + " )"]
    constructor = Constructor(args=args, init=init)
    constructor.append([assign(get(str(i))(constants_), make_shared(c)()) for i, c in enumerate(self._constants)])
    for name, idx in self._parameterNames.items():
        constructor.append(assign(dereference(get(idx)(constants_)), UnformattedExpression("auto", arg_param.name + '.getValue< ' + self._constants[idx] + ' >( "' + name + '" )', uses=[arg_param])))
    code.append(constructor)

    init = ['entity_ = &entity;']
    init += ['std::get< ' + str(i) + ' >( ' + coefficients_.name + ' ).init( entity );' for i, c in enumerate(self._coefficients)]
    init = [UnformattedBlock(init)] + self.init + [return_(True)]
    code.append(Method('bool', 'init', args=['const EntityType &entity'], code=init, const=True))

    code.append(Method('const EntityType &', 'entity', code=return_(dereference(entity_)), const=True))
    code.append(Method('std::string', 'name', const=True, code=return_(UnformattedExpression('const char *', '"' + name + '"'))))

    code.append(TypeAlias("BoundaryIdProviderType", "Dune::Fem::BoundaryIdProvider< typename GridPartType::GridType >"))
    code.append(Declaration(Variable("const bool", "symmetric"), initializer=self.symmetric, static=True))

    code.append(Method('void', 'source', targs=['class Point'], args=[self.arg_x, self.arg_u, self.arg_du, self.arg_d2u, self.arg_r], code=self.source, const=True))
    code.append(Method('void', 'linSource', targs=['class Point'], args=[self.arg_ubar, self.arg_dubar, self.arg_d2ubar, self.arg_x, self.arg_u, self.arg_du, self.arg_d2u, self.arg_r], code=self.linSource, const=True))

    code.append(Method('void', 'diffusiveFlux', targs=['class Point'], args=[self.arg_x, self.arg_u, self.arg_du, self.arg_dr], code=self.diffusiveFlux, const=True))
    code.append(Method('void', 'linDiffusiveFlux', targs=['class Point'], args=[self.arg_ubar, self.arg_dubar, self.arg_x, self.arg_u, self.arg_du, self.arg_dr], code=self.linDiffusiveFlux, const=True))

    code.append(Method('void', 'fluxDivergence', targs=['class Point'], args=[self.arg_x, self.arg_u, self.arg_du, self.arg_d2u, self.arg_r], code=self.fluxDivergence, const=True))

    code.append(Method('void', 'alpha', targs=['class Point'], args=[self.arg_x, self.arg_u, self.arg_r], code=self.alpha, const=True))
    code.append(Method('void', 'linAlpha', targs=['class Point'], args=[self.arg_ubar, self.arg_x, self.arg_u, self.arg_r], code=self.linAlpha, const=True))

    code.append(Method('bool', 'hasNeumanBoundary', const=True, code=return_(self.hasNeumanBoundary)))
    code.append(Method('bool', 'hasDirichletBoundary', const=True, code=return_(self.hasDirichletBoundary)))
    code.append(Method('bool', 'isDirichletIntersection', args=[self.arg_i, 'Dune::FieldVector< int, dimR > &dirichletComponent'], code=self.isDirichletIntersection, const=True))
    code.append(Method('void', 'dirichlet', targs=['class Point'], args=[self.arg_bndId, self.arg_x, self.arg_r], code=self.dirichlet, const=True))

    if self.hasConstants:
        code.append(Method("const ConstantType< i > &", "constant", targs=["std::size_t i"], code=return_(dereference(get("i")(constants_))), const=True))
        code.append(Method("ConstantType< i > &", "constant", targs=["std::size_t i"], code=return_(dereference(get("i")(constants_)))))

    if self.hasCoefficients:
        code.append(Method("const CoefficientType< i > &", "coefficient", targs=["std::size_t i"], code=return_(get("i")(coefficients_)), const=True))
        code.append(Method("CoefficientType< i > &", "coefficient", targs=["std::size_t i"], code=return_(get("i")(coefficients_))))

    code.append(AccessModifier("private"))
    code.append(Declaration(entity_, nullptr, mutable=True))
    if self.hasConstants:
        code.append(Declaration(constants_, mutable=True))
    if self.hasCoefficients:
        code.append(Declaration(coefficients_, mutable=True))
    return code

def transform(Class):
    Class.code = codeNV
    Class.signature += 'nv'
