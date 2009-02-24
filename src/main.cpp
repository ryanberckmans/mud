#include <set>

#include <boost/python.hpp>

#include "logger.hpp"
#include "sockets.hpp"
#include "mud_python.hpp"
#include "mud_python_extract.hpp"
#include "cmd_router.hpp"

int main () {

  python_exec_file( std::string("init_mud_python.py") );

  boost::asio::io_service io;
  socket_server server( io );

  socket_data data( python_extract< vector< int >& >( std::string("_lost_link") ),
                    python_extract< vector< int>& >( std::string("_new_cons") ),
                    python_extract< vector< int >& >( std::string("_flushed") ),
                    python_extract< map< int, string>& >( std::string("_cmds") ),
                    python_extract< map< int, string>& >( std::string("_msgs") )
                    );

  cmd_router c(io, data, server);

  io.run();

}

