#include <boost/date_time/posix_time/posix_time.hpp>

#include "logger.hpp"
#include "mud_python.hpp"
#include "sockets.hpp"

int next_player_id() {
  static int pid = 0;
  return pid++;
}
player_connection::player_connection( socket_ptr socket, socket_server *server ) : _socket(socket), _player_id(next_player_id()), _server(server) { start_read(); }

player_connection::~player_connection() { LOG_MED( SS, "player connection " << _player_id << " destroyed" ); }

// gets the next command from this connection, if any, and adds it to the queue
void player_connection::tick( map<int, string> &cmds ) {
  //LOG_LOW( SS, "playesize " << cmds.size() );
  if ( _cmds.size() > 0 ) {


    // the cmds map shouldn't contain a key for this player_id already because we only send one command per id per tick
    assert( cmds.find( _player_id ) == cmds.end() );

    cmds[ _player_id ] = _cmds.front();

    LOG_LOW( SS, "player_connection::tick id (" << _player_id << ") added cmd '" << _cmds.front() << "' to the tick queue " );
    _cmds.pop();
  }
}

void player_connection::start_read() {
  
  _socket->async_read_some( boost::asio::buffer(_raw), 
                            boost::bind( &player_connection::handle_read, this, 
                                         boost::asio::placeholders::error, 
                                         boost::asio::placeholders::bytes_transferred ));
}

void player_connection::handle_read( const boost::system::error_code error, const size_t len ) {

  if ( error && error != boost::asio::error::eof ) {
    //LOG_HIGH( SS, "player connection (" << _player_id << ") received an error that was not eof " );
    // ASSUME disconnected by mud
    return;
  }

  if( error == boost::asio::error::eof ) {
    LOG_LOW( SS, "player connection (" << _player_id << ") received eof ") ;
    _server->lost_link( _player_id );
    return;
  }
  
  // I think the handler won't get called until it reads *some* data, unless there is an error.
  // So if we get this far len shouldn't be 0
  assert( len > 0 );
  
  if ( len > 0 ) {
    //      LOG_LOW( SS, "read " << len );
  }
  
  for( int i = 0 ; i < len ; ++i) {
    _buf += _raw[i];
  }
  
  get_commands();
  
  start_read();
}

// searches raw buffer for command seperator endl
// pushes all commands onto command buffer
void player_connection::get_commands() {
  
  assert( _cmds.size() <= MAX_COMMANDS );
  
  vector< string > cmds;
  
  boost::split( cmds, _buf, boost::is_any_of("\n\r" ), boost::token_compress_on );
  
  if ( cmds.size() > 1 ) {
    
    LOG_LOW( SS, " player connection " << _player_id << " received " << cmds.size() - 1 << " new commands ");
    
    vector< string >::iterator it = cmds.begin(), end = cmds.end();
    
    end--; // do not include the last 'cmd' which is in fact not terminated by endl
    
    for( ; it != end ; it++ ) {
      
      string cmd = *it;
      boost::trim_left(cmd);
      
      
      if ( cmd.size() < 1 ) {
        // empty command (whitespace), do nothing
      }
      else if ( boost::starts_with( cmd, "--") ) {
        LOG_LOW( SS, " player connection " << _player_id << " flushed their command buffer " << cmd );
        while ( !_cmds.empty() ) { _cmds.pop(); }
        _flushed = true;
      }
      else {
        
        if ( _cmds.size() == MAX_COMMANDS ) {
          LOG_LOW( SS, " player connection " << _player_id << " has maxxed their command queue, discarding remaining input " );
          //@TODO tell player they sent too many commands
          _buf = "";
          return;
        }
        
        _cmds.push( cmd );
        LOG_LOW( SS, " playercon " << _player_id << " queued cmd " << cmd );
      }
    }
    
    LOG_LOW( SS, " player connection " << _player_id << " has " << _cmds.size() << " cmds queued " );
    
    _buf = cmds.back();
    
    boost::trim_left( _buf );
    
    LOG_LOW( SS, " with buffer '" << _buf << "'" );
    
  }
}

