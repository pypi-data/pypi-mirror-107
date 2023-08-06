/**************************************************************************

  The dune-fem module is a module of DUNE (see www.dune-project.org).
  It is based on the dune-grid interface library
  extending the grid interface by a number of discretization algorithms
  for solving non-linear systems of partial differential equations.

  Copyright (C) 2003 - 2015 Robert Kloefkorn
  Copyright (C) 2003 - 2010 Mario Ohlberger
  Copyright (C) 2004 - 2015 Andreas Dedner
  Copyright (C) 2005        Adrian Burri
  Copyright (C) 2005 - 2015 Mirko Kraenkel
  Copyright (C) 2006 - 2015 Christoph Gersbacher
  Copyright (C) 2006 - 2015 Martin Nolte
  Copyright (C) 2011 - 2015 Tobias Malkmus
  Copyright (C) 2012 - 2015 Stefan Girke
  Copyright (C) 2013 - 2015 Claus-Justus Heine
  Copyright (C) 2013 - 2014 Janick Gerstenberger
  Copyright (C) 2013        Sven Kaulman
  Copyright (C) 2013        Tom Ranner
  Copyright (C) 2015        Marco Agnese
  Copyright (C) 2015        Martin Alkaemper


  The dune-fem module is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License as
  published by the Free Software Foundation; either version 2 of
  the License, or (at your option) any later version.

  The dune-fem module is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

**************************************************************************/
#ifndef NVDGELLIPTIC_HH

#define NVDGELLIPTIC_HH

#include <dune/common/fmatrix.hh>

#include <dune/fem/misc/compatibility.hh>
#include <dune/fem/operator/common/differentiableoperator.hh>
#include <dune/fem/operator/common/operator.hh>
#include <dune/fem/operator/common/stencil.hh>
#include <dune/fem/quadrature/cachingquadrature.hh>
#include <dune/fem/schemes/elliptic.hh>
#include <dune/fem/space/discontinuousgalerkin.hh>
#include <dune/fem/space/lagrange/space.hh>
#include <dune/fem/operator/1order/localmassmatrix.hh>
#include <dune/fem/operator/common/temporarylocalmatrix.hh>
#include <dune/fem/function/localfunction/temporary.hh>
// include parameter handling
#include <dune/fem/io/parameter.hh>
#include <dune/fem/io/file/dataoutput.hh>
// include capabilities
//#include "capabilities.hh"


// EllipticOperator
// ----------------

template< class DiscreteFunction, class Model, int polOrder=2>
struct NVDGEllipticOperator
: public virtual Dune::Fem::Operator< DiscreteFunction >
{
  typedef DiscreteFunction DomainFunctionType;
  typedef DiscreteFunction  RangeFunctionType;
  typedef Model                  ModelType;
  typedef Model                  DirichletModelType;

  typedef typename DomainFunctionType::DiscreteFunctionSpaceType DomainDiscreteFunctionSpaceType;
  typedef typename DomainFunctionType::LocalFunctionType         DomainLocalFunctionType;
  typedef typename DomainLocalFunctionType::RangeType                    DomainRangeType;
  typedef typename DomainLocalFunctionType::JacobianRangeType            DomainJacobianRangeType;
  typedef typename DomainLocalFunctionType::HessianRangeType            DomainHessianRangeType;
  typedef typename RangeFunctionType::DiscreteFunctionSpaceType RangeDiscreteFunctionSpaceType;
  typedef typename RangeFunctionType::LocalFunctionType         RangeLocalFunctionType;
  typedef typename RangeLocalFunctionType::RangeType                    RangeRangeType;
  typedef typename RangeLocalFunctionType::JacobianRangeType            RangeJacobianRangeType;
  typedef typename RangeLocalFunctionType::HessianRangeType            RangeHessianRangeType;

  typedef typename RangeLocalFunctionType::RangeFieldType RangeFieldType;

  // the following types must be identical for domain and range
  typedef typename RangeDiscreteFunctionSpaceType::IteratorType IteratorType;
  typedef typename IteratorType::Entity       EntityType;
  typedef typename EntityType::Geometry       GeometryType;
  typedef typename RangeDiscreteFunctionSpaceType::DomainType DomainType;
  typedef typename RangeDiscreteFunctionSpaceType::GridPartType  GridPartType;
  typedef typename GridPartType::IntersectionIteratorType IntersectionIteratorType;
  typedef typename IntersectionIteratorType::Intersection IntersectionType;

  typedef Dune::Fem::CachingQuadrature< GridPartType, 0 > QuadratureType;
  typedef Dune::Fem::CachingQuadrature< GridPartType, 1 > FaceQuadratureType;

  static const int dimDomain = RangeLocalFunctionType::dimDomain;
  static const int dimRange = RangeLocalFunctionType::dimRange;

  //! constructor
  NVDGEllipticOperator ( const RangeDiscreteFunctionSpaceType &space,
                         ModelType &model,
                         const Dune::Fem::ParameterReader &parameter = Dune::Fem::Parameter::container() )
  : NVDGEllipticOperator(space,space,model,parameter) {}
  NVDGEllipticOperator ( const DomainDiscreteFunctionSpaceType &dSpace,
                         const RangeDiscreteFunctionSpaceType &rSpace,
                         ModelType &model,
                         const Dune::Fem::ParameterReader &parameter = Dune::Fem::Parameter::container() )
  : model_( model ),
    penalty_( parameter.getValue< double >( "penalty" ) ),
    dSpace_(dSpace), rSpace_(rSpace)
  {
    std::cout << "NVDG using penalty=" << penalty_ << std::endl;
  }

  //! application operator
  virtual void operator() ( const DomainFunctionType &u, RangeFunctionType &w ) const
  { apply(u,w); }
  template <class GF>
  void apply( const GF &u, RangeFunctionType &w ) const;

  const ModelType &model () const { return model_; }
  ModelType &model () { return model_; }
  double penalty() const { return penalty_; }

  const DomainDiscreteFunctionSpaceType& domainSpace() const
  {
    return dSpace_;
  }
  const RangeDiscreteFunctionSpaceType& rangeSpace() const
  {
    return rSpace_;
  }
private:
  ModelType &model_;
  double penalty_;
  const DomainDiscreteFunctionSpaceType &dSpace_;
  const RangeDiscreteFunctionSpaceType &rSpace_;
};

// DifferentiableNVDGEllipticOperator
// ------------------------------

