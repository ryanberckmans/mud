#include <set>

#include <boost/python.hpp>

#include "logger.hpp"
#include "sockets.hpp"
#include "mud_python.hpp"
#include "mud_python_extract.hpp"
#include "cmd_router.hpp"

int main () {

  python_exec( std::string("import mud\n"
  "import mud.core\n"
  "import mud.core.tick\n"
  "print dir(mud)\n"
  "print dir(mud.core)\n"
  "print mud.__all__\n"
  "HACK_DC = mud.core.tick.disconnectedClients\n"
  "HACK_NEW = mud.core.tick.newClients\n"
  "HACK_FLUSHED = mud.core.tick.flushedClients\n"
  "HACK_CMDS = mud.core.tick.clientCmds\n"
  "HACK_MSGS = mud.core.tick.clientMsgs\n"
                           )
    );

  boost::asio::io_service io;
  socket_server server( io );

  socket_data data( python_extract< vector< int >& >( std::string("HACK_DC") ),
                    python_extract< vector< int>& >( std::string("HACK_NEW") ),
                    python_extract< vector< int >& >( std::string("HACK_FLUSHED") ),
                    python_extract< map< int, string>& >( std::string("HACK_CMDS") ),
                    python_extract< map< int, string>& >( std::string("HACK_MSGS") )
                    );

  cmd_router c(io, data, server);

  io.run();

}

