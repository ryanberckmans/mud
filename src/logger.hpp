#ifndef LOGGER_H
#define LOGGER_H

#include <iostream>
#include <sstream>
#include <string>
#include <map>
#include <boost/shared_ptr.hpp>

using namespace std;

// Log Channels
#define CHANNEL_NONE 0
#define SS 1 << 1 // Socket Server
#define CR 1 << 2 // Command Router
#define PY 1 << 3 // Python
#define AC 1 << 4 // Account System

// Usage
#define LOG(channel, msg) { std::stringstream logs; logs << msg; Logger::instance()->log( logs.str(), channel, Logger::LOG_HIGH ); }

#define LOG_HIGH(channel, msg ) LOG( channel, msg )
#define LOG_MED(channel, msg) { std::stringstream logs; logs << msg; Logger::instance()->log( logs.str(), channel, Logger::LOG_MED ); }
#define LOG_LOW(channel, msg) { std::stringstream logs; logs << msg; Logger::instance()->log( logs.str(), channel, Logger::LOG_LOW ); }
#define LOG_LEVEL( level ) { Logger::instance()->level( level ) }


//********
// Logger
//********
class Logger {

public:
	static boost::shared_ptr<Logger> instance(int level=LOG_LOW);

	void log( const string msg, const int channel, const int level );
	void log( const string msg, const int channel );
	void log( const string msg );

	void log( const char* const msg, const int channel, const int level);
	void log( const char* const msg, const int channel );
	void log( const char* const msg);

	enum {
		LOG_MAX = -1,
		LOG_HIGH,
		LOG_MED,
		LOG_LOW,
		LOG_MIN
	};
    
    void level( int log_level ) { _log_level = log_level; } 
    int level() { return _log_level; }

private:
	ostream &out;
	int _log_level;
	static boost::shared_ptr<Logger> inst;
	map< int, string> channels;

	Logger( ostream& out, const int level = LOG_HIGH );

};


#endif