template< class JacobianOperator, class Model, int polOrder=2>
struct DifferentiableNVDGEllipticOperator
: public NVDGEllipticOperator< typename JacobianOperator::DomainFunctionType, Model, polOrder >,
  public Dune::Fem::DifferentiableOperator< JacobianOperator >
{
  typedef NVDGEllipticOperator< typename JacobianOperator::DomainFunctionType, Model, polOrder > BaseType;

  typedef JacobianOperator JacobianOperatorType;

  typedef typename BaseType::ModelType ModelType;
  typedef typename BaseType::DomainFunctionType DomainFunctionType;
  typedef typename BaseType::RangeFunctionType RangeFunctionType;

  typedef typename DomainFunctionType::DiscreteFunctionSpaceType DomainDiscreteFunctionSpaceType;
  typedef typename DomainFunctionType::LocalFunctionType         DomainLocalFunctionType;
  typedef typename DomainLocalFunctionType::RangeType                    DomainRangeType;
  typedef typename DomainLocalFunctionType::JacobianRangeType            DomainJacobianRangeType;
  typedef typename RangeFunctionType::DiscreteFunctionSpaceType RangeDiscreteFunctionSpaceType;
  typedef typename RangeFunctionType::LocalFunctionType         RangeLocalFunctionType;
  typedef typename RangeLocalFunctionType::RangeType                    RangeRangeType;
  typedef typename RangeLocalFunctionType::JacobianRangeType            RangeJacobianRangeType;

  typedef typename DomainFunctionType::DiscreteFunctionSpaceType DiscreteFunctionSpaceType;
  typedef typename DomainFunctionType::LocalFunctionType LocalFunctionType;
  typedef typename LocalFunctionType::RangeType RangeType;
  typedef typename LocalFunctionType::RangeFieldType RangeFieldType;
  typedef typename LocalFunctionType::JacobianRangeType JacobianRangeType;
  typedef typename LocalFunctionType::HessianRangeType HessianRangeType;

  typedef typename DiscreteFunctionSpaceType::IteratorType IteratorType;
  typedef typename IteratorType::Entity       EntityType;
  typedef typename EntityType::Geometry       GeometryType;

  typedef typename DiscreteFunctionSpaceType::DomainType DomainType;

  typedef typename DiscreteFunctionSpaceType::GridPartType GridPartType;
  typedef typename GridPartType::IntersectionIteratorType IntersectionIteratorType;
  typedef typename IntersectionIteratorType::Intersection IntersectionType;
  typedef typename IntersectionType::Geometry  IntersectionGeometryType;

  typedef Dune::Fem::ElementQuadrature< GridPartType, 1 > FaceQuadratureType;
  typedef Dune::Fem::CachingQuadrature< GridPartType, 0 > QuadratureType;

  static const int dimDomain = LocalFunctionType::dimDomain;
  static const int dimRange = LocalFunctionType::dimRange;

public:
  //! constructor
  DifferentiableNVDGEllipticOperator ( const DiscreteFunctionSpaceType &space,
                         ModelType &model,
                         const Dune::Fem::ParameterReader &parameter = Dune::Fem::Parameter::container() )
  : BaseType( space, model, parameter )
  {}
  DifferentiableNVDGEllipticOperator ( const DiscreteFunctionSpaceType &dSpace,
                                       const DiscreteFunctionSpaceType &rSpace,
                         ModelType &model,
                         const Dune::Fem::ParameterReader &parameter = Dune::Fem::Parameter::container() )
  : BaseType( dSpace, rSpace, model, parameter )
  {}

  //! method to setup the jacobian of the operator for storage in a matrix
  void jacobian ( const DomainFunctionType &u, JacobianOperatorType &jOp ) const
  { apply(u,jOp); }
  void apply ( const DomainFunctionType &u, JacobianOperatorType &jOp ) const;
  using BaseType::apply;

  using BaseType::model;
  using BaseType::penalty;
};

// Implementation of NVDGEllipticOperator
// ----------------------------------

