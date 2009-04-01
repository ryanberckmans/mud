#include <set>

#include "logger.hpp"
#include "sockets.hpp"
#include "mud_python.hpp"
#include "cmd_router.hpp"


#define TICK_LENGTH 250

using namespace std;


cmd_router::cmd_router( boost::asio::io_service &io_service, 
                        socket_data &data, 
                        socket_server &server ) : 
  _socket_data( data ), 
  _server( server), 
  _timer(io_service, boost::posix_time::milliseconds( TICK_LENGTH) ) { start(); }


void cmd_router::start() {
  _timer.async_wait( boost::bind( &cmd_router::tick, this ) );
}

void cmd_router::tick() {
  
  LOG_LOW( CR, " TICK: began " );
  
  _server.tick( _socket_data );
  
  
  LOG_MED( CR, " TICK: " << _socket_data._cmds.size() << " cmds, " << _socket_data._new_cons.size() << " new, " << _socket_data._lost_link.size() << " lls, " << _socket_data._flushed.size() << " flushed");
  

  python_exec("mud.core.tick.tick()");

  // _socket_data._msgs was populated inside tick.py
  map< int, string >::iterator it = _socket_data._msgs.begin();

  for(; it != _socket_data._msgs.end() ; ++it ){
    _server.send( it->first, it->second );
  }

  _timer.expires_at( _timer.expires_at() + boost::posix_time::milliseconds( TICK_LENGTH ) );
  
  _timer.async_wait( boost::bind( &cmd_router::tick, this ) );
}  



