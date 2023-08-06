#ifndef DUNE_FEMNV_SCHEMES_CAPABILITIES_HH
#define DUNE_FEMNV_SCHEMES_CAPABILITIES_HH

#include <dune/fem/schemes/capabilities.hh>

namespace Dune
{
  namespace Fem
  {
    // forward declaration
    template< class DiscreteFunction, class Model, int polOrder, class Constraints >
    class NVDGEllipticOperator;

    template< class JacobianOperator, class Model, int polOrder, class Constraints >
    class NVDGDifferentiableEllipticOperator;

    namespace Capabilities
    {
      template< class DiscreteFunction, class Model, int polOrder, class Constraints >
      struct useGridFunction< NVDGEllipticOperator< DiscreteFunction, Model, polOrder, Constraints > >
      {
        static const bool apply = true;
      };

      template< class JacobianOperator, class Model, int polOrder, class Constraints >
      struct useGridFunction< DifferentiableNVDGEllipticOperator< JacobianOperator, Model, polOrder, Constraints > >
      {
        static const bool apply = false;
      };
    }
  }
}

#endif // #ifndef DUNE_FEMNV_SCHEMES_CAPABILITIES_HH