template< class RangeDiscreteFunction, class Model, int polOrder >
template< class GF >
void NVDGEllipticOperator< RangeDiscreteFunction, Model, polOrder >
  ::apply( const GF &u, RangeFunctionType &w ) const
{
  // clear destination
  w.clear();

  // get discrete function space
  const RangeDiscreteFunctionSpaceType &dfSpace = w.space();

  // num of Dofs
  const unsigned int numDofs = dfSpace.blockMapper().maxNumDofs() * RangeDiscreteFunctionSpaceType::localBlockSize;

  // basis functions and jacobians
  std::vector< DomainRangeType > phi( numDofs );
  std::vector< DomainJacobianRangeType > dphi( numDofs );
  std::vector< DomainRangeType > phiNb( numDofs );
  std::vector< DomainJacobianRangeType > dphiNb( numDofs );

  // coefficients
  double alpha_ = 1.;

  // Hessian function space
  GridPartType& gridPart = dfSpace.gridPart();
  typedef Dune::Fem::DiscontinuousGalerkinSpace< typename RangeDiscreteFunctionSpaceType::FunctionSpaceType, GridPartType, polOrder > HDiscreteFunctionSpaceType;
  HDiscreteFunctionSpaceType HdfSpace( gridPart );
  const unsigned int HnumDofs = HdfSpace.blockMapper().maxNumDofs() * HDiscreteFunctionSpaceType::localBlockSize;
  typedef Dune::Fem::LocalMassMatrixImplementation< HDiscreteFunctionSpaceType, QuadratureType > LocalMassMatrixImplementation;
  const LocalMassMatrixImplementation massMatrix( HdfSpace );

  // Hessian basis functions and jacobians
  std::vector< DomainRangeType > Hphi( HnumDofs );
  std::vector< DomainJacobianRangeType > Hdphi( HnumDofs );

  typedef Dune::Fem::TemporaryLocalFunction< HDiscreteFunctionSpaceType > TempLocalVectorType;
  // l_ij vector
  std::vector< std::unique_ptr< TempLocalVectorType > > lKij( dimDomain*dimDomain );
  for ( int d = 0; d < dimDomain*dimDomain; ++d )
    lKij[d] = std::make_unique< TempLocalVectorType >( HdfSpace );

  // iterate over grid
  const IteratorType end = dfSpace.end();
  for( IteratorType it = dfSpace.begin(); it != end; ++it )
  {
    // get entity (here element)
    const EntityType &entity = *it;

    bool needsCalculation = model().init( entity );
    if (! needsCalculation )
      continue;

    // get elements geometry
    const GeometryType &geometry = entity.geometry();

    // get local representation of the discrete functions
    const auto uLocal = u.localFunction( entity );
    RangeLocalFunctionType wLocal = w.localFunction( entity );

    // set matrices to 0
    for ( int d = 0; d < dimDomain*dimDomain; ++d )
    {
      (*lKij[d]).init(entity);
      (*lKij[d]).clear();
    }

    // get the basis sets
    typedef typename RangeDiscreteFunctionSpaceType::BasisFunctionSetType BasisFunctionSetType;
    const BasisFunctionSetType &baseSet = wLocal.basisFunctionSet();
    const unsigned int numBaseFunctions = baseSet.size();
    const typename HDiscreteFunctionSpaceType::BasisFunctionSetType HbaseSet = HdfSpace.basisFunctionSet(entity);
    const unsigned int HnumBaseFunctions = HbaseSet.size();

    // obtain quadrature order
    int quadOrder = std::max(
                  2*HdfSpace.order(),                   // H mass matrix
                  HdfSpace.order() + wLocal.order() + 3 // A scaled mass matrix
                  );

    { // element integral
      QuadratureType quadrature( entity, quadOrder );
      const size_t numQuadraturePoints = quadrature.nop();
      for( size_t pt = 0; pt < numQuadraturePoints; ++pt )
      {
        const typename QuadratureType::CoordinateType &x = quadrature.point( pt );
        const double weight = quadrature.weight( pt ) * geometry.integrationElement( x );

        // evaluate all Hessian basis functions and jacobians at given quadrature point
        HbaseSet.evaluateAll( quadrature[ pt ], Hphi );
        HbaseSet.jacobianAll( quadrature[ pt ], Hdphi );

        // get jacobian for local u
        RangeJacobianRangeType dval;
        uLocal.jacobian( quadrature[ pt ], dval );

        for ( unsigned int Hcol = 0; Hcol < HnumBaseFunctions; ++Hcol )
          for ( int i = 0; i < dimDomain; ++i )
            for ( int j = 0; j < dimDomain; ++j )
              (*(lKij[i*dimDomain + j]))[Hcol] -= weight*Hdphi[Hcol][0][i]*dval[0][j];
      }
    }
    if ( 1 ) // ! dfSpace.continuous() )
    {
      const double area = entity.geometry().volume();
      const IntersectionIteratorType iitend = dfSpace.gridPart().iend( entity );
      for( IntersectionIteratorType iit = dfSpace.gridPart().ibegin( entity ); iit != iitend; ++iit ) // looping over intersections
      {
        //! [Compute skeleton terms: iterate over intersections]
        const IntersectionType &intersection = *iit;
        if ( intersection.neighbor() )
        {
          const EntityType outside = Dune::Fem::make_entity( intersection.outside() );

          typedef typename IntersectionType::Geometry  IntersectionGeometryType;
          const IntersectionGeometryType &intersectionGeometry = intersection.geometry();

          // compute penalty factor
          const double intersectionArea = intersectionGeometry.volume();
          const double beta = penalty() * intersectionArea / std::min( area, outside.geometry().volume() );
          const double dbeta = penalty() * intersectionArea / std::min( area, outside.geometry().volume() );

          auto uOutLocal = u.localFunction( outside ); // local u on outside element

          FaceQuadratureType quadInside( dfSpace.gridPart(), intersection, quadOrder, FaceQuadratureType::INSIDE );
          FaceQuadratureType quadOutside( dfSpace.gridPart(), intersection, quadOrder, FaceQuadratureType::OUTSIDE );
          const size_t numQuadraturePoints = quadInside.nop();
          //! [Compute skeleton terms: iterate over intersections]

          for( size_t pt = 0; pt < numQuadraturePoints; ++pt )
          {
            //! [Compute skeleton terms: obtain required values on the intersection]
            // get coordinate of quadrature point on the reference element of the intersection
            const typename FaceQuadratureType::LocalCoordinateType &x = quadInside.localPoint( pt );
            DomainType normal = intersection.integrationOuterNormal( x );
            double faceVol = normal.two_norm();
            normal /= faceVol; // make it into a unit normal
            const double weight = quadInside.weight( pt ) * faceVol;

            RangeRangeType vuIn, vuOut;
            RangeJacobianRangeType duIn, duOut;
            uLocal.evaluate( quadInside[ pt ], vuIn );
            uLocal.jacobian( quadInside[ pt ], duIn );
            uOutLocal.evaluate( quadOutside[ pt ], vuOut );
            uOutLocal.jacobian( quadOutside[ pt ], duOut );
            RangeRangeType jump = vuIn - vuOut;
            /*
            JacobianRangeType djump = duIn; djump -= duOut;
            djump *= dbeta;
            */
            // compute -0.5 * [u] x normal
            RangeJacobianRangeType dvalue;
            for ( int r = 0; r < dimRange; ++r )
              for ( int d = 0; d < dimDomain; ++d )
                dvalue[r][d] = -0.5 * normal[d] * jump[r];
            RangeJacobianRangeType aduIn, aduOut;
            model().init( outside );
            model().diffusiveFlux( quadOutside[ pt ], vuOut, duOut, aduOut );
            model().init( entity );
            model().diffusiveFlux( quadInside[ pt ], vuIn, duIn, aduIn );
            RangeJacobianRangeType affine;
            model().diffusiveFlux( quadInside[ pt ], RangeRangeType(0), RangeJacobianRangeType(0), affine);
            //! [Compute skeleton terms: obtain required values on the intersection]

            //! [Compute skeleton terms: compute factors for axpy method]
            RangeRangeType value;
            RangeJacobianRangeType advalue;
            // penalty term : beta [u] [phi] = beta (u+ - u-)(phi+ - phi-)=beta (u+ - u-)phi+
            value = jump;
            value *= beta;
            // {A grad u}.[phi] = {A grad u}.phi+ n_+ = 0.5*(grad u+ + grad u-).n_+ phi+
            aduIn += aduOut;
            aduIn *= -0.5;
            aduIn.umv(normal, value);
            //  [ u ] * { {A} grad phi_en } = -normal(u+ - u-) * 0.5 {A}    grad phi_en
            //  we actually need  G(u)tau with G(x,u) = d/sigma_j D_i(x,u,sigma)
            //  - we might need to assume D(x,u,sigma) = G(x,u)sigma + affine(x)
            model().diffusiveFlux( quadInside[ pt ], vuIn, dvalue, advalue );
            // advalue -= affine;

            // advalue += djump;

            value *= weight;
            advalue *= weight;
            //! [Compute skeleton terms: compute factors for axpy method]
            wLocal.axpy( quadInside[ pt ], value, advalue );

            /////////////////////////////////////////////////////////////
            // evaluate basis function of face inside E^- (entity)
            /////////////////////////////////////////////////////////////

            // evaluate all Hessian basis functions for quadrature point pt
            HbaseSet.evaluateAll( quadInside[ pt ], Hphi );
            HbaseSet.jacobianAll( quadInside[ pt ], Hdphi );

            // calculate entries for LKij that use neighbouring elements
            for ( unsigned int Hcol = 0; Hcol < HnumBaseFunctions; ++Hcol )
            {
              for ( int i = 0; i < dimDomain; ++i )
              {
                for ( int j = 0; j < dimDomain; ++j )
                {
                  RangeFieldType valueEn( 0 );
                  valueEn += 0.5*Hdphi[Hcol][0][i]*normal[j]*(vuIn[0] - vuOut[0]);
                  valueEn += 0.5*Hphi[Hcol][0]*normal[i]*(duIn[0][j] + duOut[0][j]);
                  (*lKij[i*dimDomain+j])[Hcol] += weight*valueEn;
                }
              }
            }
          }
        }
        else if( intersection.boundary() )
        {
          Dune::FieldVector<int, dimRange> components(1);
          model().isDirichletIntersection( intersection, components);

          typedef typename IntersectionType::Geometry IntersectionGeometryType;
          const IntersectionGeometryType &intersectionGeometry = intersection.geometry();

          // compute penalty factor
          const double intersectionArea = intersectionGeometry.volume();
          const double beta = penalty() * intersectionArea / area;

          FaceQuadratureType quadInside( dfSpace.gridPart(), intersection, quadOrder, FaceQuadratureType::INSIDE );
          const size_t numQuadraturePoints = quadInside.nop();

          for( size_t pt = 0; pt < numQuadraturePoints; ++pt )
          {
            const typename FaceQuadratureType::LocalCoordinateType &x = quadInside.localPoint( pt );
            const DomainType normal = intersection.integrationOuterNormal( x );
            const double weight = quadInside.weight( pt );

            RangeRangeType bndValue;
            model().dirichlet(1, quadInside[pt], bndValue);

            RangeRangeType value;
            RangeJacobianRangeType dvalue, advalue;

            RangeRangeType vuIn, jump;
            RangeJacobianRangeType duIn, aduIn;
            uLocal.evaluate( quadInside[ pt ], vuIn );
            uLocal.jacobian( quadInside[ pt ], duIn );
            jump = vuIn;
            jump -= bndValue;

            for ( int r = 0; r < dimRange; ++r )
              if (!components[r]) // do not use dirichlet constraints here
                jump[r] = 0;

            // penalty term : beta [u] [phi] = beta (u+ - u-)(phi+ - phi-)=beta (u+ - u-)phi+
            value = jump;
            value *= beta * intersectionGeometry.integrationElement( x );

            //  [ u ] * { grad phi_en } = -normal(u+ - u-) * 0.5 grad phi_en
            // here we need a diadic product of u x n
            for ( int r = 0; r < dimRange; ++r )
              for ( int d = 0; d < dimDomain; ++d )
                dvalue[r][d] = - normal[d] * jump[r];

            model().diffusiveFlux( quadInside[ pt ], jump, dvalue, advalue );

            // consistency term
            // {A grad u}.[phi] = {A grad u}.phi+ n_+ = 0.5*(grad u+ + grad u-).n_+ phi+
            model().diffusiveFlux( quadInside[ pt ], vuIn, duIn, aduIn );
            aduIn.mmv(normal, value);

#if 0
            for ( int r = 0; r < dimRange; ++r )
              if (!components[r]) // do not use dirichlet constraints here
              {
                value[r] = 0;
                advalue[r] = 0;
              }
#endif

            value *= weight;
            advalue *= weight;
            wLocal.axpy( quadInside[ pt ], value, advalue );

            /////////////////////////////////////////////////////////////
            // evaluate basis function of face inside E^- (entity)
            /////////////////////////////////////////////////////////////

            // evaluate all Hessian basis functions for quadrature point pt
            HbaseSet.evaluateAll( quadInside[ pt ], Hphi );
            HbaseSet.jacobianAll( quadInside[ pt ], Hdphi );

            // lKij contributions on the boundary
            for ( unsigned int Hcol = 0; Hcol < HnumBaseFunctions; ++Hcol )
              for ( int i = 0; i < dimDomain; ++i )
                for ( int j = 0; j < dimDomain; ++j )
                {
                  RangeFieldType valueEn( 0 );
                  // !!! valueEn += Hdphi[Hcol][0][i]*normal[j]*vuIn[0];
                  valueEn += Hphi[Hcol][0]*normal[i]*duIn[0][j];
                  (*lKij[i*dimDomain+j])[Hcol] += weight*valueEn;
                }
          }
        }
      }
    }
    for ( int d = 0; d < dimDomain*dimDomain; ++d )
      massMatrix.applyInverse(*lKij[d]);

    { // element integral
      QuadratureType quadrature( entity, quadOrder );
      const size_t numQuadraturePoints = quadrature.nop();
      for( size_t pt = 0; pt < numQuadraturePoints; ++pt )
      {
        const typename QuadratureType::CoordinateType &x = quadrature.point( pt );
        const double weight = quadrature.weight( pt ) * geometry.integrationElement( x );

        RangeRangeType vu;
        uLocal.evaluate( quadrature[ pt ], vu );
        RangeJacobianRangeType du;
        uLocal.jacobian( quadrature[ pt ], du );

        // evaluate all Hessian basis functions at given quadrature point
        HbaseSet.evaluateAll( quadrature[ pt ], Hphi );

        RangeHessianRangeType d2u( 0 );
        for ( int Hcol = 0; Hcol < HnumBaseFunctions; ++Hcol )
          for ( int i = 0; i < dimDomain; ++i )
            for ( int j = 0; j < dimDomain; ++j )
              d2u[0][i][j] += (*lKij[i*dimDomain+j])[Hcol]*Hphi[Hcol][0];

        // compute mass contribution (studying linear case so linearizing around zero)
        RangeRangeType avu( 0 );
        model().source( quadrature[ pt ], vu, du, d2u, avu );
        avu *= weight;
        // add to local functional wLocal.axpy( quadrature[ pt ], avu );

        RangeJacobianRangeType adu( 0 );
        // apply diffusive flux
        model().diffusiveFlux( quadrature[ pt ], vu, du, adu );
        adu *= weight;

        // add to local function
        wLocal.axpy( quadrature[ pt ], avu, adu );
      }
    }
  }
  // communicate data (in parallel runs)
  w.communicate();
}

