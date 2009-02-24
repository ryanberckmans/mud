#ifndef CMD_ROUTER_H
#define CMD_ROUTER_H

class cmd_router {

public:
   cmd_router( boost::asio::io_service &io_service, 
               socket_data &data,
               socket_server &server );


private:

  void start();

  void tick();


  socket_data &_socket_data;
  boost::asio::deadline_timer _timer;
  socket_server &_server;
  std::set<int> _logged_on; // ids of logged on players

};

#endif
