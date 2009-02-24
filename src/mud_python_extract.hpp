#ifndef MUD_PYTHON_EXTRACT_H
#define MUD_PYTHON_EXTRACT_H

#include <boost/python.hpp>

namespace python = boost::python;

#include "logger.hpp"
#include "mud_python_base.hpp"

template < typename T > T python_extract( std::string object ) {

 python::extract< T > ex( DICT[ object.c_str() ] );

  if ( ex.check() ) {
    return ex();
  }
  else {
    LOG_HIGH( PY, "python_extract object='" << std::string( object ) << "' failed check");
    throw std::runtime_error("python_extract failed check");
  }
}

#endif
