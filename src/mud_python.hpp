#ifndef MUD_PYTHON_H
#define MUD_PYTHON_H

#include <string>
#include <vector>

using namespace std;


void test_mud_python();

void python_exec_file( string  file);
void python_exec_file( char const * const file);

void python_exec( string script );
void python_exec( char const * const script );


#endif
