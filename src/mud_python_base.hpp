
#define DICT PythonWrapper::instance().dict

class PythonWrapper {
  
 public:

  python::object dict;
  
  static PythonWrapper &instance() {
    
    if ( inst == NULL ) {
      inst = new PythonWrapper();
    }
    
    return *inst;
  }

 private:
  
  PythonWrapper(); 
  
 private:
  static PythonWrapper *inst;
};