void player_connection::send( string to_send ) {

  boost::system::error_code error;

  _socket->write_some( boost::asio::buffer( to_send ), error );

  if ( error ) {
    LOG_HIGH( SS, " playercon " << _player_id << " received error (" << error << ") while sending " );
  }

  /* bool write_in_progress = !_msgs.empty();

  _msgs.push( to_send );

  if ( !write_in_progress ) {
    // begin async write
    boost::asio::async_write( _socket, boost::asio::buffer(_msgs.front()), boost::bind(&player::connection::handle_write,
                                                                                       shared_from_this(),
                                                                                       boost::asio::placeholders::error));


                                                                                       }*/
}

socket_server::socket_server( boost::asio::io_service &io_service ) 
  : _acceptor(io_service, tcp::endpoint(tcp::v4(), 4000)) { 
  start_accept(); 
}

void socket_server::tick( socket_data &data ) {

  data._lost_link = vector<int>( _lost_link );
  _lost_link.clear();

  data._new_cons = vector<int>( _new_cons );
  _new_cons.clear();

  data._flushed.clear();

  data._cmds.erase( data._cmds.begin(), data._cmds.end() );
  data._msgs.erase( data._msgs.begin(), data._msgs.end() );


  map< int, player_connection::player_connection_ptr>::iterator it = _connections.begin();

  for( ; it != _connections.end(); ++it ) {
    LOG_LOW( SS, "cmds size " << data._cmds.size() );
    it->second->tick( data._cmds );

    if ( it->second->flushed() ) {
      LOG_LOW( SS, " playercon " << it->second->id() << " flushed their connection, forwarding this to cmd router" );
      data._flushed.push_back( it->second->id() );
    }
  }

}


// lost link occurs when the client disconnects. A clean quit will always result in the server disconnecting
// the client.
void socket_server::lost_link( int id ) {
  
  LOG_LOW( SS, "playercon " << id << " lost link " );

  _lost_link.push_back( id );
  
  disconnect( id );
  
}

void socket_server::disconnect( vector< int > ids ) {

  vector<int >::iterator it = ids.begin();

  for(; it != ids.end() ; ++it ) {
    disconnect( *it );
  }

}

void socket_server::disconnect( int id ) {
  
  assert( _connections.find( id ) != _connections.end() );
  _connections.erase( id );
  
  LOG_LOW( SS, "player connection (" << id << ") has been disconnected" );
}

void socket_server::start_accept() {
  
  socket_ptr socket( new tcp::socket( _acceptor.io_service() ));
  
  _acceptor.async_accept( *socket, boost::bind(&socket_server::handle_accept, this, socket, boost::asio::placeholders::error));
  
}

void socket_server::handle_accept( socket_ptr socket, const boost::system::error_code& error ) {
  
  if ( error ) {
    LOG_HIGH( SS, "error accepting socket (error code " << error << ")");      
  }
  else {

    player_connection::player_connection_ptr con( new player_connection( socket, this ) );
    _connections[con->id()] =  con;
    _new_cons.push_back( con->id());
    LOG_LOW( SS, "accepted playercon " << con->id() );
  }
  
  start_accept();
}

void socket_server::send( int id, string msg ) {

  assert( _connections.find( id ) != _connections.end() );
  _connections[id]->send( msg );

}

void socket_server::send( vector< int> ids, string msg ) {

  vector< int >::iterator it = ids.begin();

  for( ; it != ids.end() ; ++it ) {
    assert( _connections.find( *it ) != _connections.end() );
    _connections[*it]->send( msg );
  }
}

/*
int main() {

  boost::asio::io_service io;

  socket_server s(io);

  socket_data_ptr data( new socket_data );

  boost::asio::deadline_timer t( io, boost::posix_time::seconds(5) );

  t.async_wait( boost::bind( &ticker, data, &s, &t  ) );
  
  //  for (;;) {
  io.run();
  //  cout << "Loop!" << endl;
  //  }
  
}

*/