// Implementation of DifferentiableNVDGEllipticOperator
// ------------------------------------------------
template< class JacobianOperator, class Model, int polOrder >
void DifferentiableNVDGEllipticOperator< JacobianOperator, Model, polOrder >
  ::apply ( const DomainFunctionType &u, JacobianOperator &jOp ) const
{
  typedef typename JacobianOperator::LocalMatrixType LocalMatrixType;
  typedef typename RangeDiscreteFunctionSpaceType::BasisFunctionSetType BasisFunctionSetType;

  const DomainDiscreteFunctionSpaceType &domainSpace = jOp.domainSpace();
  const RangeDiscreteFunctionSpaceType  &rangeSpace = jOp.rangeSpace();

  Dune::Fem::DiagonalAndNeighborStencil<DiscreteFunctionSpaceType, DiscreteFunctionSpaceType> stencil(domainSpace, rangeSpace);
  jOp.reserve(stencil);
  jOp.clear();

  GridPartType& gridPart = rangeSpace.gridPart();

  const unsigned int numDofs = rangeSpace.blockMapper().maxNumDofs() * DiscreteFunctionSpaceType::localBlockSize;

  // basis functions and jacobians
  std::vector< RangeRangeType > phi( numDofs );
  std::vector< RangeJacobianRangeType > dphi( numDofs );
  std::vector< RangeRangeType > phiNb( numDofs );
  std::vector< RangeJacobianRangeType > dphiNb( numDofs );

  // Hessian function space
  typedef Dune::Fem::DiscontinuousGalerkinSpace< typename DiscreteFunctionSpaceType::FunctionSpaceType, GridPartType, polOrder > HDiscreteFunctionSpaceType;
  HDiscreteFunctionSpaceType HdfSpace( gridPart );
  const unsigned int HnumDofs = HdfSpace.blockMapper().maxNumDofs() * HDiscreteFunctionSpaceType::localBlockSize;
  typedef Dune::Fem::LocalMassMatrixImplementation< HDiscreteFunctionSpaceType, QuadratureType > LocalMassMatrixImplementation;
  const LocalMassMatrixImplementation massMatrix( HdfSpace );

  // Hessian basis functions and jacobians
  std::vector< RangeRangeType > Hphi( HnumDofs );
  std::vector< RangeJacobianRangeType > Hdphi( HnumDofs );

  double alpha_ = 1.;

  typedef Dune::Fem::TemporaryLocalMatrix< RangeDiscreteFunctionSpaceType, HDiscreteFunctionSpaceType > TempLocalMatrixType;
  // stiffness matrix on current element
  std::vector< std::shared_ptr< TempLocalMatrixType > > LKKij( dimDomain*dimDomain );
  for ( int d = 0; d < dimDomain*dimDomain; ++d )
    LKKij[d] = std::make_shared< TempLocalMatrixType >( rangeSpace, HdfSpace );
  // stiffness matrix on neighbouring elements
  std::vector< std::shared_ptr< TempLocalMatrixType > > LKNij( dimDomain*dimDomain );
  for ( int d = 0; d < dimDomain*dimDomain; ++d )
    LKNij[d] = std::make_shared< TempLocalMatrixType >( rangeSpace, HdfSpace );

  std::vector< std::vector < RangeRangeType > > uOutLocalDofs;

  const IteratorType end = rangeSpace.end();
  for( IteratorType it = rangeSpace.begin(); it != end; ++it )
  {
    const EntityType &entity = *it;

    bool needsCalculation = model().init( entity );
    if (! needsCalculation )
      continue;

    const GeometryType geometry = entity.geometry();

    const auto uLocal = u.localFunction( entity );
    LocalMatrixType jLocal = jOp.localMatrix( entity, entity );

    // create sets of basis functions
    const BasisFunctionSetType &baseSet = jLocal.domainBasisFunctionSet();
    const typename HDiscreteFunctionSpaceType::BasisFunctionSetType HbaseSet = HdfSpace.basisFunctionSet(entity);
    const unsigned int numBaseFunctions = baseSet.size();
    const unsigned int HnumBaseFunctions = HbaseSet.size();

    // set matrices to 0
    for ( int d = 0; d < dimDomain*dimDomain; ++d )
    {
      (*LKKij[d]).init(entity, entity);
      (*LKKij[d]).clear();
    }
    std::vector< std::vector< std::shared_ptr< TempLocalMatrixType > > > LKNijVector(0);

    int order = std::max(
                         2*HdfSpace.order(), // H mass matrix
                         HdfSpace.order() + uLocal.order() + 3
                        );
    QuadratureType quadrature( entity, order );
    const size_t numQuadraturePoints = quadrature.nop();
    for( size_t pt = 0; pt < numQuadraturePoints; ++pt )
    {
      const typename QuadratureType::CoordinateType &x = quadrature.point( pt );
      const double weight = quadrature.weight( pt ) * geometry.integrationElement( x );

      // evaluate all jacobians of basis functions at given quadrature point
      baseSet.jacobianAll( quadrature[ pt ], dphi );
      HbaseSet.jacobianAll( quadrature[ pt ], Hdphi );
      HbaseSet.evaluateAll( quadrature[ pt ], Hphi );

      for( unsigned int localCol = 0; localCol < numBaseFunctions; ++localCol )
        for ( unsigned int Hcol = 0; Hcol < HnumBaseFunctions; ++Hcol )
          for ( int i = 0; i < dimDomain; ++i )
            for ( int j = 0; j < dimDomain; ++j )
              (*(LKKij[i*dimDomain + j]))[Hcol][localCol] -= weight*Hdphi[Hcol][0][i]*dphi[localCol][0][j];
    }
    //for ( int d = 0; d < dimDomain*dimDomain; ++d )
    //  LKNij[d].resize(0);
    uOutLocalDofs.resize(0);

    double area = geometry.volume();
    const IntersectionIteratorType endiit = gridPart.iend( entity );
    for ( IntersectionIteratorType iit = gridPart.ibegin( entity );
          iit != endiit ; ++ iit )
    {
      const IntersectionType& intersection = *iit ;

      if( intersection.neighbor() )
      {
        const EntityType neighbor = Dune::Fem::make_entity( intersection.outside() );

        typedef typename IntersectionType::Geometry  IntersectionGeometryType;
        const IntersectionGeometryType &intersectionGeometry = intersection.geometry();

        auto uOutLocal = u.localFunction( neighbor ); // local u on outside element
        uOutLocalDofs.push_back( std::vector< RangeRangeType >( numDofs ) );
        for( unsigned int localCol = 0; localCol < numBaseFunctions; ++localCol )
          uOutLocalDofs.back()[localCol] = uOutLocal[localCol];

        /*
        for ( int d = 0; d < dimDomain*dimDomain; ++d )
          LKNij[d].push_back( std::make_shared< TempLocalMatrixType >( rangeSpace, HdfSpace ) );
        for ( int d = 0; d < dimDomain*dimDomain; ++d )
        {
          (*LKNij[d].back()).init(neighbor, entity);
          (*LKNij[d].back()).clear();
        }
        */
        for ( int d = 0; d < dimDomain*dimDomain; ++d )
        {
          (*LKNij[d]).init(neighbor, entity);
          (*LKNij[d]).clear();
        }

        //! [Assemble skeleton terms: get contributions on off diagonal block]
        // get local matrix for face entries
        LocalMatrixType localOpNb = jOp.localMatrix( neighbor, entity );
        // get neighbor's base function set
        const BasisFunctionSetType &baseSetNb = localOpNb.domainBasisFunctionSet();
        const typename HDiscreteFunctionSpaceType::BasisFunctionSetType HbaseSetNb = HdfSpace.basisFunctionSet(neighbor);
        //! [Assemble skeleton terms: get contributions on off diagonal block]

        // compute penalty factor
        const double intersectionArea = intersectionGeometry.volume();
        const double beta = penalty() * intersectionArea / std::min( area, neighbor.geometry().volume() );
        const double dbeta = penalty() * intersectionArea / std::min( area, neighbor.geometry().volume() );

        // here we assume that the intersection is conforming
        int forder = 2+std::max( 2*HdfSpace.order(), HdfSpace.order() + uLocal.order() );
        FaceQuadratureType faceQuadInside(gridPart, intersection, forder,
                                          FaceQuadratureType::INSIDE);
        FaceQuadratureType faceQuadOutside(gridPart, intersection, forder,
                                           FaceQuadratureType::OUTSIDE);

        const size_t numFaceQuadPoints = faceQuadInside.nop();
        for( size_t pt = 0; pt < numFaceQuadPoints; ++pt )
        {
          const typename FaceQuadratureType::LocalCoordinateType &x = faceQuadInside.localPoint( pt );
          DomainType normal = intersection.integrationOuterNormal( x );
          double faceVol = normal.two_norm();
          normal /= faceVol; // make it into a unit normal

          const double quadWeight = faceQuadInside.weight( pt );
          const double weight = quadWeight * faceVol;

          //! [Assemble skeleton terms: obtain values on quadrature point]
          RangeRangeType u0En;
          RangeJacobianRangeType u0EnJac;
          uLocal.evaluate( faceQuadInside[ pt ], u0En );
          uLocal.jacobian( faceQuadInside[ pt ], u0EnJac );

          /////////////////////////////////////////////////////////////
          // evaluate basis function of face inside E^- (entity)
          /////////////////////////////////////////////////////////////

          // evaluate all basis functions for quadrature point pt
          baseSet.evaluateAll( faceQuadInside[ pt ], phi );
          baseSet.jacobianAll( faceQuadInside[ pt ], dphi );

          // evaluate the jacobians of all basis functions
          HbaseSet.evaluateAll( faceQuadInside[ pt ], Hphi );
          HbaseSet.jacobianAll( faceQuadInside[ pt ], Hdphi );

          /////////////////////////////////////////////////////////////
          // evaluate basis function of face inside E^+ (neighbor)
          /////////////////////////////////////////////////////////////

          // evaluate all basis functions for quadrature point pt on neighbor
          baseSetNb.evaluateAll( faceQuadOutside[ pt ], phiNb );
          baseSetNb.jacobianAll( faceQuadOutside[ pt ], dphiNb );

          for( unsigned int localCol = 0; localCol < numBaseFunctions; ++localCol )
            for ( unsigned int Hcol = 0; Hcol < HnumBaseFunctions; ++Hcol )
              for ( int i = 0; i < dimDomain; ++i )
                for ( int j = 0; j < dimDomain; ++j )
                {
                  RangeFieldType valueEn( 0 ), valueNb( 0 );
                  valueEn += 0.5*Hdphi[Hcol][0][i]*normal[j]*phi[localCol][0];
                  valueNb += 0.5*Hdphi[Hcol][0][i]*normal[j]*phiNb[localCol][0];
                  valueEn += 0.5*Hphi[Hcol][0]*normal[i]*dphi[localCol][0][j];
                  valueNb -= 0.5*Hphi[Hcol][0]*normal[i]*dphiNb[localCol][0][j];
                  (*LKKij[i*dimDomain+j])[Hcol][localCol] += weight*valueEn;
                  (*LKNij[i*dimDomain+j])[Hcol][localCol] -= weight*valueNb;
                  //(*LKNij[i*dimDomain+j].back())[Hcol][localCol] -= weight*valueNb;
                }

          model().init( neighbor );
          for( unsigned int i = 0; i < numBaseFunctions; ++i )
          {
            JacobianRangeType adphiNb = dphiNb[ i ];
            model().linDiffusiveFlux( u0En, u0EnJac, faceQuadOutside[ pt ], phiNb[i], adphiNb, dphiNb[ i ] );
          }
          model().init( entity );
          for( unsigned int i = 0; i < numBaseFunctions; ++i )
          {
            JacobianRangeType adphiEn = dphi[ i ];
            model().linDiffusiveFlux( u0En, u0EnJac, faceQuadInside[ pt ], phi[i], adphiEn, dphi[ i ] );
          }
          //! [Assemble skeleton terms: obtain values om quadrature point]

          //! [Assemble skeleton terms: compute factors for axpy method]
          for( unsigned int localCol = 0; localCol < numBaseFunctions; ++localCol )
          {
            RangeRangeType valueEn( 0 ), valueNb( 0 );
            RangeJacobianRangeType dvalueEn( 0 ), dvalueNb( 0 );

            //  -{ A grad u } * [ phi_en ]
            dphi[localCol].usmv( -0.5, normal, valueEn );

            //  -{ A grad u } * [ phi_en ]
            dphiNb[localCol].usmv( -0.5, normal, valueNb );

            //  [ u ] * [ phi_en ] = u^- * phi_en^-
            valueEn.axpy( beta, phi[ localCol ] );

            //  [ u ] * [ phi_en ] = u^- * phi_en^-
            valueNb.axpy(-beta, phiNb[ localCol ] );

            // here we need a diadic product of u x n
            for ( int r = 0; r < dimRange; ++r )
              for ( int d = 0; d < dimDomain; ++d )
              {
                //  [ u ] * { grad phi_en }
                dvalueEn[r][d] = - 0.5 * normal[d] * phi[localCol][r];

                //  [ u ] * { grad phi_en }
                dvalueNb[r][d] = 0.5 * normal[d] * phiNb[localCol][r];
              }
            model().init( neighbor );
            auto advalue = dvalueNb;
            model().linDiffusiveFlux( u0En, u0EnJac, faceQuadOutside[ pt ], phiNb[localCol], advalue, dvalueNb );
            model().init( entity );
            advalue = dvalueEn;
            model().linDiffusiveFlux( u0En, u0EnJac, faceQuadInside[ pt ], phi[localCol], advalue, dvalueEn );

            //!!!!! note: this is a problem because dphi/dphiNb has been put through the diffusive flux
            // dvalueEn.axpy( dbeta,dphi[localCol]);
            // dvalueNb.axpy(-dbeta,dphiNb[localCol]);
            jLocal.column( localCol ).axpy( phi, dphi, valueEn, dvalueEn, weight );
            localOpNb.column( localCol ).axpy( phi, dphi, valueNb, dvalueNb, weight );
          }
          //! [Assemble skeleton terms: compute factors for axpy method]
        }

        // LKN entity contribution completed
        for ( int d = 0; d < dimDomain*dimDomain; ++d )
          massMatrix.rightMultiplyInverse( *( LKNij[d] ) );
          //massMatrix.rightMultiplyInverse( *( LKNij[d].back() ) );

        LKNijVector.push_back( LKNij );
        for ( int d = 0; d < dimDomain*dimDomain; ++d )
          LKNij[d] = std::make_shared< TempLocalMatrixType >( rangeSpace, HdfSpace );

      }
      else if( intersection.boundary() )
      {
        Dune::FieldVector<int, dimRange> components(1);
        model().isDirichletIntersection( intersection, components);

        typedef typename IntersectionType::Geometry  IntersectionGeometryType;
        const IntersectionGeometryType &intersectionGeometry = intersection.geometry();

        // compute penalty factor
        const double intersectionArea = intersectionGeometry.volume();
        const double beta = penalty() * intersectionArea / area;

        // here we assume that the intersection is conforming
        int forder = 2+std::max( 2*HdfSpace.order(), HdfSpace.order() + uLocal.order() );
        FaceQuadratureType faceQuadInside(gridPart, intersection, forder,
                                          FaceQuadratureType::INSIDE);

        const size_t numFaceQuadPoints = faceQuadInside.nop();
        for( size_t pt = 0; pt < numFaceQuadPoints; ++pt )
        {
          const typename FaceQuadratureType::LocalCoordinateType &x = faceQuadInside.localPoint( pt );
          DomainType normal = intersection.integrationOuterNormal( x );
          double faceVol = normal.two_norm();
          normal /= faceVol; // make it into a unit normal

          const double quadWeight = faceQuadInside.weight( pt );
          const double weight = quadWeight * faceVol;

          RangeRangeType u0En;
          RangeJacobianRangeType u0EnJac;
          uLocal.evaluate( faceQuadInside[ pt ], u0En );
          uLocal.jacobian( faceQuadInside[ pt ], u0EnJac );

          /////////////////////////////////////////////////////////////
          // evaluate basis function of face inside E^- (entity)
          /////////////////////////////////////////////////////////////

          // evaluate all basis functions for quadrature point pt
          baseSet.evaluateAll( faceQuadInside[ pt ], phi );
          baseSet.jacobianAll( faceQuadInside[ pt ], dphi );

          // evaluate all Hessian basis functions for quadrature point pt
          HbaseSet.evaluateAll( faceQuadInside[ pt ], Hphi );
          HbaseSet.jacobianAll( faceQuadInside[ pt ], Hdphi );

          // LKK contributions on the boundary
          for( unsigned int localCol = 0; localCol < numBaseFunctions; ++localCol )
            for ( unsigned int Hcol = 0; Hcol < HnumBaseFunctions; ++Hcol )
              for ( int i = 0; i < dimDomain; ++i )
                for ( int j = 0; j < dimDomain; ++j )
                {
                  RangeFieldType valueEn( 0 );
                  // !!! valueEn += Hdphi[Hcol][0][i]*normal[j]*phi[localCol][0];
                  valueEn += Hphi[Hcol][0]*normal[i]*dphi[localCol][0][j];
                  (*LKKij[i*dimDomain + j])[Hcol][localCol] += weight*valueEn;
                }

          for( unsigned int i = 0; i < numBaseFunctions; ++i )
          {
            JacobianRangeType adphiEn = dphi[ i ];
            model().linDiffusiveFlux( u0En, u0EnJac, faceQuadInside[ pt ], phi[i], adphiEn, dphi[ i ] );
          }

          for( unsigned int localCol = 0; localCol < numBaseFunctions; ++localCol )
          {
            RangeRangeType valueEn( 0 );
            RangeJacobianRangeType dvalueEn( 0 );

            //  -{ A grad u } * [ phi_en ]
            dphi[localCol].usmv( -1.0, normal, valueEn );

            //  [ u ] * [ phi_en ] = u^- * phi_en^-

            for ( int r = 0; r < dimRange; ++r )
              if (components[r])
                valueEn[r] += beta*phi[ localCol ][r];

#if 0 //!!! unsure about this
            // here we need a diadic product of u x n
            for ( int r = 0; r < dimRange; ++r )
              for ( int d = 0; d < dimDomain; ++d )
              {
                //  [ u ] * { grad phi_en }
                dvalueEn[r][d] = - normal[d] * phi[localCol][r];
              }
#endif
#if 0
            for ( int r = 0; r < dimRange; ++r )
              if (!components[r]) // do not use dirichlet constraints here
              {
                valueEn[r] = 0;
                dvalueEn[r] = 0;
              }
#endif

            jLocal.column( localCol ).axpy( phi, dphi, valueEn, dvalueEn, weight );
          }
        }
      }
    }

    // LKK entity contribution completed
    for ( int d = 0; d < dimDomain*dimDomain; ++d )
      massMatrix.rightMultiplyInverse(*LKKij[d]);

    for( size_t pt = 0; pt < numQuadraturePoints; ++pt )
    {
      const typename QuadratureType::CoordinateType &x = quadrature.point( pt );
      const double weight = quadrature.weight( pt ) * geometry.integrationElement( x );

      // evaluate all basis functions and jacobians at given quadrature point
      baseSet.evaluateAll( quadrature[ pt ], phi );
      baseSet.jacobianAll( quadrature[ pt ], dphi );
      HbaseSet.evaluateAll( quadrature[ pt ], Hphi );

      // get value for linearization
      RangeRangeType u0;
      RangeJacobianRangeType jacU0;
      uLocal.evaluate( quadrature[ pt ], u0 );
      uLocal.jacobian( quadrature[ pt ], jacU0 );

      HessianRangeType hessU0( 0 );
      for ( unsigned int localCol = 0; localCol < numBaseFunctions; ++localCol )
        for ( int i = 0; i < dimDomain; ++i )
          for ( int j = 0; j < dimDomain; ++j )
            for ( unsigned int Hcol = 0; Hcol < HnumBaseFunctions; ++Hcol )
            {
              hessU0[0][i][j] += (*LKKij[i*dimDomain+j])[Hcol][localCol]*uLocal[localCol]*Hphi[Hcol][0];
              for ( int n = 0; n < LKNijVector.size(); ++n )
                hessU0[0][i][j] += (*LKNijVector[n][i*dimDomain+j])[Hcol][localCol]*uOutLocalDofs[n][localCol]*Hphi[Hcol][0];
            }

      for ( unsigned int localCol = 0; localCol < numBaseFunctions; ++localCol )
      {
        HessianRangeType d2phi( 0 );
        for ( int i = 0; i < dimDomain; ++i )
          for ( int j = 0; j < dimDomain; ++j )
            for ( unsigned int Hcol = 0; Hcol < HnumBaseFunctions; ++Hcol )
              d2phi[0][i][j] += (*LKKij[i*dimDomain+j])[Hcol][localCol]*Hphi[Hcol][0];

        RangeRangeType aphi( 0 );
        RangeJacobianRangeType adphi( 0 );
        // if mass terms or right hand side is present
        model().linSource( u0, jacU0, hessU0, quadrature[ pt ], phi[ localCol ], dphi[ localCol ], d2phi, aphi );

        // if gradient term is present
        model().linDiffusiveFlux( u0, jacU0, quadrature[ pt ], phi[ localCol ], dphi[ localCol ], adphi );

        // get column object and call axpy method
        jLocal.column( localCol ).axpy( phi, dphi, aphi, adphi, weight );
      }
    }

    int nbNumber = 0;
    // const IntersectionIteratorType endiit = gridPart.iend( entity );
    for ( IntersectionIteratorType iit = gridPart.ibegin( entity );
          iit != endiit ; ++ iit )
    {
      const IntersectionType& intersection = *iit ;

      if( intersection.neighbor() )
      {
        const EntityType neighbor = Dune::Fem::make_entity( intersection.outside() );

        LocalMatrixType localOpNb = jOp.localMatrix( neighbor, entity );
        for( size_t pt = 0; pt < numQuadraturePoints; ++pt )
        {
          const typename QuadratureType::CoordinateType &x = quadrature.point( pt );
          const double weight = quadrature.weight( pt ) * geometry.integrationElement( x );

          // evaluate all basis functions and jacobians at given quadrature point
          baseSet.evaluateAll( quadrature[ pt ], phi );
          baseSet.jacobianAll( quadrature[ pt ], dphi );
          HbaseSet.evaluateAll( quadrature[ pt ], Hphi );

          // get value for linearization
          RangeRangeType u0;
          RangeJacobianRangeType jacU0;
          uLocal.evaluate( quadrature[ pt ], u0 );
          uLocal.jacobian( quadrature[ pt ], jacU0 );

          HessianRangeType hessU0( 0 );
          for ( unsigned int localCol = 0; localCol < numBaseFunctions; ++localCol )
            for ( int i = 0; i < dimDomain; ++i )
              for ( int j = 0; j < dimDomain; ++j )
                for ( unsigned int Hcol = 0; Hcol < HnumBaseFunctions; ++Hcol )
                {
                  hessU0[0][i][j] += (*LKKij[i*dimDomain+j])[Hcol][localCol]*uLocal[localCol]*Hphi[Hcol][0];
                  for ( int n = 0; n < LKNijVector.size(); ++n )
                    hessU0[0][i][j] += (*LKNijVector[n][i*dimDomain+j])[Hcol][localCol]*uOutLocalDofs[n][localCol]*Hphi[Hcol][0];
                }

          for ( unsigned int localCol = 0; localCol < numBaseFunctions; ++localCol )
          {
            HessianRangeType d2phiNb( 0 );
            for ( int i = 0; i < dimDomain; ++i )
              for ( int j = 0; j < dimDomain; ++j )
                for ( unsigned int Hcol = 0; Hcol < HnumBaseFunctions; ++Hcol )
                  d2phiNb[0][i][j] += (*LKNijVector[nbNumber][i*dimDomain+j])[Hcol][localCol]*Hphi[Hcol][0];

            RangeRangeType aHphi( 0 );
            // if mass terms or right hand side is present
            model().linSource( u0, jacU0, hessU0, quadrature[ pt ], RangeRangeType(0), RangeJacobianRangeType(0), d2phiNb, aHphi );

            // get column object and call axpy method
            localOpNb.column( localCol ).axpy( phi, aHphi, weight );
          }
        }

        ++nbNumber;
      }
    }

  } // end grid traversal
  jOp.flushAssembly();
}

#endif // ELLIPTIC_HH
