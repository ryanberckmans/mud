
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>

namespace python = boost::python;

#include "logger.hpp"
#include "mud_python_extract.hpp"
#include "mud_python.hpp"


BOOST_PYTHON_MODULE(cppTypes)
{
  python::class_<std::vector<int> >("IntVector")
    .def( python::vector_indexing_suite< std::vector<int> >());

  python::class_<std::map<int, std::string> >("IntStringMap")
    .def( python::map_indexing_suite< std::map< int, std::string>, true  >());


}

PythonWrapper::PythonWrapper() {
  
  Py_Initialize();
   
  try {

    /*
      No more registration. Just export .so and load in python
    // Register module
    if (PyImport_AppendInittab("cppTypes", initcppTypes ) == -1) {
      throw std::runtime_error("Failed to add cppTypes to the interpreter's built in modules");
    }
    */
    
    python::object main = python::import("__main__");
    dict = main.attr("__dict__");
  }
  catch ( ... ) {
    python::handle_exception();
    PyErr_Print();
  }
  
}

PythonWrapper* PythonWrapper::inst;

void python_exec_file( std::string file ) {
  python_exec_file( file.c_str() );
}

void python_exec_file( char const * const file ) {
  try {
    python::object ignore_result = python::exec_file( file, 
                                                      PythonWrapper::instance().dict,
                                                      PythonWrapper::instance().dict );
  }
  catch ( ... ) {
    python::handle_exception();
    PyErr_Print();
    throw 0;
  }
}

void python_exec( std::string script ) {
  python_exec( script.c_str() );
}

void python_exec( char const * const script ) {
  try {
    python::object ignore_result = python::exec( script,
                                                 PythonWrapper::instance().dict,
                                                 PythonWrapper::instance().dict );
  }
  catch ( ... ) {
    python::handle_exception();
    PyErr_Print();
    throw 0;
  }
}

void test_mud_python() {

  
  try {
    
    python::object &dict = PythonWrapper::instance().dict;

    python::exec("testvec = IntVector()\n", dict, dict);
    
    python::exec("print \"hello!\"\n", dict, dict );
    
    python::exec("print len(testvec)\n", dict, dict );
    
    python::extract< std::vector< int >& > ex( dict["testvec"] );
    
    
    if ( ex.check() ) {
      std::vector<int> &testvec = ex();
      
      testvec.push_back( 1 ); 
      
      exec("print len(testvec)\n", dict, dict );
      
      testvec.clear();

      testvec.push_back( 1 );

      testvec.push_back( 7 );
      
      exec("print len(testvec)\n", dict, dict );

      exec("print testvec[1]\n", dict, dict );
      
      testvec.clear();
      
      exec("print len(testvec)\n", dict, dict );
      
    }

    python::exec_file("account.py", dict, dict );

    python::exec("print repr(dir())\n",dict,dict);
    
    
  }
  catch ( ... ){
    python::handle_exception();
    PyErr_Print();
  }

}

