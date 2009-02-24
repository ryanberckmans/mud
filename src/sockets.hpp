#ifndef SOCKETS_H
#define SOCKETS_H

#include <queue>
#include <utility>
#include <string>
#include <vector>
#include <map>
#include "assert.h"
#include <boost/shared_ptr.hpp>
#include <boost/enable_shared_from_this.hpp>
#include <boost/asio.hpp>
#include <boost/array.hpp>
#include <boost/bind.hpp>
#include <boost/foreach.hpp>
#include <boost/algorithm/string.hpp>

using boost::asio::ip::tcp;
using namespace std;

class socket_data { 

public:
  socket_data( vector< int> &lost_link, vector<int> &new_cons, vector<int> &flushed, map< int, string> &cmds, map<int, string> &msgs ) : _lost_link( lost_link), _new_cons( new_cons), _flushed( flushed), _cmds( cmds ), _msgs( msgs) {}

  typedef int player_id;

  vector<player_id> &_lost_link; // the set of players that lost link this tick
  vector<player_id> &_new_cons; // the set of players that connected this tick
  vector<player_id> &_flushed; // the set of players that flushed their cmd buffer this tick
                               // a player in this set may still have a cmd this tick, since flushes are processed by the game first
  map< int, string > &_cmds;


  map< int, string > &_msgs; // outbound msgs temporary maybe

};

typedef boost::shared_ptr< socket_data > socket_data_ptr;
typedef boost::shared_ptr< tcp::socket > socket_ptr;

class socket_server;

class player_connection : public boost::enable_shared_from_this< player_connection> {

public:
  
  typedef boost::shared_ptr< player_connection > player_connection_ptr;

  player_connection( socket_ptr socket, socket_server *server );

  virtual ~player_connection();

  // gets the next command from this connection, if any, and adds it to the queue
  void tick( map<int, string> &cmds );

  int id() { return _player_id; }

  void send( string to_send );

  bool flushed() { bool flushed = _flushed; _flushed = false; return flushed; }

private:

  void start_read();

  void handle_read( const boost::system::error_code error, const size_t len );

  // searches raw buffer for command seperator endl
  // pushes all commands onto command buffer
  void get_commands();

  socket_ptr _socket;
  boost::array<char, 4096> _raw; // raw reads from socket
  string _buf; // player input buffer
  queue< string > _cmds; // player command buffer
  const int _player_id;
  bool _flushed; // set true if a player flushed (--) their buffer this tick
  socket_server* _server;
  enum { MAX_COMMANDS = 100 };
};



class socket_server {

public:
  socket_server( boost::asio::io_service &io_service ) ;

  // @todo rename receive
  void tick( socket_data &data );

  // disconnect a player from the server
  void disconnect( int id ) ;
  void disconnect( vector< int > ids );

  void send( int id, string msg );
  void send( vector< int > ids, string msg );

private:

  friend class player_connection;

  // lost link occurs when the client disconnects. A clean quit will always result in the server disconnecting
  // the client.
  void lost_link( int );

  void start_accept();

  void handle_accept( socket_ptr socket, const boost::system::error_code& error );

  tcp::acceptor _acceptor;
  map< int, player_connection::player_connection_ptr > _connections; // active player connections
  vector< int > _lost_link; // list of players who have lost link this tick
  vector< int > _new_cons; // list of players who have connected this tick
};

#endif

